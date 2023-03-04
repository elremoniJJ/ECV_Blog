from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)



# Routes are what we type into our browser, to find specific pages
# Routes take us to specific information
# URL: Uniform Resource Location
# The "/" is the root page of a website


# The @ symbol is a decorator. It is a way to add more functionality to an existing function
# @app.route = additional functionality, e.g. auto-called, and directed to webbrowser
# def hello_world() is the base function
@main.route("/")
@main.route("/home")     # Using a 2nd route for the same page
def home():
    try:
        #  request.args.get('page', 1) refers to the ?page=1 in the browser url
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    except:
        posts = ""
    return render_template('home.html', posts=posts, title='Hanoi')



# The 'about page' route
@main.route("/about")
def about():
    return render_template('about.html', title='About')

