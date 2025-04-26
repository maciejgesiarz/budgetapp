from flask import Blueprint, render_template, request, redirect
from extensions import get_db

transactions_bp = Blueprint('transactions', __name__, url_prefix='/')

@transactions_bp.route('', methods=['GET','POST'])
def index():
    # ...
    return render_template('transactions/index.html', ...)
