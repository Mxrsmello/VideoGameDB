DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS developers;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS plays;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS game_genres;
DROP TABLE IF EXISTS game_platforms;
DROP TABLE IF EXISTS platforms;
DROP TABLE IF EXISTS devby;
DROP TABLE IF EXISTS owns;

CREATE TABLE developers (
    d_devkey DECIMAL(5,0) PRIMARY KEY,
    d_name VARCHAR(100),
    d_country VARCHAR(50),
    d_established DECIMAL(4,0)
);

CREATE TABLE genres (
    gn_genrekey DECIMAL(5,0) PRIMARY KEY, 
    gn_name VARCHAR(50)
);

CREATE TABLE platforms (
    p_platformkey DECIMAL(5,0) PRIMARY KEY,
    p_name VARCHAR(50)
);


CREATE TABLE users (
    u_uid DECIMAL(5,0) PRIMARY KEY,
    u_name VARCHAR(100)
);

CREATE TABLE games (
    g_gamekey DECIMAL(5,0) PRIMARY KEY,
    g_title VARCHAR(100),
    g_developer DECIMAL(5,0),
    g_base_cost DECIMAL (5,2),
    g_release_year INTEGER, 
    FOREIGN KEY (g_developer) REFERENCES developers(d_devkey)
);

CREATE TABLE ratings (
    r_ratingkey DECIMAL(5,0) PRIMARY KEY,
    r_global DECIMAL(3,2),
    r_title DECIMAL(5,0)
);

CREATE TABLE reviews (
    rv_uid DECIMAL(5,0),
    rv_gamekey DECIMAL(5,0),
    rv_rating DECIMAL(3,2),
    PRIMARY KEY (rv_uid, rv_gamekey),
    FOREIGN KEY (rv_uid) REFERENCES users(u_uid),
    FOREIGN KEY (rv_gamekey) REFERENCES games(g_gamekey)
);

CREATE TABLE friends (
    f_uid1 DECIMAL(5,0),
    f_uid2 DECIMAL(5,0),
    FOREIGN KEY (f_uid1) REFERENCES users(u_uid),
    FOREIGN KEY (f_uid2) REFERENCES users(u_uid)
);

CREATE TABLE owns (
    o_uid DECIMAL(5,0),
    o_gamekey DECIMAL(5,0),
    o_date_purchased DATE,
    PRIMARY KEY (o_uid, o_gamekey),
    FOREIGN KEY (o_uid) REFERENCES users(u_uid),
    FOREIGN KEY (o_gamekey) REFERENCES games(g_gamekey)
);

CREATE TABLE plays (
    p_uid DECIMAL(5,0),
    p_gamekey DECIMAL(5,0),
    p_last_played DATE,
    PRIMARY KEY (p_uid, p_gamekey),
    FOREIGN KEY (p_uid) REFERENCES users(u_uid),
    FOREIGN KEY (p_gamekey) REFERENCES games(g_gamekey)
);

CREATE TABLE game_genres (
    gg_gamekey DECIMAL(5,0),
    gg_genrekey DECIMAL(5,0),
    PRIMARY KEY (gg_gamekey, gg_genrekey),
    FOREIGN KEY (gg_gamekey) REFERENCES games(g_gamekey),
    FOREIGN KEY (gg_genrekey) REFERENCES genres(gn_genrekey)
);

CREATE TABLE game_platforms (
    gp_gamekey DECIMAL(5,0),
    gp_platformkey DECIMAL(5,0),
    PRIMARY KEY (gp_gamekey, gp_platformkey),
    FOREIGN KEY (gp_gamekey) REFERENCES games(g_gamekey),
    FOREIGN KEY (gp_platformkey) REFERENCES platforms(p_platformkey)
);

CREATE TABLE devby (
    g_gamekey DECIMAL(5,0),
    d_devkey DECIMAL(5,0),
    PRIMARY KEY (g_gamekey, d_devkey),
    FOREIGN KEY (g_gamekey) REFERENCES games(g_gamekey),
    FOREIGN KEY (d_devkey) REFERENCES developers(d_devkey)
);
