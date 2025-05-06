from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db
from core.models import Role
from . import auth_bp

@auth_bp.route('/roles')
@login_required
def list_roles():
    roles = Role.query.order_by(Role.name).all()
    return render_template('auth/roles.html', roles=roles)

@auth_bp.route('/roles/add', methods=['POST'])
@login_required
def add_role():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Podaj nazwę roli.', 'warning')
    elif Role.query.filter_by(name=name).first():
        flash('Taka rola już istnieje.', 'info')
    else:
        db.session.add(Role(name=name))
        db.session.commit()
        flash('Dodano rolę.', 'success')
    return redirect(url_for('auth.list_roles'))

@auth_bp.route('/roles/delete/<int:id>', methods=['POST'])
@login_required
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('Usunięto rolę.', 'success')
    return redirect(url_for('auth.list_roles'))
