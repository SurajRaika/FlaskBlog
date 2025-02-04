from flask import   render_template , url_for , redirect  ,abort , Blueprint
from FlaskBlog import  db 
from FlaskBlog.posts.forms import PostForm 
from FlaskBlog.models import  Post
from flask_login import  current_user
from FlaskBlog.main.routes import  inject_menu




# variables






posts=Blueprint("posts", __name__)

inject_menu=posts.context_processor(inject_menu)




@posts.route("/post/<int:post_id>")
def post(post_id):
    # post=Post.query.get(post_id)
    # let use another 
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title , post=post)



@posts.route("/post/<int:post_id>/Delete")
def Delete(post_id):
    # let use another 
    post=Post.query.get_or_404(post_id)
    if not post.author == current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home'))


