from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)
app.config['DEBUG'] = True

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "testdb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres"),
        cursor_factory=RealDictCursor
    )
    return conn

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data.get("name")
        print("Incoming JSON:", data)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (name,))
        user_id = cur.fetchone()["id"]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"id": user_id, "name": name}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




