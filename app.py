#################################################
# Flask Setup
#################################################
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    abort,
    session)
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlalchemy
from flask_mail import Mail, Message
# from config import mail_username, mail_password
from wtforms import TextAreaField
from wtforms.widgets import TextArea

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# ***** CREATE DATABASE FOR STORING RATES/APT TYPES/TENANT INFO/ETC ****+*
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/medicine_without"
# # Secret Key for being able to post back to database
# app.config["SECRET_KEY"] = "$MedicineWithout2021$"
# # SMTP Mail Server - outlook
# app.config["MAIL_SERVER"] = "smtp-mail.outlook.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USE_SSL"] = False
# app.config["MAIL_USERNAME"] = mail_username
# app.config["MAIL_PASSWORD"] = mail_password
# # app.config["MAIL_SUPPRESS_SEND"] = False

# # Create db object
# db = SQLAlchemy(app)
# # Create admin page object
# admin = Admin(app)
# # Create mail object
# mail = Mail(app)

#################################################
# Database tables via classes
#################################################
# class CKTextAreaWidget(TextArea):
#     def __call__(self, field, **kwargs):
#         if kwargs.get('class'):
#             kwargs['class'] += ' ckeditor'
#         else:
#             kwargs.setdefault('class', 'ckeditor')
#         return super(CKTextAreaWidget, self).__call__(field, **kwargs)

# class CKTextAreaField(TextAreaField):
#     widget = CKTextAreaWidget()

# class Posts(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(255))
#     subtitle = db.Column(db.String(255))
#     category = db.Column(db.String(255))
#     subcategory = db.Column(db.String(255))
#     content = db.Column(db.Text)
#     author = db.Column(db.String(255))
#     date_posted = db.Column(db.DateTime)
#     slug = db.Column(db.String(255))

# # admin view that contains login 
# class SecureModelView(ModelView):
#     # Override is_accesible method - within module, simply returns true by default
#     def is_accessible(self):
#         if "logged_in" in session:
#             return True
#         else:
#             abort(403)
#     extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

#     form_overrides = {
#         'content': CKTextAreaField
#     }

#     form_choices = {
#     'category': [
#         ('community_ed', 'Community Education'),
#         ('ems_disaster', 'EMS and Disaster'),
#         ('tactical_med', 'Tactical Medicine'),
#         ('wilderness_med', 'Wilderness Medicine')
#     ], 
#     'subcategory': [
#         ('no_subcategory', 'None'),
#         ('care_other', 'Care of Others'),
#         ('self_care', 'Self Care')
#     ]
#     }
         

# # Model View for posts class
# admin.add_view(SecureModelView(Posts, db.session))


#################################################
# Flask Routes
#################################################

# Homepage route
@app.route("/")
def homepage():
    return render_template("index.html")

# About page route
@app.route("/about")
def about():
    return render_template("about.html")

# Contact page route
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Forms page route
@app.route("/forms")
def forms():
    return render_template("contact.html")

# Rentals page route
@app.route("/rentals")
def rentals():
    return render_template("rentals.html")

# Virtual tour page route
@app.route("/virtual-tour")
def virtual_tour():
    return render_template("virtual_tour.html")


#################################################
# Run flask app
#################################################
if __name__ == '__main__':
    app.run(debug=True)