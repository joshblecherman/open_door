from flask import render_template, redirect, request, url_for, flash, session
from od_app import app
import threading
from od_app.od_utils import db_utils
from od_app.od_utils.merging import activities_merge, spots_merge
import re
from datetime import timedelta

invalidEventFields = False
invalidSignUp = False
invalidLogin = False
userAlreadyExists = False
rsvpUsers = []

app.permanent_session_lifetime = timedelta(minutes=10)


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

            if token is None:
                invalidLogin = True
                return redirect(url_for("login_page"))

            # Only after passing all the previous tests, the login is succesful
            session.permanent = True
            session["net_id"] = netid
            return redirect(url_for("home_page"))

    else:
        if "net_id" in session:
            return redirect(url_for("home_page"))
        if invalidLogin:
            flash("Please double check Net id or password")
            invalidLogin = False
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up_page():
    global invalidSignUp
    global userAlreadyExists
    if request.method == "POST":
        if request.form.get("Login") == "Login":
            return redirect(url_for("login_page"))
        elif request.form.get("Sign Up") == "Sign Up":
            netid = request.form["netid"].lower()
            password = request.form["password"]
            repassword = request.form["repassword"]

            existing = db_utils.get_with_attributes(db_utils.Users, {"net_id": netid})

            if len(existing) > 0:
                userAlreadyExists = True
                return redirect(url_for("sign_up_page"))

            if (
                (password != repassword)
                or (len(password) == 0)
                or (len(repassword) == 0)
                or (len(netid) == 0)
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
            session.permanent = True
            session["net_id"] = netid
            return redirect(url_for("home_page"))

    else:
        if "net_id" in session:
            return redirect(url_for("home_page"))
        if invalidSignUp:
            flash("Please double check Net id or password")
            invalidSignUp = False
        if userAlreadyExists:
            flash("User already exists, perhaps you meant to Login")
            userAlreadyExists = False
        return render_template("sign_up.html")


@app.route("/home", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        if not ("net_id" in session):
            return redirect(url_for("login_page"))
        return render_template("home.html")


@app.route("/myprofile", methods=["GET", "POST"])
def profile_page():
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
        elif request.form.get("Edit") == "Edit":
            return redirect(url_for("edit_profile_page"))
        elif request.form.get("Log out") == "Log out":
            session.pop("net_id", None)
            return redirect(url_for("login_page"))
    else:
        if not ("net_id" in session):
            return redirect(url_for("login_page"))

        currentProfile = db_utils.get_with_attributes(
            db_utils.Profiles, {"net_id": session["net_id"]}
        )
        currentProfile = currentProfile[0]

        return render_template("profile.html", profile=currentProfile)


@app.route("/editprofile", methods=["GET", "POST"])
def edit_profile_page():
    if request.method == "POST":
        if request.form.get("Cancel") == "Cancel":
            return redirect(url_for("profile_page"))
        elif request.form.get("Save Profile") == "Save Profile":
            # Here is where all the backend for storing new profile data should go
            return redirect(url_for("profile_page"))
    else:
        if not ("net_id" in session):
            return redirect(url_for("login_page"))
        return render_template("profile_form.html")


@app.route("/studentevents", methods=["GET", "POST"])
def student_events_page():
    global rsvpUsers
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))

        elif request.form.get("New") == "New":
            global invalidEventFields
            invalidEventFields = False
            return redirect(url_for("new_event_page"))

        if not (request.form.get("rsvp") is None):
            activity_id = request.form.get("rsvp")
            activity = db_utils.get_with_attributes(
                db_utils.Activities, {"activity_id": activity_id}
            )
            activity = activity[0]

            rsvp_list = activity.rsvp_list
            if type(rsvp_list) == list:
                if session["net_id"] not in rsvp_list:
                    rsvp_list.append(session["net_id"])
            else:
                rsvp_list = [session["net_id"]]

            upDated = {
                "activity_id": activity_id,
                "title": activity.title,
                "place": activity.place,
                "description": activity.description,
                "datetime": activity.datetime,
                "fee": activity.fee,
                "url": activity.url,
                "img_url": activity.img_url,
                "reservation_needed": activity.reservation_needed,
                "source": activity.source,
                "rsvp_list": rsvp_list,
            }

            rsvpUsers = []

            for id in rsvp_list:
                user = db_utils.get_with_attributes(db_utils.Profiles, {"net_id": id})
                user = user[0]
                rsvpUsers.append(user)

            db_utils.add(db_utils.Activities(**upDated), overwrite=True)

            return redirect(url_for("rsvp_list_page"))

    else:
        if not ("net_id" in session):
            return redirect(url_for("login_page"))
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
                "net_id": session["net_id"],
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
        if not ("net_id" in session):
            return redirect(url_for("login_page"))

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
        if not ("net_id" in session):
            return redirect(url_for("login_page"))

        spots = db_utils.get_with_attributes(db_utils.Spots)
        return render_template("fun_spots.html", spots=spots)


@app.route("/happeninginnyc", methods=["GET", "POST"])
def happening_in_nyc_page():
    if request.method == "POST":
        tabs = check_main_tabs()
        if tabs:
            return redirect(url_for(tabs))
    else:
        if not ("net_id" in session):
            return redirect(url_for("login_page"))

        return render_template("happening_in_nyc.html")


@app.route("/rsvplist", methods=["GET", "POST"])
def rsvp_list_page():
    if request.method == "POST":
        if request.form.get("Back") == "Back":
            return redirect(url_for("student_events_page"))
    else:
        if not ("net_id" in session):
            return redirect(url_for("login_page"))

        return render_template("rsvp_list.html", attendees=rsvpUsers)


if __name__ == "__main__":
    # db_utils.drop_all_tables()
    # db_utils.create_tables()

    # ------Activities Merge Thread------------
    activities_load = threading.Thread(target=activities_merge)
    activities_load.start()
    # -----------------------------------------

    # ------Spots Merge Thread-----------------
    spots_load = threading.Thread(target=spots_merge)
    spots_load.start()
    # -----------------------------------------

    app.run()
