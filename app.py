"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "somekey"
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

""""user routes"""

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

"""post routes"""

@app.route("/users/<int:user_id>/posts/new")
def new_user_post(user_id):
    """takes the user to a form to make a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """adds a new post from a user to the db"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['post_title'],
                    content=request.form['post_content'],
                    user_id=user.id)
    
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """shows a page with a blog post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("show_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    """deletes a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """returns a form for the user to edit a post"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template("edit_form.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=['POST'])
def handle_update_post(post_id):
    """handles form sumission for updating a post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['post_title']
    post.content = request.form['post_content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/users/{post.user_id}")

"""tag routes"""

@app.route("/tags")
def show_all_tags():
    tags = Tag.query.all()
    return render_template("all_tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_detail.html", tag=tag)

@app.route("/tags/new")
def new_tag():
    """returns form to add new tag"""
    return render_template("new_tag.html")

@app.route("/tags/new", methods=['POST'])
def create_new_tag():
    """adds a new tag to the db"""
    new_tag = Tag(name=request.form["tag_name"])
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """deletes a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """returns a form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """changes tag in db"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tag_name"]
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")
