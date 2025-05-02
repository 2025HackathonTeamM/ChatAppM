from flask import abort
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()

class User:
    @classmethod
    def create(cls, uid, name, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO  users (uid, user_name, password)VALUES (%s,%s,%s);"
                cur.execute(sql,(uid, name, password,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

class Message:
    @classmethod
    def create(cls, uid, message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages(uid, message) VALUES(%s,%s)"
            cur.execute(sql, (uid, message,))
            conn.commit()
        except pymysql.Error as e:
          print(f'エラーが発生しています：{e}')
          abort(500)
        finally:
            db_pool.release(conn)

@classmethod
def get_all(cls):
    conn = db_pool.get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT id, u.uid, user_name, message
                FROM messages AS m
                INNER JOIN users AS u ON m.uid = u.uid
                ORDER BY id ASC;
            """
            cur.execute(sql)
            messages = cur.fetchall()
            return messages
    except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
    finally:
        db_pool.release(conn)
