from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql

app = Flask(__name__)
app.secret_key ='your_secret_key'

# DB接続用関数
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='youruser',
        password='yourpassword',
        db='chatapp',
        charset='utf8mb4',
        #　辞書型で返してくれる
        cursorclass=pymysql.cursors.DictCursor
    )

#ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
# データベースに電話して、この人いる？と聞く
        conn = get_db_connection()
# cursorはデータベースにアクセスする際のメモ用のペンみたいなもの
        with conn.cursor() as cursor:
# usersテーブルから、このユーザー名とパスワードの人を抽出して
            sql = "SELECT * FROM users WHERE user_name=%s AND password=%s"
            cursor.execute(sql, (username, password))
            user = cursor.fetchone()
#　データベースへの電話を終了する
        conn.close()
#　もしユーザーが見つかっていたら
        if user:
# ログインユーザーのuidと名前を保存            
            session['user_id'] = user['uid']
            session['username'] = user['user_name']
# チャット画面にリダイレクトする
            return redirect(url_for('chat'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')