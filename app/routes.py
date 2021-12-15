from datetime import datetime
from sys import audit
from flask.helpers import url_for
from flask_wtf import form
from app import app, db
from flask import render_template, flash, redirect, request
from app.forms import LoginForm, RegistrationForm, EmptyForm, EditProfileForm
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song
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
            # print(row)
            song_data[row[0]] = {'TrackName' : row[1],
                                 'Artist' : row[2],
                                 'Genre' : row[3],
                                 'BeatsPerMinute' : row[4],
                                 'Popularity': row[len(row) - 1]}
    song_data.pop('')
    data = song_data

    for key, value in data.items():
        s = Song.query.filter_by(id=value.get('id')).first()
        if s is None:
            #print(value['Popularity'])
            s = Song(id=key,
                     track_name=value['TrackName'],
                     artist_name=value['Artist'],
                     genre=value['Genre'],
                     beats_per_minute=value['BeatsPerMinute'],
                     popularity=value['Popularity'])
            print(s)
            db.session.add(s)
            db.session.commit()
        else:
            print("Already in db")
    




@app.route('/')
@app.route('/index')
def index():
#    readData()
    user = {'username': 'Josh'}
    posts = [
        {
            'author': {'username': 'John'},
            'body' : 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body' : 'The Avengers movie was so cool!'
            
        }
    ]
    
    return render_template ('index.html', title = 'Home', user=user, posts=posts)

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
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()












































