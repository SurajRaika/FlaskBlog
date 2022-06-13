from flask import Blueprint , render_template , request , url_for , abort , flash , redirect , current_app
from FlaskBlog.models import Post
import os
from FlaskBlog import  db
from FlaskBlog.posts.forms import PostForm
from flask_login import  current_user  , login_required
No_of_post_in_1_page=5 


main=Blueprint("main", __name__)



def inject_menu():
    if current_user.is_authenticated and os.path.exists(os.path.join(current_app.root_path , 'static/profile_pic' ,current_user.image_file)):
        curr_profile_picture=url_for('static',filename='profile_pic/'+ (current_user.image_file))
        print("exits")
    else:
        curr_profile_picture=url_for('static',filename='profile_pic/'+ 'default.jpg')


    return dict(curr_profile_picture=curr_profile_picture)


inject_menu=main.context_processor(inject_menu)



@main.route("/")
@main.route("/home" ,  methods=['GET', 'POST'])
@main.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
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
            return redirect(url_for('main.home'))
        elif request.method == 'GET' :
            Form_Post.title.data=post.title
            Form_Post.content.data=post.content

    else:
        if Form_Post.validate_on_submit():
            post1=Post(title=Form_Post.title.data,content=Form_Post.content.data,user_id=current_user.id) 
            db.session.add(post1) 
            db.session.commit()

            flash('Your post has been created !','success')
            return redirect(url_for('main.home'))

    page=request.args.get('page',1,type=int)
    data=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=No_of_post_in_1_page)
    
    return render_template("home.html",title='Home',posts=data , Form_Post = Form_Post,legend_title_and_Post_Form=legend_title_and_Post_Form)

@main.route("/about")
def about():
    return render_template("about.html")






