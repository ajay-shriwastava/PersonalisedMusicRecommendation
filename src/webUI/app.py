from flask import Flask, render_template, request, url_for, flash, redirect
import json
from werkzeug.exceptions import abort
import db_cmds as db
import lookup
from lookup import cache
import itemitemcfmodel
import collabFile
import contentFile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CDSCOHORT7GROUP7'
cache.init_app(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})

DEFAULT_SESSION_USER_ID = "17291429"
session_user_id = DEFAULT_SESSION_USER_ID


@app.route('/', methods=('GET', 'POST'))
@app.route('/<int:session_user_id>', methods=('GET', 'POST'))
def index(session_user_id=DEFAULT_SESSION_USER_ID):
    if request.method == 'POST':
        session_user_id = request.form['session_user_id']
    if not session_user_id:
        session_user_id = DEFAULT_SESSION_USER_ID
    session_user = db.get_user(session_user_id)
    prefStr = session_user['preferences']
    prefDict = {}
    if prefStr:
        prefDict = json.loads(prefStr)
    users = db.get_all_users()
    top_tracks = db.get_top_tracks()
    print("Getting itemitemfcmodel from cache")
    item2item = cache.get("itemitemcfmodel")
    if not item2item:
        print("Setting itemitemfcmodel to cache")
        item2item = itemitemcfmodel.item2itemcfModel()
        cache.set("itemitemcfmodel", item2item)
    reco_df = item2item.topn_recommendation(float(session_user_id), 15)
    return render_template('index.html', session_user=session_user, preferences=prefDict, top_tracks=top_tracks,
                           users=users, reco_df=reco_df)

@app.route('/collabFilter', methods=('GET', 'POST'))
def collabFilter(song_index=0):
    sel_song =0
    reco_songs=0
    if request.method == 'POST':
        song_index = request.form['song_index_id']
    if not song_index:
        song_index = 0
    song_index = int(song_index)
    colabF = cache.get("collabFilter")
    if not colabF:
        colabF = collabFile.CollabFilter()
        cache.set("collabFilter", colabF)
    sel_song = colabF.track_df.iloc[song_index]
    reco_songs = colabF.track_df.iloc[colabF.cosine_similarity(song_index, 12)]
    track_df = colabF.track_df
    user_df = colabF.user_df
    user_item_df = colabF.user_item_df
    return render_template('collab_filter.html', sel_song=sel_song, reco_songs=reco_songs,
                           track_df=track_df, user_df=user_df, user_item_df=user_item_df)


@app.route('/contentFilter', methods=('GET', 'POST'))
def contentFilter(song_index=6):
    columns = ["Id", "artist_name", "track_title", "genre_rnb",	"genre_rap", "genre_electronic", "genre_rock",
               "genre_newage", "genre_classical"]
    reco_songs = 0
    if request.method == 'POST':
        song_index = request.form['song_index_id']
    if not song_index:
        song_index = 0
    print("Song index obtained", song_index)
    song_index = int(song_index)
    conFilter = cache.get("conFilter")
    if not conFilter:
        conFilter = contentFile.ContentFilter()
        cache.set("conFilter", conFilter)
    reco_songs = conFilter.recommend_songs(song_index, n_recommendations = 10)
    genreDf = conFilter.get_genres().head(10)
    return render_template('contentFilter.html', genreDf=genreDf, song_index=song_index,
                           columns=columns, reco_songs=reco_songs)


@app.route('/createUser', methods=('GET', 'POST'))
def createUser():
    if request.method == 'POST':
        user_id = request.form['user_id']
        locations = request.form.getlist('user_locations')
        languages = request.form.getlist('user_languages')
        genres = request.form.getlist('user_genres')
        if not locations:
            flash('Location is required!')
        elif not languages:
            flash('Language is required!')
        else:
            prefDict = {'locations': locations, 'languages': languages}
            if genres:
                prefDict['genres'] = genres
            new_pref_str = json.dumps(prefDict)
            db.insertUser(user_id, new_pref_str)
            return redirect(url_for('index', session_user_id=user_id))
    return render_template('createUser.html', locations_lookup=lookup.locations_lookup,
                           languages_lookup=lookup.languages_lookup, genres_lookup=lookup.genres_lookup)


@app.route('/user/<int:user_id>/edit', methods=('GET', 'POST'))
def editUser(user_id):
    user = db.get_user(user_id)
    prefStr = user['preferences']
    prefDict = {}
    if prefStr:
        prefDict = json.loads(prefStr)
    if request.method == 'POST':
        tracks = request.form.getlist('user_tracks')
        if not tracks:
            flash('Track selection is required!')
        else:
            prefDict['tracks'] = tracks
            new_pref_str = json.dumps(prefDict)
            db.editUser(user_id, new_pref_str)
            return redirect(url_for('index', session_user_id=user_id))
    return render_template('editUser.html', user=user, preferences=prefDict, tracks_lookup=lookup.tracks_lookup)


@app.route('/user/<int:user_id>/delete', methods=('POST',))
def deleteUser(user_id):
    db.deleteUser(user_id)
    flash('"{}" was successfully deleted!'.format(user_id))
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')
