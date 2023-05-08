from flask import Blueprint, render_template, request, Flask
from flask_login import login_required, current_user
from sqlalchemy import MetaData, Table, Column, Integer, Text, inspect
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("OmniHome.html")


@views.route('/OmniView')
@login_required
def view():

    uID = current_user.id
    inspector = inspect(db.engine)
    trackers = [name for name in inspector.get_table_names() if name.startswith(str(uID))]

    print(uID)
    print(trackers)

    return render_template("OmniView.html", trackers=trackers)


@views.route('/OmniMake', methods=['GET', 'POST'])
@login_required
def make():
    if request.method == 'POST':

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

        metadata = MetaData()
        tableData = Table(tNameUID, metadata,
                          Column("id", Integer, primary_key=True),
                          *fieldsList)

        metadata.create_all(db.engine)

        return "Success?"


    return render_template("OmniMake.html")


@views.route('/OmniCalendar')
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