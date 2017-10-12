from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogger@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)




class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body





@app.route('/blog')


def index():
    blog_id = request.args.get('id')
    if not blog_id:
        blogs = Blog.query.all()
        return render_template('the_blog.html',blogs=blogs)
    else:
        the_entry = Blog.query.get(blog_id)
        #the_blog = Blog.blog_id
        b_title = the_entry.title
        b_body = the_entry.body
        #return render_template('entry.html')
        return render_template('entry.html', entry=the_entry)




@app.route('/newpost')
def add_index():
    template = jinja_env.get_template('add.html')
    return template.render(failed_title='', title_error='', failed_body='', body_error='')

    
    #return render_template('add.html')
@app.route('/newpost', methods=['POST'])
def add_blog():
    blog_title = request.form['blog']
    blog_body = request.form['stuff']
    
    title_error=''
    
    body_error=''
    
    if not blog_title:
        title_error='Please enter a blog title!'
    if not blog_body:
        body_error='Please enter a blog body!'
    if not title_error and not body_error:
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        #blogs = Blog.query.all()
        new_id = new_blog.id
        the_new = Blog.query.get(new_id)
        return render_template('entry.html', entry=the_new)
        #return redirect('/blog?id={0}').format('new_id')

        #return render_template('the_blog.html',blogs=blogs)
        #return redirect('/blog')
    else:
        template = jinja_env.get_template('add.html')
        return template.render(failed_title=blog_title, title_error=title_error, failed_body=blog_body, body_error=body_error)



if __name__ == '__main__':
    app.run()
