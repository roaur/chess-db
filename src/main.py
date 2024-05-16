import concurrent.futures
import requests
import json
import logging
import asyncio
from stream_context import StreamContext
from data import DataFetcher, DataProcessor

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def fetch_data(url):
    while True:
        try:
            response = requests.get(url, stream=True)
            for line in response.iter_lines():
                if line:  # filter out keep-alive new lines
                    decoded_line = line.decode('utf-8')
                    data = json.loads(decoded_line)
                    logger.debug(f"Received data: {data}")
                    yield data
        except requests.ChunkedEncodingError:
            logger.error("Error fetching data. Retrying...")
            continue
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            break


async def stream_lichess_tv():
    url = "https://lichess.org/api/tv/feed"
    data_fetcher = DataFetcher(url)
    data_stream = StreamContext(data_fetcher, DataProcessor())
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        data_generator = await loop.run_in_executor(executor, fetch_data, url)
        for data in data_generator:
            await data_stream.processor.handle_data(data)


# Run the streaming function
asyncio.run(stream_lichess_tv())

