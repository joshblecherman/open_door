from flask import Flask, render_template, redirect, request, url_for
from od_utils import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:opendoor@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        return render_template('profile.html', preferred_name="B42", major="Computer Science", 
                               dorm="Off-campus", full_name="Team B42", email="teamB42@teamB42.com",
                               phone="(097) 234-5678", about_me="We are just CS students trying to graduate")


@app.route('/studentevents', methods=["GET", "POST"])
def student_events_page():
    if request.method == 'POST':
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
        elif request.form.get('see_rsvp_list') == 'See RSVP List':
            return redirect(url_for('rsvp_list_page'))
    else:
        return render_template('student_events.html', num_events=5)

@app.route('/funspots', methods=["GET", "POST"])
def fun_spots_page():
    if request.method == 'POST':
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template('fun_spots.html', num_spots=4)
    
@app.route('/happeninginnyc', methods=["GET", "POST"])
def happening_in_nyc_page():
    if request.method == 'POST':
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template('happening_in_nyc.html')
    
@app.route('/rsvplist', methods=["GET", "POST"])
def rsvp_list_page():
    if request.method == 'POST':
        if request.form.get('Back') == 'Back':
            return redirect(url_for('student_events_page'))
    else:
        return render_template('rsvp_list.html', event_name = "The Hike", preferred_name="B42", major="Computer Science", 
                               dorm="Off-campus", full_name="Team B42", email="teamB42@teamB42.com",
                               phone="(097) 234-5678")

if __name__ == '__main__':
    db.db.init_app(app)
    app.run()
