from flask import Flask
from views import views
from dotenv import find_dotenv, load_dotenv
import os
from settings import FLASK_HOST, FLASK_PORT

# loading environment variables
load_dotenv(find_dotenv())


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.register_blueprint(views)

if __name__ == '__main__':
    app.run(debug=1, host=FLASK_HOST, port=FLASK_PORT)