from flask import Blueprint, render_template, request, redirect, url_for
from extensions import get_db

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name     = request.form['name']
        amount   = float(request.form['amount'])
        date     = request.form['date']
        category = request.form['category']
        cursor.execute(
            'INSERT INTO transactions (name, amount, date, category) VALUES (?, ?, ?, ?)',
            (name, amount, date, category)
        )
        db.commit()
        return redirect(url_for('transactions.index'))

    # pobierz dane
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    cursor.execute('SELECT name FROM categories')
    categories = [row[0] for row in cursor.fetchall()]

    # render: nazwa szablonu + named args
    return render_template(
        'transactions/index.html',
        transactions=transactions,
        categories=categories
    )
