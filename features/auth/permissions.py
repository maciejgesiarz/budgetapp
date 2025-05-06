from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from core.models import Permission
from . import auth_bp

@auth_bp.route('/permissions')
@login_required
def list_perms():
    perms = Permission.query.order_by(Permission.name).all()
    return render_template('auth/permissions.html', perms=perms)

@auth_bp.route('/permissions/add', methods=['POST'])
@login_required
def add_perm():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Podaj nazwę funkcjonalności.', 'warning')
    elif Permission.query.filter_by(name=name).first():
        flash('Taka funkcjonalność już istnieje.', 'info')
    else:
        db.session.add(Permission(name=name))
        db.session.commit()
        flash('Dodano funkcjonalność.', 'success')
    return redirect(url_for('auth.list_perms'))

@auth_bp.route('/permissions/delete/<int:id>', methods=['POST'])
@login_required
def delete_perm(id):
    perm = Permission.query.get_or_404(id)
    db.session.delete(perm)
    db.session.commit()
    flash('Usunięto funkcjonalność.', 'success')
    return redirect(url_for('auth.list_perms'))
