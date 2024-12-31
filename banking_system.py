from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# User data stored in a file
user_data_file = "users.txt"

# Utility functions
def load_users():
    if not os.path.exists(user_data_file):
        return {}
    with open(user_data_file, "r") as file:
        users = {}
        for line in file:
            username, password, balance = line.strip().split(',')
            users[username] = {"password": password, "balance": int(balance)}
        return users

def save_users(users):
    with open(user_data_file, "w") as file:
        for username, data in users.items():
            file.write(f"{username},{data['password']},{data['balance']}\n")

users = load_users()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard', username=username))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if username in users:
            flash('Username already exists.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            users[username] = {"password": password, "balance": 0}
            save_users(users)
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('create.html')

@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    if username not in users:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))

    user = users[username]
    if request.method == 'POST':
        amount = int(request.form['amount'])
        if 'deposit' in request.form:
            user['balance'] += amount
            flash(f'Successfully deposited ₹{amount}.', 'success')
        elif 'withdraw' in request.form:
            if amount > user['balance']:
                flash('Insufficient balance.', 'danger')
            else:
                user['balance'] -= amount
                flash(f'Successfully withdrew ₹{amount}.', 'success')
        save_users(users)
    return render_template('dashboard.html', username=username, balance=user['balance'])

@app.route('/support')
def support():
    faqs = [
        {"question": "How can I check my account balance?", "answer": "Log in and view your dashboard."},
        {"question": "How do I reset my password?", "answer": "Contact our customer support."},
        {"question": "What are the bank's working hours?", "answer": "9 AM to 5 PM, Monday to Friday."}
    ]
    return render_template('support.html', faqs=faqs)

if __name__ == '__main__':
    app.run(debug=True)
