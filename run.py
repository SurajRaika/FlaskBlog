from flask import Flask , render_template ,flash
from form import RegistrationForm
app=Flask(__name__)
app.config['SECRET_KEY'] = '1677626b7f3074acc0f04c9fdf62145a'
data = [{'author':'Suraj','title':'Not What you think in machine learning','content':'As we know guys that today everyyyyyyyy one is waitingggggg for some ......','date_posted':'April 20 2020'},{'author':'Ravi','title':'Running a love stry ','content':'so story begin with ','date_posted':'march 20 2020'}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",posts=data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html" )

@app.route("/registration",methods=['POST',"GET"])
def registration():
    form=RegistrationForm()
    if form.email.data == 'suajraika5sr@gmail.com' and form.password.data == "suajraika5sr@gmail.com":
            flash(f' Logged In ','success')
            return redirect(url_for("home")) 
    else :
            flash(f'Wrong Password or email ','danger')
    return render_template("registration.html",form = form )

if __name__=="__main__":
    app.run(debug=True)