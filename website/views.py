from email.mime import image
from flask import Blueprint, render_template, session, request, redirect, flash, jsonify, url_for, current_app
from flask_login import login_required, current_user 
from sqlalchemy import inspect
from . import db 
import json
from .models import Note, MenuCategory, Menu
from .forms import AddToCart


# this is our blueprint, lots root and URL
views = Blueprint('views',__name__) # keep this the same as the python file for easier convention

@views.route('/', methods=['GET','POST'])
@login_required
def note():
    if request.method == 'POST':
        note = request.form.get('note')
        print(note)
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("note.html", user=current_user)    
@views.route("/about-us")
def about_us():
    return render_template("about-us.html")



@views.route('/menu')
def menu():
    menucategory = MenuCategory.query.all()
    menuitems = Menu.query.all()
    return render_template('menu.html', menucategory=menucategory,menuitems=menuitems, image_loc = current_app.config['UPLOAD_FOLDER'])


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/product/<id>')
# this is a function that directs you to view item detail after you clicked 'add to cart' button in menu page
def item(id):
    item = Menu.query.filter_by(id=id).first()

    form = AddToCart()

    return render_template('view-item.html', item=item, form=form)

@views.route('/add-to-cart', methods= ['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []
    
    form = AddToCart()

    if form.validate_on_submit():
        session['cart'].append(
            {'id': form.id.data, 'quantity': form.quantity.data}
        )
        session.modified = True
        flash('Item(s) added successfully', category='success')
    else:
        flash('Invalid selection, please add again.')
    
    return redirect(url_for('views.menu'))


def handle_cart():
    added_items_detail = []
    grand_total = 0
    index = 0
    quantity_total = 0
    tax_total = 0
    SF_TAX_RATE = float(0.0975)
    grand_total_plus_tax = 0
    for i in session['cart']:
        item = Menu.query.filter_by(id=i['id']).first()

        quantity = int(i['quantity'])
        total = quantity * item.price
        tax = SF_TAX_RATE * item.price * quantity
        added_items_detail.append({
            'id':item.id, 'item_name':item.item_name, 'item_name_cn': item.item_name_cn, 'price': item.price,\
                'image': item.image, 'quantity' : quantity, 'total' : total, 'index':index, 'tax':tax
        })
        index += 1
        grand_total += total
        quantity_total += quantity
        tax_total += tax
    grand_total_plus_tax += (grand_total + tax_total)


    return added_items_detail, grand_total, quantity_total, round(tax_total,2), round(grand_total_plus_tax,2), SF_TAX_RATE

@views.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    flash('Item deleted', category='success')
    return redirect(url_for('views.cart'))


@views.route('/cart', methods=['GET','POST'])
def cart():
    added_items_detail, grand_total, quantity_total, tax_total, grand_total_plus_tax, SF_TAX_RATE = handle_cart()
    return render_template('cart.html', items = added_items_detail, grand_total = grand_total, quantity_total = quantity_total, tax_total=tax_total, grand_total_plus_tax = grand_total_plus_tax, SF_TAX_RATE = SF_TAX_RATE)


@views.route('/checkout', methods=['GET','POST'])
def checkout():
    return render_template('checkout.html')