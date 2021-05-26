from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

import forms
from seed import *
from models import User

app = Flask(__name__)
app.secret_key = 'my_secret_key'
csrf = CsrfProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/git_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)


@app.route('/',methods=['GET','POST'])
def index():
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        session['username'] = comment_form.username.data
        session['email'] = comment_form.email.data
        session['total'] = comment_form.total.data
        return redirect('seed' )
    title = "Login"
    return render_template('index.html', title= title, form=comment_form)


@app.route('/seed')
def seed():
    get_users(int(session['total']))
    return redirect('git_list')


@app.route('/git_list',methods=['GET','POST'])
def git_list():
    users = User(int(session['total']))
    #list = User.query.join(User)
    title = "Git Hub Users"
    return render_template('git_view.html',title=title, list = users.get_data() )

if __name__ == '__main__':
    app.run(debug=True)