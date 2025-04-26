from flask import Blueprint, render_template

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/appearance')
def appearance():
    return render_template('settings/appearance.html')

@settings_bp.route('/categories')
def settings_categories():
    # … dotychczasowa logika …
    return render_template('settings/categories.html')
