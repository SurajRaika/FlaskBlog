from flask import  render_template , url_for ,flash , redirect , request ,abort , Blueprint
from FlaskBlog import  db ,bcrypt
from FlaskBlog.users.forms import RegistrationForm , LoginForm , AccountForm , change_password_Form , ConfirmPossword
from FlaskBlog.models import User , Post
from flask_login import login_user , current_user , logout_user , login_required
from FlaskBlog.users.utils import save_picture , delete_image ,sendMail
from FlaskBlog.main.routes import  inject_menu

# variables






users=Blueprint("users", __name__)


inject_menu=users.context_processor(inject_menu)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and  bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/registration", methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        # if not  User.query.filter_by(username=form.username.data).first() == '':
        if User.query.filter_by(email=form.email.data).first() == None and User.query.filter_by(username=form.username.data).first() == None:
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data , email=form.email.data  , password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('users.login'))
        else:
            if User.query.filter_by(email=form.email.data).first() == None:
                flash(f'Account aready  created for {form.email.data}!', 'danger')
            else:
                flash(f'Account aready  created for {form.username.data}!', 'danger')

            # return redirect(url_for('registration'))

    return render_template('registration.html', title='Register', form=form)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))




@users.route("/account", methods=['GET', 'POST'])
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

        return redirect(url_for('users.account'))
    # elif request.method ==["GET"]:
    else:
        form.username.data=current_user.username
    return render_template('account.html', title='Account' , form=form)




@users.route("/user/<string:username>")
def User_posts(username):
    user=User.query.filter_by(username=username).first_or_404()
    page=request.args.get('page',1,type=int)
    data=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template("user_post.html",title='My Post',posts=data)



@users.route("/account/confirm-email-password_Reset/", methods=['GET', 'POST'])
def Reset_password_Confirm_Email():

    form=ConfirmPossword()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            sendMail(user)
            # flash(f'Password Reset link is sended to your {form.email.data} ', 'success')
            flash(f'this service is stopped temporary ', 'danger')
        else:
            flash(f'{form.email.data} is not been registered', 'danger')

    return render_template("Reset_password_Confirm_Email.html",title='Confirm paoasword',form=form)




@users.route("/account/password-reset/<token>", methods=['GET', 'POST'])
def Reset_token(token): 
    user=User.varify_token(token)
    if user is None:
        flash(  ' that is invalid token or expired '  , 'danger')
        return redirect(url_for('users.login'))
    else:
        flash(  f' Hy {user.email} '  , 'success')
        form=change_password_Form()
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return redirect(url_for('users.login'))
    return render_template("Reset_password.html",title='Reset Password',form=form)

