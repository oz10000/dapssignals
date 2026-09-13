# data_engine.py
"""
DataEngine con PAGINACIÓN para obtener muchas velas.
"""
import os
import time
import logging
import pandas as pd
import ccxt
from typing import Optional, List
from config import EXCHANGE_PRIORITY, CACHE_DIR, TIMEFRAME, SYMBOLS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataEngine:

    def __init__(self):
        self.cache_dir = CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
        self.exchanges = {}
        self.primary = None
        self._connect_exchanges()

    def _connect_exchanges(self):
        for ex_id in EXCHANGE_PRIORITY:
            try:
                ex_class = getattr(ccxt, ex_id)
                exchange = ex_class({
                    'enableRateLimit': True,
                    'options': {'defaultType': 'spot'},
                    'rateLimit': 1200,
                })
                exchange.load_markets()
                self.exchanges[ex_id] = exchange
                if self.primary is None:
                    self.primary = ex_id
                logger.info(f"✅ Conectado a {ex_id}")
            except Exception as e:
                logger.warning(f"⚠️ No se pudo conectar a {ex_id}: {e}")

        if not self.exchanges:
            logger.error("❌ No hay exchanges disponibles.")

    def fetch_ohlcv(self, symbol: str, timeframe: str = None,
                    limit: int = 1000, use_cache: bool = True) -> Optional[pd.DataFrame]:
        """
        Descarga OHLCV con PAGINACIÓN para superar el límite del exchange (~500-1000).
        """
        if timeframe is None:
            timeframe = TIMEFRAME

        cache_file = os.path.join(
            self.cache_dir,
            f"{symbol.replace('/', '_')}_{timeframe}_{limit}.parquet"
        )

        # Caché válida por 1 hora
        if use_cache and os.path.exists(cache_file):
            try:
                df = pd.read_parquet(cache_file)
                if not df.empty:
                    age = (pd.Timestamp.now() - df.index[-1]).total_seconds()
                    if age < 3600:
                        return df
            except Exception:
                pass

        # Intentar en cada exchange
        for ex_id, exchange in self.exchanges.items():
            try:
                df = self._fetch_with_pagination(exchange, symbol, timeframe, limit)
                if df is not None and not df.empty:
                    if use_cache:
                        try:
                            df.to_parquet(cache_file)
                        except Exception:
                            pass
                    logger.debug(f"✅ {symbol} desde {ex_id}: {len(df)} velas")
                    return df
            except ccxt.BadSymbol:
                logger.debug(f"❌ {symbol} no existe en {ex_id}")
                continue
            except Exception as e:
                logger.debug(f"⚠️ {symbol}@{ex_id}: {e}")
                continue

        logger.warning(f"❌ No se pudo obtener {symbol}")
        return None

    def _fetch_with_pagination(self, exchange, symbol: str,
                                timeframe: str, total_limit: int) -> Optional[pd.DataFrame]:
        """
        Descarga velas usando paginación (múltiples llamadas).
        Los exchanges devuelven máximo 500-1000 velas por llamada.
        """
        # Detectar el límite por llamada del exchange
        exchange_max = 500  # default conservador
        try:
            if hasattr(exchange, 'options') and 'fetchOHLCV' in exchange.options:
                exchange_max = exchange.options['fetchOHLCV'].get('maxLimit', 500)
            elif hasattr(exchange, 'limits') and exchange.limits.get('fetchOHLCV'):
                exchange_max = exchange.limits['fetchOHLCV'].get('max', 500)
        except Exception:
            pass

        # Si el total es menor al máximo del exchange, una sola llamada
        if total_limit <= exchange_max:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=total_limit)
            return self._to_dataframe(ohlcv)

        # Si no, hacer paginación
        all_ohlcv = []
        remaining = total_limit
        since = None  # timestamp desde dónde traer

        # Calcular cuántas llamadas necesitamos
        n_calls = (total_limit // exchange_max) + 1

        for _ in range(n_calls):
            if remaining <= 0:
                break

            call_limit = min(exchange_max, remaining)

            try:
                if since is None:
                    # Primera llamada: traer las más recientes
                    ohlcv = exchange.fetch_ohlcv(
                        symbol, timeframe, limit=call_limit
                    )
                else:
                    # Llamadas siguientes: traer velas más antiguas (backward)
                    ohlcv = exchange.fetch_ohlcv(
                        symbol, timeframe, since=since, limit=call_limit
                    )

                if not ohlcv:
                    break

                # Prepend (más antiguas primero)
                all_ohlcv = ohlcv + all_ohlcv

                # Actualizar "since" para la siguiente llamada (más antiguo)
                since = ohlcv[0][0] - (self._tf_to_ms(timeframe) * call_limit)

                remaining -= len(ohlcv)

                # Rate limit preventivo
                time.sleep(exchange.rateLimit / 1000.0)

                # Si recibimos menos de los pedidos, no hay más historia
                if len(ohlcv) < call_limit:
                    break

            except Exception as e:
                logger.debug(f"Paginación falló: {e}")
                break

        if not all_ohlcv:
            return None

        df = self._to_dataframe(all_ohlcv)
        if df is not None:
            # Deduplicar por timestamp y ordenar
            df = df[~df.index.duplicated(keep='first')].sort_index()
        return df

    @staticmethod
    def _to_dataframe(ohlcv: list) -> Optional[pd.DataFrame]:
        if not ohlcv:
            return None
        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        df = df[(df['high'] >= df['low']) & (df['close'] > 0)]
        return df

    @staticmethod
    def _tf_to_ms(tf: str) -> int:
        """Convierte timeframe a milisegundos."""
        tf_map = {
            '1m': 60_000, '3m': 180_000, '5m': 300_000, '15m': 900_000,
            '30m': 1_800_000, '1h': 3_600_000, '4h': 14_400_000, '1d': 86_400_000
        }
        return tf_map.get(tf, 300_000)

    def get_symbols(self) -> List[str]:
        return SYMBOLS
