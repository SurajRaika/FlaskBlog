

import secrets
import os
from PIL import Image
from flask import  url_for 
from FlaskBlog import app  ,mail
from flask_mail import Message

# variables








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



def sendMail(user):
    token=user.get_token()
    msg=Message('Password Reset Request',recipients=[user.email],sender='http://127.0.0.1:5000/')
    msg.body=f''' 
    Reset your Possword 
        {url_for('users.Reset_token',token=token ,_external=True)}
     '''
    mail.send(msg)