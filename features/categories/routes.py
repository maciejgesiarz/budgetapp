from flask import Blueprint, render_template, request, redirect
from extensions import get_db

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('', methods=['GET', 'POST'])
def list_categories():
    # … logika …
    return render_template('categories/index.html', ...)
