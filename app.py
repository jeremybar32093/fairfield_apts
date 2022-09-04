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
from config import mail_username, mail_password, postgres_secret_key, postgres_un, contact_email

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# ***** CREATE DATABASE FOR STORING RATES/APT TYPES/TENANT INFO/ETC ****+*
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/fairfield_apt"
# Secret Key for being able to post back to database
app.config["SECRET_KEY"] = postgres_secret_key
# SMTP Mail Server - outlook
app.config["MAIL_SERVER"] = "smtp-mail.outlook.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = mail_username
app.config["MAIL_PASSWORD"] = mail_password
# app.config["MAIL_SUPPRESS_SEND"] = False

# Create db object
db = SQLAlchemy(app)
# Create admin page object
admin = Admin(app)
# Create mail object
mail = Mail(app)

#################################################
# Database tables via classes
#################################################
class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class Listings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    unit_number = db.Column(db.String(255))
    floor_number = db.Column(db.String(255))
    bedrooms = db.Column(db.String(255))
    bathrooms = db.Column(db.String(255))
    square_footage = db.Column(db.String(255))
    available_date = db.Column(db.Date)
    monthly_rent = db.Column(db.String(255))
    min_credit_score = db.Column(db.String(255))
    pets_allowed = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
# admin view that contains login 
class SecureModelView(ModelView):
    # Override is_accesible method - within module, simply returns true by default
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'notes': CKTextAreaField
    }

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
         

# Model View for posts class
admin.add_view(SecureModelView(Listings, db.session))


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
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        email_body = f"Name: {name}\nE-mail: {email}\nPhone: {phone}\n\n\n{message}"

        msg = Message(subject=f"Mail from {name}", body=email_body, sender=mail_username, recipients=[contact_email])
        mail.send(msg)
        print(name)
        return render_template("contact.html", success=True)

    return render_template("contact.html")

# Forms page route
@app.route("/forms")
def forms():
    return render_template("forms.html")

# Rentals page route
@app.route("/rentals")
def rentals():
    # List all posts on homepage list
    listings = Listings.query.order_by(Listings.available_date.desc())
    return render_template("rentals.html", listings=listings)

# Virtual tour page route
@app.route("/virtual-tour")
def virtual_tour():
    return render_template("virtual_tour.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Right now, handles only 1 user (admin user)
        # ***** FUTURE ENHANCEMENT - ADD ABILITY FOR MULTIPLE USER SIGNUP *****
        if request.form.get("username") == postgres_un and request.form.get("password") == postgres_secret_key:
            session['logged_in'] = True
            return redirect("/admin")
        else:
            return render_template("login.html", failed=True)
    return render_template("login.html")

# Logout page
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


#################################################
# Run flask app
#################################################
if __name__ == '__main__':
    app.run(debug=True)