# data_engine.py
"""
Motor de datos — CORREGIDO.
Fixes:
  - Eliminada COMPLETAMENTE la generación de datos sintéticos.
  - Solo datos reales de exchanges (CCXT).
  - Si no hay datos, retorna None (nunca inventa).
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
            logger.error("❌ No hay exchanges disponibles. DataEngine no funcional.")

    def fetch_ohlcv(self, symbol: str, timeframe: str = None,
                    limit: int = 300, use_cache: bool = True) -> Optional[pd.DataFrame]:
        """
        Descarga OHLCV REAL. Si falla, retorna None.
        NUNCA genera datos sintéticos.
        """
        if timeframe is None:
            timeframe = TIMEFRAME

        cache_file = os.path.join(
            self.cache_dir,
            f"{symbol.replace('/', '_')}_{timeframe}_{limit}.parquet"
        )

        # Caché válido por 1 hora
        if use_cache and os.path.exists(cache_file):
            try:
                df = pd.read_parquet(cache_file)
                if not df.empty:
                    age = (pd.Timestamp.now() - df.index[-1]).total_seconds()
                    if age < 3600:
                        return df
            except Exception as e:
                logger.debug(f"Caché inválido para {symbol}: {e}")

        # Intentar cada exchange
        for ex_id, exchange in self.exchanges.items():
            for attempt in range(2):
                try:
                    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                    if not ohlcv or len(ohlcv) < 30:
                        logger.debug(f"⚠️ {ex_id}: pocas velas para {symbol}")
                        break

                    df = pd.DataFrame(
                        ohlcv,
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
                    )
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    df.set_index('timestamp', inplace=True)
                    df.sort_index(inplace=True)

                    # Validar OHLC
                    df = df[(df['high'] >= df['low']) & (df['close'] > 0)]

                    if use_cache:
                        try:
                            df.to_parquet(cache_file)
                        except Exception:
                            pass

                    logger.debug(f"✅ {symbol} desde {ex_id} ({len(df)} velas)")
                    return df

                except ccxt.BadSymbol:
                    logger.debug(f"❌ {symbol} no existe en {ex_id}")
                    break
                except Exception as e:
                    logger.debug(f"Intento {attempt+1}/2 {symbol}@{ex_id}: {e}")
                    time.sleep(1)

        logger.warning(f"❌ No se pudo obtener {symbol} de ningún exchange")
        return None

    def get_symbols(self) -> List[str]:
        return SYMBOLS