from flask import Blueprint, render_template, request, flash, redirect, url_for

home_bp = Blueprint('home', __name__)


@home_bp.get("/home")
def home():
    return render_template('home.html')