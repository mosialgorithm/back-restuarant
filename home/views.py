from flask import render_template, url_for, redirect
from . import home


@home.route('/')
def home_view():
    return render_template('home/home.html')

@home.route('/menu')
def menu_view():
    return render_template('home/menu.html')

@home.route('/cart')
def cart_view():
    return render_template('home/cart.html')

@home.route('/about-us')
def about_us_view():
    return render_template('home/about-us.html')

@home.route('/contact-us')
def contact_us_view():
    return render_template('home/contact-us.html')