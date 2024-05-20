import concurrent.futures
import requests
import aiohttp
import json
import logging
import asyncio
from stream_context import StreamContext
from data import DataFetcher, DataProcessor

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def run_stream_context(url, client_session):
    data_fetcher = DataFetcher(url, client_session)
    data_stream = StreamContext(data_fetcher, DataProcessor())
    async for data in data_fetcher.fetch_data():
        await data_stream.processor.handle_data(data)


async def main():
    urls = [
        "https://lichess.org/api/tv/rapid/feed",
        "https://lichess.org/api/tv/blitz/feed",
        "https://lichess.org/api/tv/bullet/feed",
        "https://lichess.org/api/tv/classical/feed",
        "https://lichess.org/api/tv/ultraBullet/feed",
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [run_stream_context(url, session) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Run the streaming function
    asyncio.run(main())

