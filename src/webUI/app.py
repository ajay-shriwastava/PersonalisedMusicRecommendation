import db_cmds as db
from flask import Flask, render_template, request, url_for, flash, redirect
import json
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'CDSCOHORT7GROUP7'
DEFAULT_SESSION_USER_ID = "35653693"
session_user_id = DEFAULT_SESSION_USER_ID

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        session_user_id = request.form['session_user_id']
        session_user = db.get_user(session_user_id)
    else:
        session_user_id = DEFAULT_SESSION_USER_ID
        session_user = db.get_user(session_user_id)
    users = db.get_all_users()
    top_tracks = db.get_top_tracks()
    return render_template('index.html', session_user=session_user, top_tracks=top_tracks, users=users)

@app.route('/createUser', methods=('GET', 'POST'))
def createUser():
    if request.method == 'POST':
        user_id = request.form['user_id']
        location = request.form['location']
        if not location:
            flash('Location selection is required!')
        else:
            db.insertUser(user_id, location)
            return redirect(url_for('index'))
    return render_template('createUser.html')


@app.route('/user/<int:user_id>/edit', methods=('GET', 'POST'))
def editUser(user_id):
    user = db.get_user(user_id)
    if request.method == 'POST':
        tracks = request.form.getlist('user_tracks')
        print("Type of tracks is", type(tracks), tracks)
        if not tracks:
            flash('Track selection is required!')
        else:
            prefStr = user['preferences']
            print("Existing Preference Dictionary", prefStr)
            prefDict = {}
            if prefStr:
                prefDict = json.loads(prefStr)
            prefDict['tracks'] = tracks
            print("Tracks updated", prefDict)
            new_pref_str = json.dumps(prefDict)
            db.editUser(user_id, new_pref_str)
            return redirect(url_for('index'))
    return render_template('editUser.html', user=user)

@app.route('/user/<int:user_id>/delete', methods=('POST',))
def deleteUser(user_id):
    db.deleteUser(user_id)
    flash('"{}" was successfully deleted!'.format(user_id))
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')