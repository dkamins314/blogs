from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app= Flask (__name__)
app.config['DEBUG']= True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blogs:abc123@localhost:8889/blogs'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='56ka52dh10WQOPHT$%$%$'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))


    def __init__(self, title, body, owner):
        self.title = title
        self.body= body
        self.owner
        
    def is_valid(self):
        if self.title and self.body and self.owner:
            return True
        else:
             return False

@app.before_request
def require_login():
    allowed_routes = ['login','register']
    if request.endpoint not in allowed_routes and 'user_name' not in session:
        return redirect('/login')
    
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_name= db.Column(db.String(120), unique=True)
    password=db.Column(db.String(120))
    blogs= db.relationship('Blog', backref='owner')

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
       



@app.route('/register', methods =['POST','GET'])
def register():
     if request.method == 'POST':
        user_name =request.form['user_name']
        password = request.form['password']
        verify = request.form['verify']
        if len(user_name) == 0:
            flash("The name field was left blank.", 'error')
            return render_template('/register')
        else:
            user_name = user_name
        if len(password) == 0:
            flash('The password field was left blank.', 'error')
            return render_template("register.html", user_name = user_name, password='', verify='')
        else:
            password = password
        if len(verify) == 0:
            flash('The verify password field was left blank.', 'error')
            return render_template("register.html", user_name = user_name, password='', verify='')
        else:
            verify = verify

    # --------Invalid Username, Password, Email-------------

        if len(user_name) != 0:
            if len(user_name) < 5 or len(user_name) > 40 or ' ' in user_name:
                # minimum user name
                flash('User_name must be between 4 and 20 characters long, cannot contain spaces.', 'error')
                return  redirect('/register')
            else:
                user_name = user_name

        if len(password) != 0:
            if len(password) < 4 or len(password) > 19 or ' ' in password:
                flash("The password must be between 4 and 19 characters long and cannot contain spaces.", 'error')
                return  render_template("register.html", user_name = user_name, password='', verify='')
            else:
                password = password

    # --------Password and Verify Do Not Match----------

        for char, letter in zip(password, verify):
            if char != letter:
                flash('Passwords do not match.', 'error')
                return render_template("register.html", user_name = user_name, password='', verify='')
            else:
                verify = verify
                password = password

        if user_name and password and verify:
      
            existing_user = User.query.filter_by(user_name= user_name).first()

        if not existing_user:
            new_user = User(user_name, password)
            db.session.add(new_user)
            db.session.commit()
            session['user_name'] =user_name
            return redirect('/single_user_all')
        else:
    
            flash('Duplicate user, please login')

            return render_template('login.html')
     return render_template('register.html')



@app.route('/login', methods =['POST','GET'] )
def login():
    if request.method == 'POST':
        user_name =request.form['user_name']
        password = request.form['password']
        user = User.query.filter_by(user_name= user_name).first()
        if user and user.password == password:
            session['user_name'] =user_name
            flash("Logged In!")
            return redirect('/new_blog')
        else:
            flash( 'User password is incorrect, or user is not registered','error')
            return  redirect('/login')
            
    return render_template('login.html')


@app.route('/single_user_all', methods =['POST','GET'])
def single_user_all():
    owner = User.query.filter_by(user_name= session['user_name']).first()

    blogs = Blog.query.filter_by (owner=owner).all()
    return render_template('all_blogs.html',title="Your Blog Posts!",
     blogs=blogs)


@app.route('/single_user', methods =['POST','GET'])
def display_blogs():
   owner = User.query.filter_by(user_name= session['user_name']).first()
   blog_id =request.args.get('id') 
   if (blog_id):
      blog=Blog.query.get(blog_id)
      return render_template('single_user.html', title="Blog Title", blog= blog) 
   else:
        all_blogs = Blog.query.all() 

        return render_template('single_user_all.html', title="All Blogs", all_blogs=all_blogs)


@app.route('/new_blog', methods =['POST','GET'])
def new_blog():
    owner = User.query.filter_by(user_name= session['user_name']).first()

    if request.method == 'POST':
        new_title = request.form ['title'] 
        new_body = request.form ['body']
        new_post = Blog(new_title, new_body)

        if new_post .is_valid():
            db.session.add(new_post)
            db.session.commit()
            return redirect('/single_user_all')
        else:
            flash("Please check your entry for errors or missing fields. Both title and body are required")
            return render_template('new_blog.html', title = "Create new blog entry", new_blog_title = new_blog_title,
                   new_blog_body = new_blog_body)
    else:
        return render_template('new_blog.html', title= "Create new blog")
            

    #if request.method == 'POST':
       # blog_name = request.form['new_blog']   
       # new_blog =Blog(blog_name,owner)
       # db.session.add(new_blog)
       # db.session.commit()
        #return redirect ('/single_user_all')

@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    blog_id = int(request.form['blog_id'])
    blog= Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()
    
    return redirect('/single_user_all')

@app.route('/logout')
def logout():
    del session['user_name']
    return redirect('/login')


@app.route('/')
def index():
    
    return redirect('/blog')

if __name__ == '__main__':
    app.run()