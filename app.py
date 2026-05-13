from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DATABASE
def init_db():

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount REAL,
            category TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route('/')
def index():

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()

    c.execute("SELECT SUM(amount) FROM expenses")
    total = c.fetchone()[0]

    conn.close()

    if total is None:
        total = 0

    return render_template(
        'index.html',
        expenses=expenses,
        total=total
    )

# ADD EXPENSE
@app.route('/add', methods=['POST'])
def add():

    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute(
        "INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
        (title, amount, category)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# DELETE EXPENSE
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True) 
