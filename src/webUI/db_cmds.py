import sqlite3
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('sqlite/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_top_tracks():
    top_tracks_query = """SELECT tr.track_Id, tr.track_title, 
    tr.tweet_count, tr.artist_id, art.artist_name
    FROM track tr, Artist art
    WHERE tr.artist_id = art.artist_id
    ORDER BY tr.tweet_count DESC"""
    conn = get_db_connection()
    top_tracks = conn.execute(top_tracks_query).fetchall()
    conn.close()
    return top_tracks


def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM USER').fetchall()
    conn.close()
    return users

def get_all_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return posts


def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM USER WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def getPreferences(user_id):
    conn = get_db_connection()
    user_pref = conn.execute('Select tracks, location From USER_PREFERENCE WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return user_pref

def insertUser(user_id, tracks, location):
    conn = get_db_connection()
    conn.execute('INSERT INTO USER (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    insertPreferences(user_id, tracks, location)


def insertPreferences(user_id, tracks, location):
    conn = get_db_connection()
    conn.execute('INSERT INTO USER_PREFERENCE (user_id, tracks, location) VALUES (?, ?, ?)', (user_id, tracks, location))
    conn.commit()
    conn.close()


def insertPost(title, content):
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()


def editUser(user_id, tracks, location):
    deleteUserPreferences(user_id)
    insertPreferences(user_id, tracks, location)

def editPost(title, content, id):
    conn = get_db_connection()
    conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                 (title, content, id))
    conn.commit()
    conn.close()


def deleteUser(user_id):
    deleteUserPreferences(user_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM USER WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


def deleteUserPreferences(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM USER_PREFERENCE WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def deletePost(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()