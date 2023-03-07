from sqlalchemy import and_
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user
from app import db
from app.utilities import logger as log
from app.utilities.helpers import save_picture
from app.models import Note, Category

# Set up Logging
loggy = log.get_logger(__name__)

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
@main.route("/home", methods=["GET"])
def home():
    context={}
    if current_user.is_authenticated:
        query = request.args.get("query", None) # here query will be the search inputs name
        filter_category = request.args.get("category", None) # here value will be the filter category id
        notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created.desc()).all()
        if query:
            notes = Note.query.filter(and_(Note.title.like("%"+query+"%"), Note.user_id == current_user.id))\
              .order_by(Note.created.desc()).all()
        if filter_category:
            notes = Note.query.filter(and_(Note.user_id == current_user.id, Note.category_id == int(filter_category)))\
              .order_by(Note.created.desc()).all()

        categories = Category.query.filter_by(user_id=current_user.id)
        context = {
            'notes':notes, 
            'categories':categories
            }
    return render_template("index.html", context=context)

@main.route("/add_category", methods=["POST"])
def add_category():
    form = request.form
    if current_user.is_authenticated:
        category_exist = Category.query.filter_by(
            title=form.get('category_title'), user_id = current_user.id).first()
        if  category_exist:
            flash("category exist with same title", "danger")
        # Add New category
        new_category = Category(
            title=form.get('category_title'), 
            user_id=current_user.id,
        )
        db.session.add(new_category)
        db.session.commit()
        flash("New category Added", "success")
    return redirect(url_for("main.home"))

@main.route("/edit_category", methods=["POST"])
def edit_category():
    form = request.form
    if current_user.is_authenticated:
        id = form['edited_category_id']
        category = Category.query.filter_by(id=int(id)).first()
        # Update category title
        if  category and form.get('edited_category_title'):
            category.title = form.get('edited_category_title')
            db.session.add(category)
            db.session.commit()
            flash("Category updated", "success")
        return redirect(url_for("main.home"))

@main.route("/delete_category", methods=["GET"])
def delete_category():
    id = request.args.get("query")
    if current_user.is_authenticated:
        category = Category.query.filter_by(id=id).first()
        if  category:
            db.session.delete(category)
            db.session.commit()
            flash("Category Deleted", "success")
        return redirect(url_for("main.home"))
    
@main.route("/add_note", methods=["POST"])
def add_note():
    form = request.form
    file = request.files
    if current_user.is_authenticated:
        image_path = None
        if file.get('note_image'):
            image_path = save_picture(file['note_image'])
        # Add New Note
        new_note = Note(
            title = form.get('note_title'),
            content = form.get('note_content'),
            category_id = form.get('note_category'),
            user_id=current_user.id,
            image = image_path
        )

        db.session.add(new_note)
        db.session.commit()
        flash("Note Added", "success")
        return redirect(url_for("main.home"))

@main.route("/edit_note", methods=["POST"])
def edit_note():
    form = request.form
    file = request.files
    if current_user.is_authenticated:
        image_path = None
        if file.get('note_image'):
            image_path = save_picture(file['note_image'])
        note = Note.query.filter_by(id=form.get('note_id')).first()
        if  note:
            note.title = form.get('note_title')
            note.content = form.get('note_content')
            note_category_id=form.get('note_category_id')
            if note_category_id and note_category_id != 'no_category':
                note.category_id = form.get('note_category_id')
            elif note_category_id == 'no_category':
                note.category_id = None
            if image_path:
                note.image = image_path
            db.session.add(note)
            db.session.commit()
            flash("Note Updated", "success")      
        return redirect(url_for("main.home"))

@main.route("/delete_note", methods=["GET"])
def delete_note():
    id = request.args.get("query")
    form = request.form
    if current_user.is_authenticated:
        note = Note.query.filter_by(id=id).first()
        if  note:
            db.session.delete(note)
            db.session.commit()
            flash("Note Deleted", "success")
        return redirect(url_for("main.home"))

@main.route("/remove_img_from_note", methods=["GET"])
def remove_img_from_note():
    id = request.args.get("noteId")
    if current_user.is_authenticated and id:
        note = Note.query.filter_by(id=int(id)).first()
        if  note:
            note.image = None
            db.session.add(note)
            db.session.commit()
            flash("Image Removed from note", "success")
        return redirect(url_for("main.home"))



