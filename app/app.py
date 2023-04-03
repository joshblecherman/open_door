from flask import Flask, render_template
from od_utils import db

app = Flask(__name__)

@app.route('/')
def home_page():
    db.test_db()
    return render_template('home.html');

if __name__ == '__main__':
    app.run()
