from datetime import datetime
from sys import audit
from flask.helpers import url_for
from flask_wtf import form
from app import app, db
from flask import render_template, flash, redirect, request, url_for
from app.forms import LoginForm, RegistrationForm, EmptyForm, EditProfileForm
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song, SongData
from werkzeug.urls import url_parse
import csv
import os

# CSV Reading
def readData():
    song_data = {}
    path = os.path.abspath(os.path.dirname('top50spotifySongs.csv'))
    file_addresss = os.path.join(path, 'app/top50spotifySongs.csv')
    with open(file_addresss, 'r', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            song_data[row[0]] = {'TrackName' : row[1],
                                 'Artist' : row[2],
                                 'Genre' : row[3],
                                 'BeatsPerMinute' : row[4],
                                 'Energy' : row[5],
                                 'Danceability' : row[6],
                                 'Loudness_dB' : row[7],
                                 'Liveness' : row[8],
                                 'Valence' : row[9],
                                 'Length' : row[10],
                                 'Acousticness' : row[11],
                                 'Speechiness' : row[12]}
                                 #'Popularity': row[len(row) - 1]}
    song_data.pop('')
    data = song_data

    for key, value in data.items():
        s = Song.query.filter_by(id=key).first()
        print(s)
        if s is None:
            s = Song(id=key,
                     track_name=value['TrackName'],
                     artist_name=value['Artist'],
                     genre=value['Genre'],
                     beats_per_minute=value['BeatsPerMinute'])

            s_data = SongData(song_id=s.id,
                              danceability=value['Danceability'],
                              loudness_dB=value['Loudness_dB'],
                              valence=value['Valence'],
                              acousticness=value['Acousticness'],
                              speechiness=value['Speechiness'])


            print(s_data)
            db.session.add(s)
            db.session.add(s_data)
            db.session.commit()
        else:
            print("Already in db")
    




@app.route('/')
@app.route('/index')
def index():
    r = readData()
    user = {'username': 'Josh'}
    return render_template ('index.html', title = 'Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/terminate')
def terminate():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        db.session.delete(user)
        db.session.commit()
        flash('Account terminated.')
        return redirect(url_for('login'))
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
        flash('Account not signed in.')
    return redirect(next_page)
    
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    
    
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)    

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/leaderboard')
def leaderboard():
    all_songs = Song.query.order_by(Song.id.asc()).all()
    return render_template('leaderboard.html', all_songs=all_songs)


@app.route('/leaderboard/<int:songID>')
def song_page(songID):
    song = Song.query.filter_by(id=songID).first_or_404()
    return render_template('song_page.html', song=song)


@app.route('/leaderboard/<int:songID>/<action>')
@login_required
def song_follow(songID, action):
    song = Song.query.filter_by(id=songID).first_or_404()
    if action == "follow":
        current_user.song_follow(song)
        flash('You are following {}'.format(song.track_name))
        db.session.commit()
    elif action == "unfollow":
        current_user.song_unfollow(song)
        flash('You unfollowed {}'.format(song.track_name))
        db.session.commit()
    return redirect(request.referrer)

@app.route("/tutorial")
@login_required
def tutorial():
    return render_template('tutorial.html', title='Tutorial')















