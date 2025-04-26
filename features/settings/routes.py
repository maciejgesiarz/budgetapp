import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/appearance')
def appearance():
    return render_template('settings/appearance.html')

@settings_bp.route('/categories', methods=['GET', 'POST'])
def categories():
    # 1) Otwórz połączenie i utwórz kursor
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()

    # 2) Obsługa POST — dodanie nowej kategorii
    if request.method == 'POST':
        new_cat = request.form.get('new_category')
        if new_cat:
            try:
                cursor.execute(
                    'INSERT INTO categories (name) VALUES (?)',
                    (new_cat,)
                )
                conn.commit()
            except sqlite3.IntegrityError:
                # ignoruj duplikaty
                pass
        # zamknij połączenie przed redirectem
        conn.close()
        return redirect(url_for('settings.categories'))

    # 3) SELECT wszystkich kategorii
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()

    # 4) Zamknij połączenie i renderuj szablon
    conn.close()
    return render_template(
        'settings/categories.html',
        categories=categories
    )
