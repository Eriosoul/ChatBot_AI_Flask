from flask import Blueprint, render_template, session, flash, redirect, url_for
from db.connection_db import DataBaseConnection
from .auth import login_required
from db.queries import GetAllhotels

hotels_bp = Blueprint('hotels', __name__)

@hotels_bp.route('/home')
@login_required
def hotels():
    try:
        g = GetAllhotels()
        print(g)
    except Exception as ex:
        print(ex)

    return render_template('hotels.html')