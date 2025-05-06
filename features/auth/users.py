from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from core.models import AllowedEmail
from . import auth_bp

@auth_bp.route('/users')
@login_required
def list_users():
    emails = AllowedEmail.query.order_by(AllowedEmail.created_at.desc()).all()
    return render_template('auth/users.html', emails=emails)

@auth_bp.route('/users/add', methods=['POST'])
@login_required
def add_user():
    email = request.form.get('email', '').strip().lower()
    if not email:
        flash('Podaj email.', 'warning')
    elif AllowedEmail.query.filter_by(email=email).first():
        flash('Ten email już jest na liście.', 'info')
    else:
        db.session.add(AllowedEmail(email=email))
        db.session.commit()
        flash('Dodano email.', 'success')
    return redirect(url_for('auth.list_users'))

@auth_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    entry = AllowedEmail.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Usunięto email.', 'success')
    return redirect(url_for('auth.list_users'))
