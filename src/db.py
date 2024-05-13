import psycopg
import psycopg_pool
from utils import settings
from contextlib import asynccontextmanager
import logging
import asyncio

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logging.getLogger("psycopg.pool").setLevel(logging.DEBUG)

SETTINGS = settings

logging.debug(f"Database URL: {SETTINGS.DATABASE_URL}")

pool = None


async def init_db_pool():
    global pool
    pool = psycopg_pool.AsyncConnectionPool(str(SETTINGS.DATABASE_URL), max_size=25, open=False)
    await pool.open()
    await pool.wait()
    logging.info("Database connection pool ready.")
    # return pool


@asynccontextmanager
async def get_db_connection():
    if pool is None:
        await init_db_pool()
    conn = await pool.getconn()
    try:
        yield conn
    finally:
        await pool.putconn(conn)
