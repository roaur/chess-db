CREATE TABLE players (
    player_id text PRIMARY KEY,
    name text,
    title text,
    flair text
);

CREATE TABLE games (
    game_id text PRIMARY KEY,
    orientation text,
    white_player_id text,
    black_player_id text,
    white_rating int,
    black_rating int,
    initial_fen TEXT,
    FOREIGN KEY (white_player_id) REFERENCES players(player_id),
    FOREIGN KEY (black_player_id) REFERENCES players(player_id),
    game_time timestamp DEFAULT now()
);

CREATE TABLE moves (
    move_id text PRIMARY KEY,
    game_id text,
    fen TEXT,
    last_move text,
    white_clock INT,
    black_clock INT,
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);