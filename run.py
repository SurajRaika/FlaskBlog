from flask import Flask , render_template , url_for ,flash , redirect
from form import RegistrationForm , LoginForm



app=Flask(__name__)
app.config['SECRET_KEY'] = '1677626b7f3074acc0f04c9fdf6s145a'
data = [
    {'author':'Suraj','title':'Not What you think in machine learning','content':'As we know guys that today everyyyyyyyy one is waitingggggg for some ......','date_posted':'April 20 2020'}
    ,{'author':'Ravi','title':'Lorem, ipsum dolor.','content':'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Sunt, dolorum.','date_posted':'march 20 2020'}
    ,{'author':'John Wick','title':'Ullam esse mollitia.','content':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Ullam esse mollitia, placeat rem natus molestias aliquid odio dicta sequi nisi optio sapiente quos.','date_posted':'march 20 2020'}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",posts=data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/registration", methods=['GET','POST'])
def registration():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('registration.html', title='Register', form=form)

if __name__=="__main__":
    app.run(debug=True)