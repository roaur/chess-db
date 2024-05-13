from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn

settings = Settings()

async def handle_player_data(game_data):
    players = game_data['players']
    player_data = {}
    for player in players:
        player_data[player['color']] = player['user']
        player_data[player['color']]['rating'] = player['rating']
        player_data[player['color']]['seconds'] = player['seconds']
        logger.debug(f"Player data: {player_data}")
    return player_data
