import logging
import requests
import json
import asyncio
import concurrent.futures
from utils import handle_player_data
from db import get_db_connection


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class StreamContext:
    def __init__(self, fetcher, processor):
        self.fetcher = fetcher
        self.processor = processor
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


    async def run(self):
        loop = asyncio.get_running_loop()
        while True:
            # Run fetch_data in a separate thread
            data_generator = await loop.run_in_executor(self.executor, self.fetcher.fetch_data)
            for data in data_generator:
                await self.processor.process_data(data)
