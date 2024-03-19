from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
#import json
#import os
import pyodbc

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/account_user')
def account_user():
    return render_template('account/account_user.html')