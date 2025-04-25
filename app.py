import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "🎉 Hello from your Docker-powered Flask app!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=55000)