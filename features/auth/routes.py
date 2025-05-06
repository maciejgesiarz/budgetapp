# features/auth/routes.py

from flask     import Blueprint, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required
from extensions import oauth, db
from core.models import User, AllowedEmail

auth_bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/settings/auth',
    template_folder='templates/auth'
)

@auth_bp.route('/login')
def login():
    redirect_uri = url_for('auth.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize')
def authorize():
    token     = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    email     = user_info.get('email', '').lower()

    if not AllowedEmail.query.filter_by(email=email).first():
        flash('Ten adres nie jest uprawniony.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, pw_hash='')
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('transactions.index'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Wylogowano.', 'info')
    return redirect(url_for('auth.login'))
