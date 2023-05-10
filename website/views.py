from flask import Blueprint, render_template, request, Flask, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import MetaData, Table, Column, Integer, Text, inspect, text
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
        tableCols.append([dict["name"] for dict in inspector.get_columns(trackers[i]) if not dict["name"]=="id"])

    # Removing the user ID from the name of the table
    trackers = [name.split("_")[1] for name in trackers]

    return render_template("OmniView.html", trackers=trackers, tableCols=tableCols)


@views.route("/OmniEdit")
@login_required
def editBase():
    return redirect(url_for("views.view"))


@views.route("/OmniEdit/<tracker>")
@login_required
def edit(tracker):

    # Getting the columns of the specified table
    engine = db.engine
    inspector = inspect(engine)
    tableName = f"{current_user.id}_{tracker}"
    with engine.connect() as connection:
        # Getting the column names of the table and the rows of information in the table
        tableCols = [dict["name"] for dict in inspector.get_columns(tableName) if not dict["name"]=="id"]
        tableRows = connection.execute(text(f"SELECT * FROM '{tableName}'"))
        tableRows = [row[1:] for row in tableRows]

        # Getting the types of values in the table, and turning it to 0 & 1 for Jinja use
        tableTypes = [dict["type"] for dict in inspector.get_columns(tableName) if not dict["name"] == "id"]
        tableTypes = [0 if isinstance(col, Integer) else 1 if isinstance(col, Text) else -1 for col in tableTypes]

    # If the table is empty, like a newly made table, then fill it with default values
    if tableRows == []:
        tableRows = [["Empty" if col == 1 else 0 if col == 0 else "ERROR" for col in tableTypes]]

    return render_template("OmniEdit.html", tName=tracker, tableCols=tableCols, tableRows=tableRows, tableTypes=tableTypes)


@views.route("/OmniEdit/<tracker>", methods=["POST"])
@login_required
def edit2(tracker):
    return "Success " + tracker


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