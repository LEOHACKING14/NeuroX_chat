
from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        with open('users.json', 'r') as f:
            users = json.load(f)
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect('/chat')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)
        else:
            users = {}
        if username in users:
            return "User already exists"
        users[username] = password
        with open('users.json', 'w') as f:
            json.dump(users, f)
        return redirect('/login')
    return render_template('signup.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/login')
    return render_template('chat.html', user=session['user'])

@app.route('/send', methods=['POST'])
def send():
    if 'user' in session:
        msg = request.form['message']
        user = session['user']
        with open('chatlog.txt', 'a') as f:
            f.write(f"{user}: {msg}\n")
    return redirect('/chat')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Render देता है PORT env variable
    app.run(host="0.0.0.0", port=port)
