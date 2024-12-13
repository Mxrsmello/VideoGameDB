from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import sqlite3
# global var for user :|
current_user_id = None


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect('videogame.db')

@app.route('/')
def index():
    
    """Home page with navigation links."""
    # this is new!
    global current_user_id
    if not current_user_id:
        return redirect('/login')
    
    username = session.get('username')

    return render_template('index.html', username=username)

@app.route('/games')
def games():
    """View all games."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Games")
    games = cursor.fetchall()
    conn.close()
    return render_template('games.html', games=games)

@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    """Add a new game."""
    if request.method == 'POST':
        name = request.form['name']
        genre = request.form['genre']
        release_date = request.form['release_date']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Games (name, genre, release_date) VALUES (?, ?, ?)", 
                       (name, genre, release_date))
        conn.commit()
        conn.close()
        username = session.get('username')
        return redirect('/games')
    return render_template('add_game.html', username=username)

@app.route('/search_games', methods=['GET', 'POST'])
def search_games():
    username = session.get('username')
    if request.method == 'POST':
        title = request.form.get('title', '')
        genre = request.form.get('genre', '')
        developer = request.form.get('developer', '')
        
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT g.g_gamekey, 
                   g.g_title, 
                   d.d_name AS developer, 
                   g.g_base_cost, 
                   GROUP_CONCAT(gn.gn_name, ', ') AS genres
            FROM games g
            LEFT JOIN developers d ON g.g_developer = d.d_devkey
            LEFT JOIN game_genres gg ON g.g_gamekey = gg.gg_gamekey
            LEFT JOIN genres gn ON gg.gg_genrekey = gn.gn_genrekey
            WHERE g.g_title LIKE ? AND gn.gn_name LIKE ? AND d.d_name LIKE ?
            GROUP BY g.g_gamekey
        """
        cursor.execute(query, (f"%{title}%", f"%{genre}%", f"%{developer}%"))
        games = cursor.fetchall()
        conn.close()
        return render_template('search_results.html', games=games, username=username)
    return render_template('search_games.html', username=username)



@app.route('/game_details/<int:game_id>')
def game_details(game_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect to login if no user is logged in

    conn = connect_db()
    cursor = conn.cursor()

    # Fetch game details, including the developer's country
    query = """
    SELECT g.g_title, d.d_name, g.g_base_cost, g.g_release_year, r.r_global,
       GROUP_CONCAT(DISTINCT gn.gn_name) AS genres,
       GROUP_CONCAT(DISTINCT p.p_name) AS platforms,
       d.d_country
    FROM games g
    LEFT JOIN developers d ON g.g_developer = d.d_devkey
    LEFT JOIN ratings r ON g.g_gamekey = r.r_title
    LEFT JOIN game_genres gg ON g.g_gamekey = gg.gg_gamekey
    LEFT JOIN genres gn ON gg.gg_genrekey = gn.gn_genrekey
    LEFT JOIN game_platforms gp ON g.g_gamekey = gp.gp_gamekey
    LEFT JOIN platforms p ON gp.gp_platformkey = p.p_platformkey
    WHERE g.g_gamekey = ?
    GROUP BY g.g_gamekey
    """
    cursor.execute(query, (game_id,))
    game = cursor.fetchone()

    conn.close()

    if not game:
        return "Game not found"

    # Render the template with game details
    return render_template('game_details.html', game=game, username=username)


@app.route('/purchase_game/<int:game_id>', methods=['POST'])
def purchase_game(game_id):
    global current_user_id  # Example user ID; replace with session user ID
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO owns (o_uid, o_gamekey, o_date_purchased) VALUES (?, ?, DATE('now'))"
    try:
        cursor.execute(query, (current_user_id, game_id))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    return redirect('/my_games')


from datetime import datetime

@app.route('/play/<int:game_id>', methods=['POST'])
def play_game(game_id):
    """Update the Last Played date in the plays table or insert a new record."""
    global current_user_id  # Replace with session-based user management
    conn = connect_db()
    cursor = conn.cursor()

    # Today's date in YYYY-MM-DD format
    today = datetime.now().strftime('%Y-%m-%d')

    # Query to check if the game has been played by the user
    check_query = """
        SELECT p_last_played FROM plays WHERE p_uid = ? AND p_gamekey = ?
    """
    cursor.execute(check_query, (current_user_id, game_id))
    record = cursor.fetchone()

    if record:
        # Update the p_last_played date
        update_query = """
            UPDATE plays
            SET p_last_played = ?
            WHERE p_uid = ? AND p_gamekey = ?
        """
        cursor.execute(update_query, (today, current_user_id, game_id))
    else:
        # Insert a new record if the game hasn't been played before
        insert_query = """
            INSERT INTO plays (p_uid, p_gamekey, p_last_played)
            VALUES (?, ?, ?)
        """
        cursor.execute(insert_query, (current_user_id, game_id, today))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "last_played": today}), 200

