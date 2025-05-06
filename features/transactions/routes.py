# features/categories/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from core.models import Category

categories_bp = Blueprint(
    'categories',
    __name__,
    url_prefix='/categories',
    template_folder='templates/categories'
)

@categories_bp.route('/')
@login_required
def index():
    categories = Category.query.order_by(Category.name).all()
    return render_template('categories/index.html', categories=categories)

@categories_bp.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Podaj nazwę kategorii.', 'warning')
    elif Category.query.filter_by(name=name).first():
        flash('Taka kategoria już istnieje.', 'info')
    else:
        db.session.add(Category(name=name))
        db.session.commit()
        flash('Dodano kategorię.', 'success')
    return redirect(url_for('categories.index'))

@categories_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Usunięto kategorię.', 'success')
    return redirect(url_for('categories.index'))
