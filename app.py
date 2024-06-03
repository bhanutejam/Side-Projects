import os
import psycopg2
import flask
from dotenv import load_dotenv
from flask import request,flash,render_template,redirect,url_for
from datetime import datetime
import secrets

CREATE_TASKS=("CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, task text, date TIMESTAMP, ach boolean);")
INSERT_TASK="INSERT INTO tasks (task,ach,date) VALUES (%s,%s,%s) RETURNING id;"
VIEW_ACHIEVEMENTS=("SELECT * FROM tasks WHERE ach=true;")
VIEW_TASKS=("SELECT * FROM tasks;")


load_dotenv()
url=os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

app = flask.Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def home():
    return flask.render_template("index.html")
@app.route('/addtasks')
def add():
    return flask.render_template("addtasks.html")


@app.route('/submit', methods=['POST'])
def submit():
    task=request.form['task']
    ach=request.form['ach']
    date=request.form['date']
    try:
        date = datetime.strptime(date, '%Y-%M-%d')
        flash('Your details have been submitted successfully!', 'success')
    except KeyError:
        date = datetime.now(timezone.ist)
        flash('Your details have been submitted successfully! with'+ date, 'success')

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TASKS)
            cursor.execute(INSERT_TASK,(task,ach,date))
    return render_template('submit.html')

@app.route('/achievements')
def view_ach():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(VIEW_ACHIEVEMENTS)
            rows=cursor.fetchall()
    return render_template('achievements.html', tasks=rows)
@app.route('/tasks')
def view_tasks():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(VIEW_TASKS)
            rows=cursor.fetchall()
    return render_template('tasks.html', tasks=rows)

@app.route('/handle_task_decision')
def handle_task_decision():
   
    add_task = request.args.get('newtask')
    print(add_task)
    if add_task == 'true':
        return flask.render_template("addtasks.html")
    else:
        return flask.render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)