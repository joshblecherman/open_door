from flask import Flask, render_template, redirect, request, url_for
from od_utils import db

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home_page():
    db.test_db()
    if request.method == 'POST':
        if request.form.get('my_profile') == 'My Profile':
            return redirect(url_for('profile_page'))
        
        elif  request.form.get('student_events') == 'Student Events':
            return redirect(url_for('profile_page'))
        
        elif request.form.get('fun_spots') == 'Fun Spots':
            return redirect(url_for('profile_page'))
        
        elif request.form.get('happening_in_nyc') == 'Happening in NYC':
            return redirect(url_for('profile_page'))
    else:
        return render_template('home.html')

@app.route('/myprofile', methods=["GET", "POST"])
def profile_page():
    if request.method == 'POST':
        if request.form.get('my_profile') == 'My Profile':
            return redirect(url_for('home_page'))
        
        elif  request.form.get('student_events') == 'Student Events':
            return redirect(url_for('home_page'))
        
        elif request.form.get('fun_spots') == 'Fun Spots':
            return redirect(url_for('home_page'))
        
        elif request.form.get('happening_in_nyc') == 'Happening in NYC':
            return redirect(url_for('home_page'))
    else:
        return render_template('profile.html')


if __name__ == '__main__':
    app.run()
