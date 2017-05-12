from flask import Flask

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='you-will-never-guess'
)

from app import views