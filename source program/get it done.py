from flask import Flask,request,redirect, render_template, session,flash
from flask_sqlalchemy import SQLAlchemy

app= Flask (__name__)
app.config['DEBUG']= True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://get-it-done:lc101@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='56ka52dh10#$@abn'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(120))
    completed = db.Column(db. Boolean)


    def __init__(self, name,owner):
        self.name = name
        self.completed= False
        self.owner

@app.before_request
def require_login():
    allowed_routes = ['login','register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')
    
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(120), unique=True)
    password=db.Column(db.String(120))
    tasks= db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password
       

@app.route('/login', methods =['POST','GET'] )
def login():
    if request.method == 'POST':
        email=request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email= email).first()
        if user and user.password == password:
            session['email'] =email
            flash("Logged In!")
            return redirect('/')
        else:
            flash( 'User password is incorrect, or user is not registered','error')
            return  redirect('/login')
            
    return render_template('login.html')

@app.route('/register', methods =['POST','GET'])
def register():
     if request.method == 'POST':
        email=request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if len(email) == 0:
            flash("The email field was left blank.", 'error')
            return  redirect('/register')
        else:
            email = email
        if len(password) == 0:
            flash('The password field was left blank.', 'error')
            return render_template("register.html", email = email, password='', verify='')
        else:
            password = password
        if len(verify) == 0:
            flash('The verify password field was left blank.', 'error')
            return render_template("register.html", email = email, password='', verify='')
        else:
            verify = verify

    # --------Invalid Username, Password, Email-------------

        if len(email) != 0:
            if len(email) < 5 or len(email) > 40 or ' ' in email or '@' not in email or '.' not in email:
                # if '@' not in email and '.' not in email:
                flash('Email must be between 4 and 20 characters long, cannot contain spaces, and must be in proper email format.', 'error')
                return  redirect('/register')
            else:
                email = email

        if len(password) != 0:
            if len(password) < 4 or len(password) > 19 or ' ' in password:
                flash("The password must be between 4 and 19 characters long and cannot contain spaces.", 'error')
                return  render_template("register.html", email = email, password='', verify='')
            else:
                password = password

    # --------Password and Verify Do Not Match----------

        for char, letter in zip(password, verify):
            if char != letter:
                flash('Passwords do not match.', 'error')
                return render_template("register.html", email =email, password='', verify='')
            else:
                verify = verify
                password = password

        if email and password and verify:
      
            existing_user = User.query.filter_by(email= email).first()

        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] =email
            return redirect('/')
        else:
    
            return "<h1> Duplicate user </h1>"

     return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    
    owner = User.query.filter_by(email= session['email']).first()

    if request.method == 'POST':
        task_name = request.form['task']   
        new_task =Task(task_name,owner)
        db.session.add(new_task)
        db.session.commit()
   

    tasks = Task.query.filter_by (completed=False, owner=owner).all()
    completed_tasks =Task.query.filter_by(completed=True, owner=owner).all()
    return render_template('todos.html',title="Get It Done!",
     tasks=tasks, completed_tasks=completed_tasks)



@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task_id'])
    task= Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()
    
    return redirect('/')


if __name__ == '__main__':
    app.run()