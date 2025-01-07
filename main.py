from flask import Flask
from views import blueprint
from dotenv import find_dotenv, load_dotenv
import os

# loading environment variables
load_dotenv(find_dotenv())


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=1, port=5001)