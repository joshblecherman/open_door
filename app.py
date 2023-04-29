from flask import render_template, redirect, request, url_for, flash
from od_app import app, db
import threading
from od_app.od_utils import db_utils
from od_app.od_utils.merging import activities_merge

missingEventFields = False


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
            global missingEventFields
            missingEventFields = False
            return redirect(url_for("new_event_page"))
    else:
        events = db_utils.get_with_attributes(
            db_utils.Activities, {"source": "student_events"}
        )
        events.reverse()
        return render_template("student_events.html", events=events)


@app.route("/newevent", methods=["GET", "POST"])
def new_event_page():
    global missingEventFields
    if request.method == "POST":
        if request.form.get("Create New Event") == "Create New Event":
            event = {
                "net_id": "JuanSupremacy",
                "title": request.form["title"],
                "place": request.form["location"],
                "description": request.form["description"],
                "date": request.form["date"],
                "time": request.form["time"],
                "fee": request.form["fee"],
                "url": request.form["url"],
                "reservation_needed": False,
            }

            if len(event["url"]) == 0:
                event["url"] = "No URL"

            for col in event:
                if type(event[col]) != bool:
                    if len(event[col]) == 0:
                        missingEventFields = True
                        return redirect(url_for("new_event_page"))

            db_utils.StudentEvents(**event).add_to_activities()

        return redirect(
            url_for("student_events_page")
        )  # This will need to be changed to whatever the POST is
    else:
        if missingEventFields:
            flash("Please fill in missing fields")
            missingEventFields = False
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
