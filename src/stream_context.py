import logging
from utils import handle_player_data
from db import get_db_connection


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class StreamContext:
    def __init__(self):
        self.game_id = None
        self.move_num = 0

    def generate_move_id(self):
        return f"{self.game_id}-{self.move_num}"

    async def handle_data(self, data):
        if data['t'] == 'featured':
            # Insert new game and players into database
            self.game_id = data['d']['id']
            await self.insert_players(data['d']['players'])
            await self.insert_game(self.game_id, data['d'])
        elif data['t'] == 'fen' and self.game_id is not None:
            self.move_num += 1
            # Insert move into database
            await self.insert_move(data['d'], self.game_id)

    async def insert_game(self, game_id, game_data):
        # Insert game into database
        player_data = await handle_player_data(game_data)
        id = game_id
        game_orientation = game_data['orientation']
        white_player_id = player_data['white']['id']
        black_player_id = player_data['black']['id']
        white_rating = player_data['white']['rating']
        black_rating = player_data['black']['rating']
        initial_fen = game_data['fen']
        async with get_db_connection() as aconn:
            async with aconn.cursor() as acur:
                logger.debug(f"Inserting game {id} into database.")
                await acur.execute(
                    "INSERT INTO games (game_id, white_player_id, black_player_id, white_rating, black_rating, initial_fen, orientation) VALUES (%s, %s, %s, %s, %s, %s, %s) ON conflict do nothing;",
                    (id, white_player_id, black_player_id, white_rating, black_rating, initial_fen, game_orientation)
                )
                await aconn.commit()
                logger.debug(f"Game {id} inserted into database.")


    async def insert_players(self, players):
        for player in players:
            # Insert player into database
            user = player['user']
            player_name = user['name']
            player_title = user['title'] if 'title' in user else None
            player_id = user['id']
            async with get_db_connection() as aconn:
                async with aconn.cursor() as acur:
                    logger.debug(f"Upserting player {player_name} into database.")
                    await acur.execute(
                        "INSERT INTO players (player_id, name, title) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                        (player_id, player_name, player_title)
                    )
                    await aconn.commit()
                    logger.debug(f"Player {player_name} upserted into database.")


    async def insert_move(self, move, game_id):
        fen = move['fen']
        last_move = move['lm']
        white_clock = move['wc']
        black_clock = move['bc']
        async with get_db_connection() as aconn:
            async with aconn.cursor() as acur:
                logger.debug(f"Inserting move {last_move} into database.")
                await acur.execute(
                    "INSERT INTO moves (move_id, game_id, fen, last_move, white_clock, black_clock) VALUES (%s, %s, %s, %s, %s, %s);",
                    (self.generate_move_id(), game_id, fen, last_move, white_clock, black_clock)
                )
                await aconn.commit()
                logger.debug(f"Move {last_move} inserted into database.")