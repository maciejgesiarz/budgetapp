from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Inicjalizacja bazy danych
def init_db():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    conn.commit()
    conn.close()

# Uruchamiamy inicjalizację przy starcie aplikacji
init_db()

# Strona główna z listą transakcji
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        date = request.form['date']
        category = request.form['category']
        cursor.execute('INSERT INTO transactions (name, amount, date, category) VALUES (?, ?, ?, ?)',
                       (name, amount, date, category))
        conn.commit()

    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    cursor.execute('SELECT name FROM categories')
    categories = [row[0] for row in cursor.fetchall()]

    conn.close()
    return render_template('index.html', transactions=transactions, categories=categories)

# Strona kategorii
@app.route('/categories', methods=['GET', 'POST'])
def categories():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        new_category = request.form.get('new_category')
        if new_category:
            try:
                cursor.execute('INSERT INTO categories (name) VALUES (?)', (new_category,))
                conn.commit()
            except sqlite3.IntegrityError:
                pass  # ignorujemy duplikaty

    cursor.execute('SELECT * FROM categories')
    all_categories = cursor.fetchall()

    conn.close()
    return render_template('categories.html', categories=all_categories)

@app.route('/update_category/<int:transaction_id>', methods=['POST'])
def update_category(transaction_id):
    new_category = request.form.get('category')
    if new_category:
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE transactions SET category = ? WHERE id = ?', (new_category, transaction_id))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/settings/appearance')
def settings_appearance():
    return render_template('settings_appearance.html')

@app.route('/settings/categories')
def settings_categories():
    # Załaduj kategorie jak wcześniej
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    return render_template('settings_categories.html', categories=categories)
    
if __name__ == '__main__':
    app.run(debug=True)
