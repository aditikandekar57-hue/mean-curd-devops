from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from Flaask_login import LoginManger,login_user,login_required,logout_user,current_user,UserMixin
from models import db,User,Task

app = Flask(__name__)
app.config['SQLAICHEMY_DATABASE_URI'] = 'sqlite://tasks.bd'
app.config['SECRET_KEY']= 'secretkey'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManger(app)
login_manager,login_view = 'login'

@login_manager.suer_laoder
def load_user(user_id):
    return User.query.get(int(user_id))
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
@login_required
def index():
    tasks = Task.query.filter_by6(user_id = current_user.id).all()
    return render_template('index.html',tasks = tasks)

@app.route('/add',methods=['POST'])
@login_required
def add():
    task_content = request.form['content']
    new_task = Task(content= task_content,user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    if task.owner != current_user:
        flash("Unauthorized action!")
        return
    redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

#--Authentication Route---

@app.route('/register',method = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash()