import secrets
import os
from PIL import Image
import cv2
from flask import Flask , render_template , url_for ,flash , redirect , request ,abort
from FlaskBlog import app , db ,bcrypt ,mail
from FlaskBlog.form import RegistrationForm , LoginForm , AccountForm ,PostForm , change_password_Form , ConfirmPossword
from FlaskBlog.models import User , Post
from flask_login import login_user , current_user , logout_user , login_required
from flask_mail import Message

# variables
No_of_post_in_1_page=5 





@app.context_processor
def inject_menu():
    if current_user.is_authenticated and os.path.exists(os.path.join(app.root_path , 'static/profile_pic' ,current_user.image_file)):
        curr_profile_picture=url_for('static',filename='profile_pic/'+ (current_user.image_file))
    else:
        curr_profile_picture=url_for('static',filename='profile_pic/'+ 'default.jpg')


    return dict(curr_profile_picture=curr_profile_picture)

@app.route("/")
@app.route("/home" ,  methods=['GET', 'POST'])
@app.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
@login_required
def home(post_id=None):
    Form_Post = PostForm()
    legend_title_and_Post_Form=["Create Post",'collapse']

    if not post_id==None:
        legend_title_and_Post_Form=["Update Post",""]
        post=Post.query.get_or_404(post_id)
        if not post.author == current_user:
            abort(403)
        if Form_Post.validate_on_submit():
            post.title=Form_Post.title.data
            post.content=Form_Post.content.data
            db.session.commit()
            flash(f"updated","success")  
            return redirect(url_for('home'))
        elif request.method == 'GET' :
            Form_Post.title.data=post.title
            Form_Post.content.data=post.content

    else:
        if Form_Post.validate_on_submit():
            post1=Post(title=Form_Post.title.data,content=Form_Post.content.data,user_id=current_user.id) 
            db.session.add(post1) 
            db.session.commit()

            flash('Your post has been created !','success')
            return redirect(url_for('home'))

    page=request.args.get('page',1,type=int)
    data=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=No_of_post_in_1_page)
    
    return render_template("home.html",title='Home',posts=data , Form_Post = Form_Post,legend_title_and_Post_Form=legend_title_and_Post_Form)

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
        if User.query.filter_by(email=form.email.data).first() == None and User.query.filter_by(username=form.username.data).first() == None:
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data , email=form.email.data  , password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        else:
            if User.query.filter_by(email=form.email.data).first() == None:
                flash(f'Account aready  created for {form.email.data}!', 'danger')
            else:
                flash(f'Account aready  created for {form.username.data}!', 'danger')

            # return redirect(url_for('registration'))

    return render_template('registration.html', title='Register', form=form)




@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def delete_image(myfile):
    ## If file exists, delete it ##
    if not "default" in myfile:    
            myfile=os.path.join(app.root_path , 'static/profile_pic' ,myfile)
            if os.path.isfile(myfile):
                os.remove(myfile)
            # else:    ## Show an error ##
                # flash(f'{myfile} file not found!', 'danger')
                # print("Error: %s file not found" % myfile)
    # else:
                # flash(f'{myfile} is default ', 'danger')

def save_picture(form_picture ):
    random_hex=secrets.token_hex(8)
    
    _ , f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/profile_pic' ,picture_fn)
    image=Image.open(form_picture)
    width , height=image.size
    w1=(25/100)*width
    w2=(75/100)*width
    new_width=w2-w1
    Gap= height - new_width
    h1=Gap/2
    h2=height-Gap/2
    image = image.crop((int(w1), int(h1), int(w2), int(h2)))
    if width > 125 and height >125:
        image.thumbnail((125,125))


    image.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required 
def account():
    form=AccountForm()
    if form.validate_on_submit():
        if form.picture.data and form.Picture_save.data:
            picture_file = save_picture(form.picture.data)
            delete_image(current_user.image_file)
            current_user.image_file = picture_file
        

        if not current_user.username == form.username.data:
            if not (User.query.filter_by(username=form.username.data).first()):
                current_user.username = form.username.data
            else:
                flash(f'{form.username.data} registrated by another!', 'danger')

        db.session.commit()

        return redirect(url_for('account'))
    # elif request.method ==["GET"]:
    else:
        form.username.data=current_user.username
    return render_template('account.html', title='Account' , form=form)



@app.route("/post/<int:post_id>")
def post(post_id):
    # post=Post.query.get(post_id)
    # let use another 
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title , post=post)



@app.route("/post/<int:post_id>/Delete")
def Delete(post_id):
    # let use another 
    post=Post.query.get_or_404(post_id)
    if not post.author == current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))




@app.route("/user/<string:username>")
def User_posts(username):
    user=User.query.filter_by(username=username).first_or_404()
    page=request.args.get('page',1,type=int)
    data=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=No_of_post_in_1_page)
    return render_template("user_post.html",title='My Post',posts=data)




def sendMail(user):
    token=user.get_token()
    msg=Message('Password Reset Request',recipients=[user.email],sender='http://127.0.0.1:5000/')
    msg.body=f''' 
    Reset your Possword 
        {url_for('Reset_token',token=token ,_external=True)}
     '''
    mail.send(msg)

@app.route("/account/confirm-email-password_Reset/", methods=['GET', 'POST'])
def Reset_password_Confirm_Email():

    form=ConfirmPossword()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            sendMail(user)
            flash(f'Password Reset link is sended to your {form.email.data} ', 'success')
        else:
            flash(f'{form.email.data} is not been registered', 'danger')

    return render_template("Reset_password_Confirm_Email.html",title='Confirm paoasword',form=form)




@app.route("/account/password-reset/<token>", methods=['GET', 'POST'])
def Reset_token(token):
    user=User.varify_token(token)
    if user is None:
        flash(  ' that is invalid token or expired '  , 'danger')
        return redirect(url_for('login'))
    else:
        flash(  f' Hy {user.email} '  , 'success')
        form=change_password_Form()
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("Reset_password.html",title='Reset Password',form=form)

