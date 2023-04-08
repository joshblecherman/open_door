from flask import Flask, render_template, redirect, request, url_for
from od_utils import db

app = Flask(__name__)

def check_main_tabs():
    if request.form.get('my_profile') == 'My Profile':
        return 'profile_page'
        
    elif request.form.get('student_events') == 'Student Events':
        return 'student_events_page'
    
    elif request.form.get('fun_spots') == 'Fun Spots':
        return 'fun_spots_page'
    
    elif request.form.get('happening_in_nyc') == 'Happening in NYC':
        return 'happening_in_nyc_page'
    else:
        return False


@app.route('/', methods=["GET", "POST"])
def home_page():
    db.test_db()
    if request.method == 'POST':
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template('home.html')


@app.route('/myprofile', methods=["GET", "POST"])
def profile_page():
    if request.method == 'POST':
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template('profile.html')


@app.route('/studentevents', methods=["GET", "POST"])
def student_events_page():
    if request.method == 'POST':
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template('student_events.html')

@app.route('/funspots', methods=["GET", "POST"])
def fun_spots_page():
    if request.method == 'POST':
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template('fun_spots.html')
    
@app.route('/happeninginnyc', methods=["GET", "POST"])
def happening_in_nyc_page():
    if request.method == 'POST':
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template('happening_in_nyc.html')

if __name__ == '__main__':
    app.run()