@app.route('/write_review/<int:game_id>', methods=['GET', 'POST'])
def write_review(game_id):
    username = session.get('username')
    if request.method == 'POST':
        global current_user_id  # Replace with actual session user ID
        rating = float(request.form['rating'])  # Convert to float
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            INSERT INTO reviews (rv_uid, rv_gamekey, rv_rating) VALUES (?, ?, ?)
            ON CONFLICT(rv_uid, rv_gamekey) DO UPDATE SET rv_rating = ?
        """
        try:
            cursor.execute(query, (current_user_id, game_id, rating, rating))  # Store directly as /5
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
        return redirect('/game_details/' + str(game_id))
    return render_template('write_review.html', game_id=game_id, username=username)

@app.route('/manage_friends', methods=['GET', 'POST'])
def manage_friends():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect if no user is logged in

    conn = connect_db()
    cursor = conn.cursor()

    # Retrieve current user ID based on the username
    cursor.execute("SELECT u_uid FROM users WHERE u_name = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found"  # Handle case where the user doesn't exist

    current_user_id = user[0]

    # Handle adding or removing friends
    if request.method == 'POST':
        action = request.form.get('action')
        friend_id = request.form.get('friend_id')

        if action == 'add':  # Add a friend
            query = "INSERT INTO friends (f_uid1, f_uid2) VALUES (?, ?)"
            try:
                cursor.execute(query, (current_user_id, friend_id))
                conn.commit()
            except Exception as e:
                print(f"Error adding friend: {e}")
        elif action == 'remove':  # Remove a friend
            query = "DELETE FROM friends WHERE (f_uid1 = ? AND f_uid2 = ?) OR (f_uid1 = ? AND f_uid2 = ?)"
            try:
                cursor.execute(query, (current_user_id, friend_id, friend_id, current_user_id))
                conn.commit()
            except Exception as e:
                print(f"Error removing friend: {e}")

    # Retrieve list of friends
    query_friends = """
        SELECT u.u_uid, u.u_name
        FROM users u
        INNER JOIN friends f ON u.u_uid = f.f_uid2
        WHERE f.f_uid1 = ?
    """
    cursor.execute(query_friends, (current_user_id,))
    friends = cursor.fetchall()
    no_friends = len(friends) == 0

    # Retrieve games owned by the current user
    query_my_games = """
        SELECT g.g_gamekey, g.g_title
        FROM owns o
        INNER JOIN games g ON o.o_gamekey = g.g_gamekey
        WHERE o.o_uid = ?
    """
    cursor.execute(query_my_games, (current_user_id,))
    my_games = set(cursor.fetchall())  # Use a set for easy comparison

    # Retrieve friends' games and find shared games
    friends_games = {}
    shared_games = {}

    for friend in friends:
        friend_id = friend[0]

        # Get games owned by the friend
        cursor.execute(query_my_games, (friend_id,))
        friend_games = cursor.fetchall()
        friends_games[friend_id] = friend_games

        # Find shared games
        shared_games[friend_id] = [game for game in friend_games if game in my_games]

    conn.close()

    # Render the template with shared games data
    return render_template(
        'friends.html',
        friends=friends,
        username=username,
        no_friends=no_friends,
        friends_games=friends_games,
        shared_games=shared_games,
    )

@app.route('/friend_games/<int:friend_id>', methods=['GET'])
def friend_games(friend_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect if no user is logged in

    conn = connect_db()
    cursor = conn.cursor()

    # Get current user ID
    cursor.execute("SELECT u_uid FROM users WHERE u_name = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found"  # Handle case where the user doesn't exist

    current_user_id = user[0]

    # Retrieve friend's name
    cursor.execute("SELECT u_name FROM users WHERE u_uid = ?", (friend_id,))
    friend = cursor.fetchone()

    if not friend:
        conn.close()
        return "Friend not found"  # Handle case where the friend doesn't exist

    friend_name = friend[0]

    # Get games owned by the friend
    query_friend_games = """
        SELECT g.g_gamekey, g.g_title
        FROM owns o
        INNER JOIN games g ON o.o_gamekey = g.g_gamekey
        WHERE o.o_uid = ?
    """
    cursor.execute(query_friend_games, (friend_id,))
    friend_games = cursor.fetchall()

    # Get games owned by the current user
    cursor.execute(query_friend_games, (current_user_id,))
    my_games = {game[0] for game in cursor.fetchall()}  # Use a set for easy lookup

    # Mark games as owned or not
    games_with_ownership = [
        {'gamekey': game[0], 'title': game[1], 'owned': game[0] in my_games}
        for game in friend_games
    ]

    conn.close()

    return render_template(
        'friend_games.html',
        username=username,
        friend_name=friend_name,
        games_with_ownership=games_with_ownership,
    )

@app.route('/my_games')
def my_games():
    """Display the user's purchased games with the date purchased and last played."""
    username = session.get('username')
    global current_user_id  # Example user ID; replace with session user ID
    conn = connect_db()
    cursor = conn.cursor()
    query = """
        SELECT 
            g.g_gamekey, 
            g.g_title, 
            g.g_base_cost, 
            o.o_date_purchased,
            p.p_last_played
        FROM owns o
        JOIN games g ON o.o_gamekey = g.g_gamekey
        LEFT JOIN plays p ON o.o_gamekey = p.p_gamekey AND o.o_uid = p.p_uid
        WHERE o.o_uid = ?
    """
    cursor.execute(query, (current_user_id,))
    games = cursor.fetchall()
    conn.close()
    return render_template('my_games.html', games=games, username=username)


