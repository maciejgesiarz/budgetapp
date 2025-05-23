# core/models.py

from datetime import datetime
from extensions import db
from flask_login import UserMixin

# Asocjacje many-to-many
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    pw_hash    = db.Column(db.String(128), nullable=False)
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    roles      = db.relationship('Role', secondary=user_roles, backref='users')

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def has_permission(self, perm_name):
        return any(
            perm.name == perm_name
            for role in self.roles
            for perm in role.permissions
        )

class Role(db.Model):
    __tablename__ = 'role'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    permissions = db.relationship('Permission', secondary=role_permissions, backref='roles')

class Permission(db.Model):
    __tablename__ = 'permission'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))

class AllowedEmail(db.Model):
    __tablename__ = 'allowed_email'
    id    = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'category'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # (opcjonalnie) relacje do transakcji, np. backref='category'

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id  = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount       = db.Column(db.Numeric(12, 2), nullable=False)
    description  = db.Column(db.String(255))
    date         = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # relacje (opcjonalne):
    user         = db.relationship('User', backref='transactions')
    category     = db.relationship('Category', backref='transactions')