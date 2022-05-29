from flask import Flask , render_template , url_for ,flash , redirect , request
from FlaskBlog import app , db ,bcrypt
from FlaskBlog.form import RegistrationForm , LoginForm
from FlaskBlog.models import User , Post
from flask_login import login_user , current_user , logout_user , login_required

data = [
    {'author':'Suraj','title':'Not What you think in machine learning','content':'As we know guys that today everyyyyyyyy one is waitingggggg for some ......','date_posted':'April 20 2020'}
    ,{'author':'Ravi','title':'Lorem, ipsum dolor.','content':'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Sunt, dolorum.','date_posted':'march 20 2020'}
    ,{'author':'John Wick','title':'Ullam esse mollitia.','content':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Ullam esse mollitia, placeat rem natus molestias aliquid odio dicta sequi nisi optio sapiente quos.','date_posted':'march 20 2020'}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title='Home',posts=data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and  bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/registration", methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        # if not  User.query.filter_by(username=form.username.data).first() == '':
        if User.query.filter_by(email=form.email.data).first() == None:
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data , email=form.email.data  , password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Account aready  created for {form.email.data}!', 'danger')
            # return redirect(url_for('registration'))

    return render_template('registration.html', title='Register', form=form)




@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required                       # decorator
def account():
    return render_template('account.html', title='Account')
