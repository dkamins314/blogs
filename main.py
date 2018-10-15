from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app= Flask (__name__)
app.config['DEBUG']= True
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://Build-a-Blog:bsiyatadishmaya@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='56ka52dh10WQOPHT$%$%$'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))


    def __init__(self, title, body):
        self.title = title
        self.body= body
        
    def is_valid(self):
        if self.title and self.body:
            return True
        else:
             return False

@app.route('/')
def index():
    
    return redirect('/blog')

      

@app.route('/blog', methods=['POST','GET'])
def display_blogs():
   blog_id =request.args.get('id') 
   if (blog_id):
      blog=Blog.query.get(blog_id)
      return render_template('single_blog.html', title="Blog Title", blog= blog) 
   else:
        all_blogs = Blog.query.all() 

        return render_template('all_blogs.html', title="All Blogs", all_blogs=all_blogs)
  
@app.route('/new_blog', methods=['Post', 'GET'] )
def new_blog_entry():
    if request.method == 'POST':
        new_title = request.form ['title'] 
        new_body = request.form ['body']
        new_post = Blog(new_title, new_body)

        if new_post .is_valid():
            db.session.add(new_post)
            db.session.commit()
            url= "/blog?id="+str(new_post.id)
            return redirect(url)
        else:
            flash("Please check your entry for errors or missing fields. Both title and body are required")
            return render_template('new_blog.html', title = "Create new blog entry", new_blog_title = new_blog_title,
                   new_blog_body = new_blog_body)
    else:
        return render_template('new_blog.html', title= "Create new blog")
            


if __name__ == '__main__':
    app.run()