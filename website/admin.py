
from flask import Blueprint, render_template, request, redirect, flash, current_app ,url_for
from flask_login import login_required, current_user 
from sqlalchemy import inspect
from . import db
import os
from .models import MenuCategory, Menu, Order
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['jpeg','jpg','png','gif','JPEG','JPG','PNG','GIF'])

admin = Blueprint('admin',__name__)

@admin.route('/manage-category', methods=['POST','GET'])
def change_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        category_name_cn = request.form.get('category_name_cn')
        rec = MenuCategory.query.filter_by(category=category_name).first()
        if 'ADD' in request.form:
            if rec:
                flash('this category already exist, please add a new one')
            elif not category_name or not category_name_cn:
                flash('Please fill in both category fields', category='error')
            else:
                new_category = MenuCategory(category=category_name,category_cn=category_name_cn)
                db.session.add(new_category)
                db.session.commit()
                flash('Category added successfully', category='success')
            
        elif 'DELETE' in request.form:

            if not category_name:
                flash('Please fill in category name to delete', category='error')
            elif not rec:
                flash('The category is not in the database, please try again', category='error')
            else:
                db.session.delete(rec)
                db.session.commit()
                flash(f'Category "{rec.category}" has been deleted successfully', category='success')

    menucategory= MenuCategory.query.all()
    return render_template('manage_category.html', menucategory=menucategory)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_image(image):
    # return value: imagename -> success | 2-> error: file existed | 3-> error: file not supported
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            imagename = filename
            print('first if')
            return imagename
        else:
            print('first else')
            return '2'
        
    return '3'

@admin.route('/manage-menu', methods=['POST','GET'])
def manage_menu():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_name_cn = request.form.get('item_name_cn')
        price = request.form.get('price')
        description = request.form.get('description')
        
        categoryID = request.form.get('categoryID')
        image = request.files['image']


        rec = Menu.query.filter_by(item_name=item_name).first()
        process_image_res = process_image(image)
        if 'ADD' in request.form:
            if rec:
                flash('This item already exist, please add a new one', category='error')
            elif not (item_name and item_name_cn and price and categoryID):
                flash('Please fill in all fields', category='error')
            elif process_image_res == '3':
                flash('We cannot process this image. Supported format: jpeg, jpg,png,gif', category='error')
            elif process_image_res == '2':
                flash('We cannot process this image. Already existed in database', category='error')
            else:
                imagename = process_image_res
                new_menu = Menu(item_name=item_name,item_name_cn=item_name_cn,price=price,\
                    description=description,image=imagename,categoryID=categoryID)
                db.session.add(new_menu)
                db.session.commit()
                flash('Menu added successfully', category='success')

        elif 'DELETE' in request.form:
            
            if not item_name:
                flash('Please fill in item name to delete', category='error')
            elif not rec:
                flash('The menu item is not in the database, please try again', category='error')
            else:
                db.session.delete(rec)
                db.session.commit()
                flash(f'Category "{rec.item_name}" has been deleted successfully', category='success')


    menucategory = MenuCategory.query.all()
    menuitems = Menu.query.all()

    return render_template('manage_menu.html', menucategory=menucategory,menuitems=menuitems)

@admin.route('/manage-order')
def manage_order():
    orders = Order.query.all()
    return render_template('manage_order.html', orders=orders)
