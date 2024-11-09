import db_cmds as db
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'CDSCOHORT7GROUP7'
DEFAULT_SESSION_USER_ID = "35653693"
session_user_id = DEFAULT_SESSION_USER_ID

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        session_user_id = request.form['session_user_id']
    else:
        session_user_id = DEFAULT_SESSION_USER_ID
    users = db.get_all_users()
    posts = db.get_all_posts()
    top_tracks = db.get_top_tracks()
    return render_template('index.html', session_user_id=session_user_id, top_tracks=top_tracks, users=users)

@app.route('/user/<int:user_id>')
def getUser(user_id):
    user = db.get_user(user_id)
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@app.route('/createUser', methods=('GET', 'POST'))
def createUser():
    if request.method == 'POST':
        user_id = request.form['user_id']
        tracks = request.form['user_tracks']
        location = request.form['location']
        if not tracks:
            flash('Track selection is required!')
        if not location:
            flash('Location selection is required!')
        else:
            db.insertUser(user_id, tracks, location)
            return redirect(url_for('index'))
    return render_template('createUser.html')


@app.route('/user/<int:user_id>/edit', methods=('GET', 'POST'))
def editUser(user_id):
    user = db.get_user(user_id)
    userPref = db.getPreferences(user_id)
    print("User Preference", userPref)
    if request.method == 'POST':
        tracks = request.form['user_tracks']
        location = request.form['location']
        if not tracks:
            flash('Track selection is required!')
        if not location:
            flash('Location selection is required!')
        else:
            db.editUser(user_id, tracks, location)
            return redirect(url_for('index'))
    return render_template('editUser.html', user=user, userPref=userPref)

@app.route('/user/<int:user_id>/delete', methods=('POST',))
def deleteUser(user_id):
    db.deleteUser(user_id)
    flash('"{}" was successfully deleted!'.format(user_id))
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')