import os
import time

import mysql.connector
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "apppass"),
    "database": os.getenv("DB_NAME", "praktikum"),
}


def get_conn(retries=15, delay=2):
    """Koneksi ke MySQL, dengan retry karena DB bisa lebih lambat siap."""
    last_err = None
    for _ in range(retries):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as err:
            last_err = err
            time.sleep(delay)
    raise last_err


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


PAGE = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Simple App - Flask + MySQL</title>
  <style>
    body { font-family: sans-serif; max-width: 640px; margin: 40px auto; padding: 0 16px; }
    input[type=text] { width: 70%; padding: 6px; }
    button { padding: 6px 12px; }
    li { margin: 6px 0; }
    small { color: #666; }
  </style>
</head>
<body>
  <h1>Halo dari Flask + Docker + Jenkins!</h1>
  <p>Data di bawah disimpan di database MySQL.</p>
  <form method="post" action="{{ url_for('add') }}">
    <input type="text" name="content" placeholder="Tulis catatan..." required maxlength="255">
    <button type="submit">Simpan</button>
  </form>
  <ul>
    {% for n in notes %}
      <li>{{ n[1] }} <small>({{ n[2] }})</small></li>
    {% else %}
      <li><em>Belum ada catatan.</em></li>
    {% endfor %}
  </ul>
</body>
</html>
"""


@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(PAGE, notes=notes)


@app.route("/add", methods=["POST"])
def add():
    content = request.form.get("content", "").strip()
    if content:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for("index"))


@app.route("/health")
def health():
    """Dipakai Jenkins untuk memastikan app + database sama-sama hidup."""
    try:
        conn = get_conn(retries=1, delay=0)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        return {"status": "ok", "database": "connected"}, 200
    except mysql.connector.Error as err:
        return {"status": "error", "database": str(err)}, 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
