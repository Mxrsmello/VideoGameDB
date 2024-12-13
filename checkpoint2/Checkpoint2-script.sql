-- Games owned by ShadowMaster (specific user)
SELECT g.g_title
    FROM games g
    JOIN owns o ON g.g_gamekey = o.o_gamekey
    JOIN users u ON o.o_uid = u.u_uid
    WHERE u_name = 'ShadowMaster';

-- Expected Output: Path of Exile, Prey

-- Count how many users play each game
SELECT g_title, COUNT(*) AS player_count
    FROM plays 
    JOIN games ON plays.p_gamekey = games.g_gamekey
    GROUP BY g_title;

-- Avg price of games in 2008
SELECT AVG(g_base_cost) AS avg_price
    FROM games
    WHERE g_release_year = 2008;

-- Expected Output: 20.0

--- Total price of all games owned by StarGazer (user)
SELECT SUM(g.g_base_cost) AS total_price
    FROM games g
    JOIN owns o ON g.g_gamekey = o.o_gamekey
    JOIN users u ON o.o_uid = u.u_uid
    WHERE u.u_name = 'StarGazer';

-- Expected output: 260

-- Developer with most games
SELECT d.d_name, COUNT(g.g_gamekey) AS game_count
    FROM developers d
    JOIN games g ON d.d_devkey = g.g_developer
    GROUP BY d.d_name
    ORDER BY game_count DESC
    LIMIT 1;
-- Expected Output: Valve Software|16

-- All games in order of developer
SELECT g.g_title, d.d_name
    FROM games g
    JOIN developers d ON g.g_developer = d.d_devkey
    ORDER BY d.d_name;

-- All games in order of provided sample ratings
SELECT g.g_title, r.r_global
    FROM games g
    JOIN ratings r ON g.g_gamekey = r.r_title
    ORDER BY r.r_global DESC;

-- All games that EchoBlade has that their friend VortexSamurai also owns
SELECT g.g_title
    FROM games g
    JOIN owns o1 ON g.g_gamekey = o1.o_gamekey
    JOIN owns o2 ON g.g_gamekey = o2.o_gamekey
    JOIN friends f ON o1.o_uid = f.f_uid1 AND o2.o_uid = f.f_uid2
    JOIN users u1 ON f.f_uid1 = u1.u_uid
    JOIN users u2 ON f.f_uid2 = u2.u_uid
    WHERE u1.u_name = 'EchoBlade' OR u2.u_name = 'VortexSamurai';

-- Expected Output: Bioshock

-- Worst rated game
SELECT g.g_title, r.r_global
    FROM games g
    JOIN ratings r ON g.g_gamekey = r.r_title
    ORDER BY r.r_global ASC
    LIMIT 1;

-- Expected Output: Counter-Strike: Global Offensive|2.9 (yeah sounds about right lol)

-- All users that own the game Hotline Miami
SELECT u.u_name
    FROM users u
    JOIN owns o ON u.u_uid = o.o_uid
    JOIN games g ON o.o_gamekey = g.g_gamekey
    WHERE g.g_title = 'Hotline Miami';

-- Expected Output: PixelNinja, EchoBlade

--  Last time NebulaKnight played a game they share with their friend
SELECT g.g_title, MAX(p1.p_last_played) AS last_played
    FROM games g
    JOIN plays p1 ON g.g_gamekey = p1.p_gamekey
    JOIN plays p2 ON g.g_gamekey = p2.p_gamekey
    JOIN friends f ON p1.p_uid = f.f_uid1 AND p2.p_uid = f.f_uid2
    JOIN users u ON f.f_uid1 = u.u_uid
    WHERE u.u_name = 'NebulaKnight'
    GROUP BY g.g_title;

-- Expected Output: Mass Effect|2024-01-08, Wolfenstein: The New Order|2023-11-29

-- Genres of game 
SELECT gn.gn_name
    FROM genres gn
    JOIN game_genres gg ON gn.gn_genrekey = gg.gg_genrekey
    JOIN games g ON gg.gg_gamekey = g.g_gamekey
    WHERE g.g_title = 'Fallout: New Vegas';

