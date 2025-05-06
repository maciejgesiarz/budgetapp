# features/transactions/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from core.models import Transaction, Category

transactions_bp = Blueprint(
    'transactions',
    __name__,
    url_prefix='/transactions',
    template_folder='templates/transactions'
)

@transactions_bp.route('/')
@login_required
def index():
    # Pobierz wszystkie transakcje zalogowanego użytkownika, posortowane malejąco po dacie
    transactions = (
        Transaction.query
        .filter_by(user_id=current_user.id)
        .order_by(Transaction.date.desc())
        .all()
    )
    categories = Category.query.order_by(Category.name).all()
    return render_template('transactions/index.html', transactions=transactions, categories=categories)

@transactions_bp.route('/add', methods=['POST'])
@login_required
def add():
    # Pobranie danych z formularza
    try:
        amount = float(request.form.get('amount', 0))
    except ValueError:
        flash('Nieprawidłowa kwota.', 'warning')
        return redirect(url_for('transactions.index'))

    category_id = request.form.get('category_id')
    description = request.form.get('description', '').strip()
    date_str    = request.form.get('date', '').strip()  # format YYYY-MM-DD

    if not category_id:
        flash('Wybierz kategorię.', 'warning')
        return redirect(url_for('transactions.index'))

    txn = Transaction(
        amount=amount,
        category_id=int(category_id),
        user_id=current_user.id,
        description=description,
        date=date_str
    )
    db.session.add(txn)
    db.session.commit()
    flash('Dodano transakcję.', 'success')
    return redirect(url_for('transactions.index'))

@transactions_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    txn = Transaction.query.get_or_404(id)
    # Zabezpieczenie: tylko właściciel może usuwać
    if txn.user_id != current_user.id:
        flash('Brak uprawnień do usunięcia tej transakcji.', 'danger')
        return redirect(url_for('transactions.index'))
    db.session.delete(txn)
    db.session.commit()
    flash('Usunięto transakcję.', 'success')
    return redirect(url_for('transactions.index'))
