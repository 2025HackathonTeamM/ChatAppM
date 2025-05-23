from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import hashlib
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DB接続用の関数（毎回呼び出す）
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_DATABASE"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # ← 辞書型で返してくれる！
    )
@app.route('/')
def home():
    return "Flask is working!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_name=%s AND password=%s"
            cursor.execute(sql, (user_name, hashed_password))
            user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user['user_name']
            session['uid'] = user['uid']
            print("ログイン成功:", session)
            return redirect(url_for('chat'))
        else:
            flash("Invalid email or password")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.')
            return render_template('signup.html')

        # パスワードをハッシュ化！
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # データベースに登録
        conn = get_db_connection()
        with conn.cursor() as cursor:
            user_id = str(uuid.uuid4())
            sql = "INSERT INTO users (uid, user_name, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_id, user_name, hashed_password))
            conn.commit()
        conn.close()

        flash('Account created! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    uid = session.get('uid')
    print("セッション情報:", session)
    if 'username' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        message = request.form['message']
        if message.strip():
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO messages (message, user_id) VALUES (%s, %s)"
                cursor.execute(sql, (message, session['uid']))
                conn.commit()
            conn.close()
            return redirect(url_for('chat'))

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT m.id, m.message, m.user_id, u.user_name
            FROM messages m
            JOIN users u ON m.user_id = u.uid
            ORDER BY m.created_at ASC
        """)
        messages = cursor.fetchall()
    conn.close()

    return render_template('messages.html', messages=messages, user_name=session['username'], uid=uid)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    uid = session.get('uid')

    if uid is None:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        sql = "DELETE FROM messages WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (message_id, uid))
        conn.commit()
    conn.close()

    return redirect(url_for('chat'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