-- Expected Output: RPG, Indie, Strategy (Indie? Maybe because of Obsidian but okay lol)

-- Get all games released after 2015 along with their platforms
SELECT g_title, p_name FROM games 
JOIN game_platforms ON games.g_gamekey = game_platforms.gp_gamekey 
JOIN platforms ON game_platforms.gp_platformkey = platforms.p_platformkey 
WHERE g_release_year > 2015;

-- List all developers established before 2000
SELECT d_name
FROM developers
WHERE d_established < 2000;

-- Find popular games (games owned by multiple users)
SELECT g_title, COUNT(*) AS ownership_count 
FROM owns 
JOIN games ON owns.o_gamekey = games.g_gamekey 
GROUP BY g_title 
HAVING COUNT(*) > 1;

-- Query to find games owned by friends of a specific user (e.g., Alice)
SELECT u2.u_name AS friend, g_title 
FROM friends 
JOIN users u1 ON friends.f_uid1 = u1.u_uid 
JOIN users u2 ON friends.f_uid2 = u2.u_uid 
JOIN owns ON owns.o_uid = u2.u_uid 
JOIN games ON owns.o_gamekey = games.g_gamekey 
WHERE u1.u_name = 'Alice';

-- Retrieve all reviews and ratings provided by friends of a user for recommendations
SELECT u2.u_name AS friend, g_title, rv_rating 
FROM friends 
JOIN users u1 ON friends.f_uid1 = u1.u_uid 
JOIN users u2 ON friends.f_uid2 = u2.u_uid 
JOIN reviews ON reviews.rv_uid = u2.u_uid 
JOIN games ON reviews.rv_gamekey = games.g_gamekey 
WHERE u1.u_name = 'Alice';

-- Find popular games (games owned by multiple users)
SELECT g_title, COUNT(*) AS ownership_count 
FROM owns 
JOIN games ON owns.o_gamekey = games.g_gamekey 
GROUP BY g_title 
HAVING COUNT(*) > 1;

-- Check what games a user is currently playing, with last played date
SELECT u_name, g_title, p_last_played 
FROM plays 
JOIN users ON plays.p_uid = users.u_uid 
JOIN games ON plays.p_gamekey = games.g_gamekey;

-- Retrieve games with high global ratings for potential recommendations
SELECT g_title, r_global 
FROM ratings 
JOIN games ON ratings.r_title = games.g_gamekey 
WHERE r_global > 4.0 
ORDER BY r_global DESC;

-- Retrieve all games released in a specific year, showing historical preferences.
SELECT g_title 
FROM games 
WHERE g_release_year = 2017;

-- Identify developers with the highest number of games owned by users.
SELECT d_name, COUNT(g_gamekey) AS game_count 
FROM developers 
JOIN games ON developers.d_devkey = games.g_developer 
JOIN owns ON games.g_gamekey = owns.o_gamekey 
GROUP BY d_name 
ORDER BY game_count DESC;


-- Adding additional users
INSERT INTO users (u_uid, u_name) VALUES (21, 'LuckySteel'), (22, 'ZwagXerath');

-- Adding friends for social interactions
INSERT INTO friends (f_uid1, f_uid2) VALUES (1, 2), (1, 3), (2, 4);

-- Inserting user-owned games for ownership tracking
INSERT INTO owns (o_uid, o_gamekey, o_date_purchased) VALUES (1, 1, '2023-08-01'), (2, 2, '2023-07-15');

-- Recording games users are currently playing
INSERT INTO plays (p_uid, p_gamekey, p_last_played) VALUES (1, 1, '2023-09-10'), (2, 2, '2023-09-05');

-- Adding ratings and reviews for user engagement
INSERT INTO ratings (r_ratingkey, r_global, r_title) VALUES (1, 4.5, 1), (2, 4.2, 2);
INSERT INTO reviews (rv_uid, rv_gamekey, rv_rating) VALUES (1, 1, 4.5), (2, 2, 4.0);
