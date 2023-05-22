from flask import Flask, request
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import datetime
from sqlalchemy.orm import sessionmaker
from os import path
import itertools


app = Flask(__name__, template_folder='templates')


# SLQ access layer initialization
DATABASE_FILE = "activities_data.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s' % DATABASE_FILE, echo=False,
                       connect_args={'check_same_thread': False})  # echo = True shows all SQL calls

Base = declarative_base()


# Declaration of data
class Activities(Base):
    __tablename__ = 'Activities'
    student = Column(String)
    date_time = Column(String, primary_key=True)  # A type for datetime.date() objects.
    area = Column(String)
    activity = Column(String)
    start = Column(String)
    end = Column(String)

    def __repr__(self):
        return "Student='%s', Area = %s, Activity='%s', Start = '%s', End = '%s',Date/time = %s" % (
            self.student, self.area, self.activity,self.start,self.end, str(self.date_time))


Base.metadata.create_all(engine)  # Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()

@app.route("/API/activities/<path:arg>", methods = ['GET', 'POST'])
def activities(arg):
    if request.method == "GET":
        if (arg == "plot"):
            j = request.json
            a = session.query(Activities.start , Activities.end).filter(Activities.area == j["area"]).all()
            date_personal = []
            for k in a:
                date_personal.append({"start":k[0], "end":k[1]})
            return jsonify(date_personal), 200
        elif(arg == "table"):
            j = request.json
            a = session.query(Activities.activity, Activities.area, Activities.start,  Activities.end).filter(Activities.student == j["name"]).all()
            table = []
            for k in a:
                table.append({"activity":k[0], "area":k[1], "start":k[2],"end":k[3]})
            return jsonify(table), 200

        elif not (arg == 'all') and not (arg == 'plot') and not (arg == 'table'):
            j = request.json
            if (j["area"] == "Student"):
                student = arg
                b = session.query(Activities).filter(Activities.student == student).first()
                if not b:   
                    return "", 122
                a = session.query(Activities.activity).filter(Activities.student == student).all()
                gatesData = list(itertools.chain(*a))
                return jsonify(gatesData), 200
            elif (j["area"] == "Administrative"):
                student = arg
                b = session.query(Activities).filter(Activities.student == student).first()
                if not b:   
                    return "", 122
                a = session.query(Activities.activity).filter(Activities.student == student).filter(Activities.area == j["area"]).distinct().all()
                gatesData = list(itertools.chain(*a))
                return jsonify(gatesData), 200
        else:
            a = session.query(Activities.student).distinct().all()
            gatesData = list(itertools.chain(*a))
            return jsonify(gatesData), 200
    if request.method == "POST":
        j = request.json
        student = j["name"]
        area = j["area"]
        start = j["start"]
        end = j["end"]
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%y , %H:%M:%S")
        activity = Activities(student = student, area = area, activity = arg, start = start, end = end, date_time = dt_string)
        session.add(activity)
        try:
            session.commit()
        except:
            session.rollback()
            return "", 521
        return "", 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8077, debug=True)