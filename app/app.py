from flask import Flask, render_template
from od_utils import db

app = Flask(__name__)

@app.route('/')
def home_page():
<<<<<<< HEAD
    return render_template('home.html')
    # test_db()
    return render_template('home.html')
=======
    db.test_db()
    return render_template('home.html');
>>>>>>> a4f700ae3fd8acf37a76344778c29bf4bcd1129f

if __name__ == '__main__':
    app.run()
