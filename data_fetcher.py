import os
from datetime import datetime
from bitget_client import BitgetClient
from database import get_db_connection

def fetch_and_store_data():
    client = BitgetClient()
    symbols = ["BTC_USDT", "ETH_USDT"]  # Example symbols
    intervals = ["1m", "5m", "15m"]     # Example intervals

    conn = get_db_connection()
    cursor = conn.cursor()

    for symbol in symbols:
        for interval in intervals:
            try:
                candles = client.fetch_candles(symbol, interval)
                for candle in candles:
                    timestamp = datetime.fromtimestamp(candle[0] / 1000)  # Assuming timestamp is in milliseconds
                    open_price = float(candle[1])
                    high_price = float(candle[2])
                    low_price = float(candle[3])
                    close_price = float(candle[4])
                    volume = float(candle[5])

                    cursor.execute("""
                        INSERT INTO candles (time, instrument_id, timeframe, open, high, low, close, volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (time, instrument_id, timeframe) DO UPDATE
                        SET open = EXCLUDED.open,
                            high = EXCLUDED.high,
                            low = EXCLUDED.low,
                            close = EXCLUDED.close,
                            volume = EXCLUDED.volume;
                    """, (timestamp, symbol, interval, open_price, high_price, low_price, close_price, volume))

                conn.commit()
            except Exception as e:
                print(f"Failed to fetch or store data for {symbol} with interval {interval}: {e}")

    cursor.close()
    conn.close()
