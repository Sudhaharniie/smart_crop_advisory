from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    farm_size = request.form.get('farm_size', 0)
    location = request.form.get('location', '')
    phone = request.form.get('phone', '')
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists')
        return redirect(url_for('auth.login'))
    
    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        farm_size=float(farm_size) if farm_size else 0,
        location=location,
        phone=phone
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    session['user_id'] = new_user.id
    session['username'] = new_user.username
    return redirect(url_for('dashboard.dashboard'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
