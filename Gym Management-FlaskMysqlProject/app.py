from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2457'
app.config['MYSQL_DB'] = 'gym'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/members')
def members():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM members")
    memberinfo = cur.fetchall()
    cur.close()
    return render_template('members.html', members=memberinfo)

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_results = []
    if request.method == "POST":
        search_term = request.form['memberid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM members WHERE id LIKE %s", ('%' + search_term + '%',))
        search_results = cur.fetchmany(size=1)
        cur.close()
        return render_template('members.html', members=search_results)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        memberid = request.form['memberid']
        name = request.form['name']
        plan = request.form['plan']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO members (id, name, plan, status) VALUES (%s, %s, %s, %s)", (memberid, name, plan, status))
        mysql.connection.commit()
        return redirect(url_for('members'))

@app.route('/delete/<string:memberid>', methods=['GET'])
def delete(memberid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM members WHERE id = %s", (memberid,))
    mysql.connection.commit()
    return redirect(url_for('members'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        memberid = request.form['memberid']
        name = request.form['name']
        plan = request.form['plan']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE members SET name = %s, plan = %s, status = %s WHERE id = %s", (name, plan, status, memberid))
        mysql.connection.commit()
        return redirect(url_for('members'))

if __name__ == "__main__":
    app.run(debug=True)
