from flask import Flask, render_template, redirect, url_for, flash
# from flask_jsglue import JSGlue
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import Development
from flask_login import LoginManager


#
# jsglue = JSGlue()

app = Flask(__name__)

# jsglue = JSGlue(app)

app.config.from_object(Development)

# jsglue.init_app(app)


# ----------------------------- CONFIGS_OF_LOGIN_MANAGER -----------------------
login = LoginManager()
login.login_view = 'auth.login_view'
login.login_message_category = 'info'
login.init_app(app)
# --------------------------------------------------------------------------------


CORS(app)

db = SQLAlchemy(app)

ma = Marshmallow(app)

# migrate = Migrate(app, db, compare_type=True)
migrate = Migrate(app, db)




# @app.route("/")
# def index():
#     return render_template('home/home.html')

@app.route('/result')
def result():
    return "hello world"



# .................... Bluepriont Config ........................................
from home import home
from auth import auth
from admin import admin




app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(admin)
# .................... End of Bluepriont Config ..................................


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



# ....................... login user handler ................................
from auth.models import UserModel

@login.user_loader
def userLoader(user_id):
    return UserModel.query.get(user_id)

@login.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login_view'))

# ...........................................................................


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run()