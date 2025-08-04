from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect("waste.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS waste (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            weight REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect("waste.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM waste")
    data = cur.fetchall()
    conn.close()
    return render_template("index.html", waste_data=data)

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/submit', methods=['POST'])
def submit():
    waste_type = request.form['type']
    weight = request.form['weight']

    conn = sqlite3.connect("waste.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO waste (type, weight) VALUES (?, ?)", (waste_type, weight))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect("waste.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM waste WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return ('', 204)

@app.route('/refresh', methods=['POST'])
def refresh():
    conn = sqlite3.connect("waste.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM waste")
    conn.commit()
    conn.close()
    return ('', 204)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
