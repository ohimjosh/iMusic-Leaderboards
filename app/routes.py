from sys import audit
from flask.helpers import url_for
from flask_wtf import form
from app import app, db
from flask import render_template, flash, redirect, request
from app.forms import LoginForm, RegistrationForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Song
from werkzeug.urls import url_parse
import csv



# CSV Reading
def readData():
    song_data = {}
    file_addresss = '/home/damien/python/336_project/app/static/top50spotifySongs.csv'
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
    # print(song_data)
    return song_data




@app.route('/')
@app.route('/index')
def index():
    data = readData()
    for key, value in data.items():
        s = Song(id=key,
                 track_name=value['TrackName'],
                 artist_name=value['Artist'],
                 genre=value['Genre'],
                 beats_per_minute=value['BeatsPerMinute'],
                 popularity=value['Popularity'])
        print(s)



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

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

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
    
@app.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)
