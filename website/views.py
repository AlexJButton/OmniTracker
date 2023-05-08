from flask import Blueprint, render_template, request, Flask
from flask_login import login_required, current_user
from sqlalchemy import MetaData, Table, Column, Integer, String
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("OmniHome.html")


@views.route('/OmniView')
@login_required
def view():
    return render_template("OmniView.html")


@views.route('/OmniMake', methods=['GET', 'POST'])
@login_required
def make():
    if request.method == 'POST':

        # Getting all the user specified info from the user
        tName = request.form.get("tableName")
        num = int(request.form.get("fieldCount")) # This is the invisible input value for how many fields there are
        print(num)
        fieldsList = []
        for i in range(1, num+1):
            fName = request.form.get(f"{i}name")
            fType = request.form.get(f"{i}")
            print(fName)
            fieldsList.append(Column(fName, colType(fType)))

        uID = current_user.id  # Getting the user id and adding it to the table name for later retrieval uses
        tNameUID = f"{uID}_{tName}"

        metadata = MetaData()
        tableData = Table(tNameUID, metadata,
                          Column("id", Integer, primary_key=True),
                          *fieldsList)

        metadata.create_all(db.engine)

        # Create the table with the user given information
        #meta = MetaData()
        #meta.bind = db.engine
        #tableData = Table(tNameUID, meta, *fieldsList)
        #meta.create_all(bind=db.engine)

        return "Success?"


    return render_template("OmniMake.html")


@views.route('/OmniCalendar')
@login_required
def calendar():
    return render_template("OmniCalendar.html")


def colType(col):
    if col == "Text":
        return Integer()
    elif col == "Number":
        return String()

    return String()