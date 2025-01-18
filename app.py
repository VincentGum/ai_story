from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Feedback
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",
)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered'})

    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({'status': 'success'})

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/story-generator', methods=['GET', 'POST'])
@login_required
def story_generator():
    if request.method == 'POST':
        character_type = request.form.get('character_type')
        story_length = request.form.get('story_length')
        story_theme = request.form.get('story_theme')

        # Temporary story generation (placeholder for OpenAI API)
        story = f"This is a {story_length} story about a {character_type}, themed around {story_theme}..."
        images = []  # Placeholder for image generation
        
        return render_template('story.html', story=story, images=images)
    
    return render_template('generator.html')

@app.route('/feedback', methods=['POST'])
@login_required
def submit_feedback():
    content = request.form.get('content')
    if content:
        feedback = Feedback(content=content, user_id=current_user.id)
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
    return redirect(url_for('home'))

@app.route('/admin/feedback')
@login_required
def view_feedback():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('admin/feedback.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True) 