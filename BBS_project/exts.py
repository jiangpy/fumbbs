#! /usr/bin/env python
# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import config

app = Flask('BBS_project')

app.config.from_object(config)
mail = Mail(app)

db = SQLAlchemy(app)
