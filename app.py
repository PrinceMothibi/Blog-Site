from crypt import methods
from datetime import datetime
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer ,primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String(5000))

    def __repr__(self):
        return '<Blog %r>' %self.id

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        task_title = request.form['title']
        blog_content=' '
        blogs = Todo(title=task_title,content=blog_content)
        try:
            db.session.add(blogs)
            db.session.commit()
            id=blogs.id
            return redirect(f'/newblog/{id}/')
        except:
            return 'there was an error creating your blog'
        
        # 'redirect to blogpost page, correlates with the Todo.id'
    else:
        blogs = Todo.query.order_by(Todo.date_posted).all()
        return render_template('home.html', blogs=blogs)

@app.route('/newblog/<int:id>/', methods=["GET","POST"])
def new_blog(id):
    # render_template('newblog.html')
    blog=Todo.query.get_or_404(id)

    if request.method=='POST':
        blog.content=request.form['blog_content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue uploading your blog'
    else:
        return render_template('newblog.html', blog=blog)

@app.route('/viewblog/<int:id>', methods=["GET","POST"])
def viewblog(id):

    blog = Todo.query.get_or_404(id)
    return render_template("blogpost.html",blog=blog)
    
@app.route('/delete/<int:id>')
def delete(id):
    blog_to_delete=Todo.query.get_or_404(id)

    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

if __name__ == '__main__':
    app.run(debug=True)