@app.route('/reviews')
def reviews():
    """View all reviews made by the current user."""
    username = session.get('username')
    global current_user_id  # Assume this variable tracks the logged-in user's ID
    conn = connect_db()
    cursor = conn.cursor()

    # Query to fetch games reviewed by the user
    query = """
        SELECT 
            g.g_title, 
            g.g_base_cost, 
            g.g_release_year, 
            d.d_name, 
            r.rv_rating
        FROM reviews r
        JOIN games g ON r.rv_gamekey = g.g_gamekey
        JOIN developers d ON g.g_developer = d.d_devkey
        WHERE r.rv_uid = ?
    """
    try:
        cursor.execute(query, (current_user_id,))
        reviews = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        reviews = []
    finally:
        conn.close()

    # Check if the user has any reviews
    no_reviews = len(reviews) == 0

    return render_template('reviews.html', no_reviews=no_reviews, reviews=reviews, username=username)

# this is new! 
@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user_id
    if request.method == 'POST':

        username = request.form['username']
        _conn = connect_db()
        cursor = _conn.cursor()

        query = """
        SELECT u_uid
            FROM users
            WHERE u_name = ?
        """

        cursor.execute(query, (username,)) # tuple
        user = cursor.fetchone()
        
        # checking if the user exists. make a user profile.
        if user:
            current_user_id = user[0]
            session['username'] = username
            _conn.close()
            return redirect('/')
        
        else:
            query = """
            SELECT MAX(u_uid)
                FROM users"""
            
            cursor.execute(query)
            max_id = cursor.fetchone()[0]

            new_user_id = max_id + 1

            query = """
            INSERT INTO users (u_uid, u_name) VALUES (?, ?)
            """

            cursor.execute(query, (new_user_id, username))
            _conn.commit()
            _conn.close()

            current_user_id = new_user_id
            session['username'] = username #saves username in session

            return redirect('/')
    return render_template('login.html')

@app.route('/add_to_library/<int:game_id>', methods=['POST'])
def add_to_library(game_id):
    conn = connect_db()
    cursor = conn.cursor()
    # check if in library
    query = """
    SELECT *
        FROM owns
        WHERE o_uid = ?
        AND o_gamekey = ?
    """
    cursor.execute(query, (current_user_id, game_id))
    exists = cursor.fetchone()

    if not exists:
        query = """
            INSERT INTO owns (o_uid, o_gamekey, o_date_purchased) 
            VALUES (?, ?, DATE('now'))
        """
        cursor.execute(query, (current_user_id, game_id))
        conn.commit()

    conn.close()
    return redirect('/search_games')



if __name__ == '__main__':
    app.run(debug=True)
