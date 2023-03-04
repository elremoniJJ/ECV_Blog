
# When working with python, the __init__ file is used when importing objects from folders
from flaskblog import create_app

app = create_app()

# __name__ refers to the module name.
# Allows command line to use 'python main.py' directly, instead of flask run
if __name__ == '__main__':
    app.run(debug=True)

