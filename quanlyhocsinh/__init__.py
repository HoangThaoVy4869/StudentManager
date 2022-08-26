from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from flask_mail import Mail
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)
app.secret_key = '$%^DFGHTYUIUY#$%^&*)(*&^%$%^&*(*&DFGHNMGHJ(*&^'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:01257604435@localhost/qlhs?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'demoemail12345678910@gmail.com'
app.config['MAIL_PASSWORD'] = 'demoweb@4869'

mail = Mail(app)

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name='ou',
    api_key='551542926151973',
    api_secret='XJv0gKx6WUIC_jmcfhjxKqO1GG0'
)

login = LoginManager(app=app)
