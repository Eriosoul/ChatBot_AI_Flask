from flask import Blueprint, render_template, request, flash, redirect, url_for
# from utils.decorators import login_required  # Asegúrate de importar tu decorador

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
# @login_required
def home():
    return render_template('home.html')