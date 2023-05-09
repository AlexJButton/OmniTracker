from flask import Blueprint, render_template, request, Flask, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import MetaData, Table, Column, Integer, Text, inspect
from . import db

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("OmniHome.html")


@views.route("/OmniView")
@login_required
def view():

    # Getting the titles for all the tables for the user
    uID = current_user.id
    inspector = inspect(db.engine)
    trackers = [name for name in inspector.get_table_names() if name.startswith(str(uID))]

    # Getting the columns of each table
    tableCols = []
    for i in range(len(trackers)):
        tableCols.append([dict["name"] for dict in inspector.get_columns(trackers[i])])

    # Removing the user ID from the name of the table
    trackers = [name.split("_")[1] for name in trackers]

    return render_template("OmniView.html", trackers=trackers, tableCols=tableCols)


@views.route("/OmniEdit/<tracker>")
@login_required
def edit(tracker):

    # Getting the columns of the specified table
    engine = db.engine()
    uID = current_user.id
    tableName = f"{uID}_{tracker}"
    with engine.connect() as connection:
        tableCols = connection.execute(f"SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('{tableName}')")
        tableRows = connection.execute(f"SELECT * FROM {tableName}")

    return render_template("OmniEdit", tName=tracker, tableCols=tableCols, tableRows=tableRows)


#@views.route("OmniEdit")
#@login_required
#def edit(tracker):



@views.route("/OmniMake", methods=["GET", "POST"])
@login_required
def make():
    if request.method == "POST":

        # Getting all the user specified info from the user
        tName = request.form.get("tableName")
        num = int(request.form.get("fieldCount")) # This is the invisible input value for how many fields there are
        fieldsList = []
        for i in range(1, num+1):
            fName = request.form.get(f"{i}name")
            fType = request.form.get(f"{i}")
            fieldsList.append(Column(fName, colType(fType)))

        uID = current_user.id  # Getting the user id and adding it to the table name for later retrieval uses
        tNameUID = f"{uID}_{tName}"

        # Creating the table with the name, a primary key, and the requested fields
        metadata = MetaData()
        tableData = Table(tNameUID, metadata,
                          Column("id", Integer, primary_key=True),
                          *fieldsList)

        metadata.create_all(db.engine)

        return redirect(url_for("views.view"))


    return render_template("OmniMake.html")


@views.route("/OmniCalendar")
@login_required
def calendar():
    return render_template("OmniCalendar.html")


def colType(col):
    if col == "Text":
        print(col, "is returning Text")
        return Text()
    elif col == "Number":
        print(col, "is returning Integer")
        return Integer()
    else:
        print(col, "is returning base case")
        return Text()