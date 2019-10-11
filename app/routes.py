from flask import Flask, render_template,url_for,redirect,flash
from flask_wtf import form
from app import db
from app.forms import RegistrationForm
from flask import Flask, redirect, render_template, request, session, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

from app.forms import LoginForm
from app import app
from flask_login import current_user,login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)


@app.route('/',methods=['GET','POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if current_user.is_authenticated:
        return redirect(url_for('index',user=user))
    if form.validate_on_submit():
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index',user=user))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/ok', methods=['GET', 'POST'])
@login_required
def index():
    print("inside index")
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']

    # handle image upload from Dropszone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)

            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename
            )

            # append image urls
            file_urls.append(photos.url(filename))


            # db.session.add('photo url',photos.url(filename))
            # db.session.commit()
        session['file_urls'] = file_urls
        temp_str1=filename+','
        ok=User.query.filter_by(username=current_user.username).first()
        print('ok username',ok)
        print('ok.imageurl', ok.image_url)
        if ok.image_url==None:
            ok.image_url=temp_str1
        else:


           temp_str =ok.image_url + ','
           temp_str+=temp_str1
           print(temp_str)
           ok.image_url=temp_str
        #print('userrr',user)
        db.session.add(ok)
        db.session.commit()
        return "uploading..."
    # return dropzone template on GET request
    return render_template('index.html')




# @app.route('/index')
# @login_required
# def index():
#     return render_template("index.html",title="homepage")



@app.route('/logout')
def logout():
    logout_user()
    return redirect((url_for('index')))

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


@app.route('/results')
def results():
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))

    # set the file_urls and remove the session variable

    file_urls = session['file_urls']
    print(file_urls)
    # user= User(image_url=file_urls)
    # db.session.add(user)
    # db.session.commit()

    session.pop('file_urls', None)

    return render_template('results.html', file_urls=file_urls)

@app.route('/temp')
def temp():
    return render_template("temp.html", title="homepage")



