import requests
import os
import threading
import concurrent.futures

import datetime
import pytz

from typing import List, Tuple

class BitgetClient:

    BASE_URL = "https://api.bitget.com/api/v2/mix/market/history-mark-candles"
    INSTRUMENTS_URL = "https://api.bitget.com/api/v2/mix/market/tickers?productType=USDT-FUTURES"
    TIMEFRAMES = ['1m']
    request_limit = 20 
    semaphore = threading.Semaphore(request_limit)

    def __init__(self):
        self.api_key = os.getenv('BITGET_API_KEY') or ''
        self.secret_key = os.getenv('BITGET_SECRET_KEY') or ''

    def _generate_time_intervals(start_datetime, end_datetime=datetime.datetime.now().replace(second=0, microsecond=0), timeframe='1D', range=200):
        intervals = []
        current_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone('Europe/Paris'))
        end_datetime = end_datetime.replace(tzinfo=pytz.timezone('Europe/Paris'))

        # Define the size of the intervals for each timeframe
        timeframe_intervals = {
            '1W': datetime.timedelta(weeks=1*12),
            '1m': datetime.timedelta(minutes=1*range),
            '5m': datetime.timedelta(minutes=5*range),
            '15m': datetime.timedelta(minutes=15*range),
            '30m': datetime.timedelta(minutes=30*range),
            '1H': datetime.timedelta(hours=1*range),
            '4H': datetime.timedelta(hours=4*range),
            '1D': datetime.timedelta(days=1*90),
        }

        # Get the size of the intervals for the specified timeframe
        interval = timeframe_intervals[timeframe]

        # Generate the intervals
        while current_datetime < end_datetime:
            next_datetime = current_datetime + interval
            if next_datetime > end_datetime:
                next_datetime = end_datetime
            intervals.append((current_datetime.replace(second=0, microsecond=0), next_datetime.replace(second=0, microsecond=0)))
            current_datetime = next_datetime

        return intervals

    def _fetch_candles(self,  symbol: str, granularity: str, interval: List[Tuple[datetime.datetime, datetime.datetime]], product: str ='usdt-futures'):
    
        start_time, end_time = interval

        start_time = int(start_time.timestamp()) * 1000
        end_time = int(end_time.timestamp()) * 1000

        params = {
                        "symbol": f"{symbol}",
                        "productType": product,
                        "granularity": f"{granularity}",
                        "limit": "200",
                        "startTime": start_time,
                        "endTime": end_time
                    }

        with self.semaphore:
            response = requests.get(self.BASE_URL, params=params)
            data = response.json()['data']
            # print(len(data))
            return data

    def populate_to_db(self):
        intervals = []
        for tf in self.TIMEFRAMES:
            intervals = self._generate_time_intervals(datetime.datetime(2018,1,1,0,0,0), timeframe=tf)

        symbols = [instrument['symbol'] for instrument in self._get_all_instruments()]

        for symbol in symbols:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(lambda interval: self._fetch_candles(symbol, interval, tf), intervals))

    def _get_all_instruments(self):
        
        response = requests.get(self.INSTRUMENTS_URL)
        instruments = response.json()['data']

        return instruments
    

