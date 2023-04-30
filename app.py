from flask import render_template, redirect, request, url_for, flash
from od_app import app, db
import threading
from od_app.od_utils import db_utils
from od_app.od_utils.merging import activities_merge
import re

invalidEventFields = False
invalidSignUp = False
invalidLogin = False


def check_main_tabs():
    if request.form.get("my_profile") == "My Profile":
        return "profile_page"

    elif request.form.get("student_events") == "Student Events":
        return "student_events_page"

    elif request.form.get("fun_spots") == "Fun Spots":
        return "fun_spots_page"

    elif request.form.get("happening_in_nyc") == "Happening in NYC":
        return "happening_in_nyc_page"
    else:
        return False


@app.route("/", methods=["GET", "POST"])
def login_page():
    global invalidLogin
    if request.method == "POST":
        if request.form.get("Sign Up") == "Sign Up":
            return redirect(url_for("sign_up_page"))
        elif request.form.get("Login") == "Login":
            netid = request.form["netid"]
            password = request.form["password"]

            if (len(netid) == 0) or (len(password) == 0):
                invalidLogin = True
                return redirect(url_for("login_page"))

            token = db_utils.login(netid, password)

            if token == None:
                invalidLogin = True
                return redirect(url_for("login_page"))

            # Only after passing all the previous tests, the login is succesful

            return redirect(url_for("home_page"))

    else:
        if invalidLogin:
            flash("Please double check Net id or password")
            invalidLogin = False
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up_page():
    global invalidSignUp
    if request.method == "POST":
        if request.form.get("Login") == "Login":
            return redirect(url_for("login_page"))
        elif request.form.get("Sign Up") == "Sign Up":
            netid = request.form["netid"].lower()
            password = request.form["password"]
            repassword = request.form["repassword"]

            token = db_utils.login(netid, password)

            if (
                (password != repassword)
                or (len(password) == 0)
                or (len(repassword) == 0)
                or (len(netid) == 0)
                or (token != None)
            ):
                invalidSignUp = True
                return redirect(url_for("sign_up_page"))

            profile = {
                "net_id": netid,
                "first_name": "Please add your first name",
                "last_name": "Please add your last name",
            }

            newUser = {"net_id": netid, "password": password, "profile": netid}

            db_utils.add(db_utils.Profiles(**profile))
            db_utils.add(db_utils.Users(**newUser))
            return redirect(url_for("home_page"))

    else:
        if invalidSignUp:
            flash("Please double check Net id or password")
            invalidSignUp = False
        return render_template("sign_up.html")


@app.route("/home", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template("home.html")


@app.route("/myprofile", methods=["GET", "POST"])
def profile_page():
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
        elif request.form.get("Edit") == "Edit":
            return redirect(url_for("edit_profile_page"))
    else:
        return render_template(
            "profile.html",
            preferred_name="B42",
            major="Computer Science",
            dorm="Off-campus",
            full_name="Team B42",
            email="teamB42@teamB42.com",
            phone="(097) 234-5678",
            about_me="We are just CS students trying to graduate",
        )


@app.route("/editprofile", methods=["GET", "POST"])
def edit_profile_page():
    if request.method == "POST":
        if request.form.get("Cancel") == "Cancel":
            return redirect(url_for("profile_page"))
        elif request.form.get("Save Profile") == "Save Profile":
            # Here is where all the backend for storing new profile data should go
            return redirect(url_for("profile_page"))
    else:
        return render_template("profile_form.html")


@app.route("/studentevents", methods=["GET", "POST"])
def student_events_page():
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
        elif request.form.get("see_rsvp_list") == "See RSVP List":
            return redirect(url_for("rsvp_list_page"))
        elif request.form.get("New") == "New":
            global invalidEventFields
            invalidEventFields = False
            return redirect(url_for("new_event_page"))
    else:
        events = db_utils.get_with_attributes(
            db_utils.Activities, {"source": "student_events"}
        )
        events.reverse()
        return render_template("student_events.html", events=events)


@app.route("/newevent", methods=["GET", "POST"])
def new_event_page():
    global invalidEventFields
    if request.method == "POST":
        if request.form.get("Create New Event") == "Create New Event":
            event = {
                "net_id": "JuanSupremacy",
                "title": request.form["title"],
                "place": request.form["location"],
                "description": request.form["description"],
                "date": request.form["date"].strip(),
                "time": request.form["time"].strip(),
                "fee": request.form["fee"].strip(),
                "url": request.form["url"],
                "reservation_needed": False,
            }

            # Fill in the url field in case there is none
            if len(event["url"]) == 0:
                event["url"] = "No URL"

            # If any field is empty then don't save event
            for col in event:
                if type(event[col]) != bool:
                    if len(event[col]) == 0:
                        invalidEventFields = True
                        return redirect(url_for("new_event_page"))

            date = event["date"][:]
            time = event["time"][:]
            date_regex = r"^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4}$"
            time_regex = r"((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))"
            fee = event["fee"]

            if (
                (not re.match(date_regex, date))
                or (not re.match(time_regex, time))
                or (not fee.isdigit())
            ):
                invalidEventFields = True
                return redirect(url_for("new_event_page"))

            # Only after passing all those checks we store the event
            db_utils.StudentEvents(**event).add_to_activities()

        return redirect(
            url_for("student_events_page")
        )  # This will need to be changed to whatever the POST is
    else:
        if invalidEventFields:
            flash("Please fill in missing fields")
            invalidEventFields = False
        return render_template("new_event.html")


@app.route("/funspots", methods=["GET", "POST"])
def fun_spots_page():
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template("fun_spots.html", num_spots=4)


@app.route("/happeninginnyc", methods=["GET", "POST"])
def happening_in_nyc_page():
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        return render_template("happening_in_nyc.html")


@app.route("/rsvplist", methods=["GET", "POST"])
def rsvp_list_page():
    if request.method == "POST":
        if request.form.get("Back") == "Back":
            return redirect(url_for("student_events_page"))
    else:
        return render_template(
            "rsvp_list.html",
            event_name="The Hike",
            preferred_name="B42",
            major="Computer Science",
            dorm="Off-campus",
            full_name="Team B42",
            email="teamB42@teamB42.com",
            phone="(097) 234-5678",
        )


if __name__ == "__main__":
    # ------Activities Merge Thread------------
    activities_load = threading.Thread(target=activities_merge)
    activities_load.start()
    # -----------------------------------------
    # db_utils.drop_all_tables()
    # db_utils.create_tables()
    app.run()
