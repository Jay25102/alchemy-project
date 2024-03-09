"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "somekey"
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

""""routes"""

@app.route("/")
def root():
    """currently redirects to all_users page"""
    return redirect("/users")

@app.route("/users")
def all_users():
    """shows a list of all users"""
    users = User.query.all()
    return render_template("all_users.html", users=users)

@app.route("/users/new")
def new_user_form():
    """returns a form to add new users"""
    return render_template("new_user.html")

@app.route("/users/new", methods=["POST"])
def create_new_user():
    """adds a new user to db based on form"""
    print(request.form['first_name'])
    new_user = User(first_name=request.form['first_name'],
                    last_name=request.form['last_name'],
                    image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    """shows user details page"""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def user_edit_form(user_id):
    """return a form for the user to edit their details"""
    user = User.query.get(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_edit_details(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")