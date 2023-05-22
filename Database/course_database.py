from flask import Flask, request
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
import datetime
from sqlalchemy.orm import sessionmaker
from os import path
import itertools
import datetime


app = Flask(__name__, template_folder='templates')


# SLQ access layer initialization
DATABASE_FILE = "course_database.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s' % DATABASE_FILE, echo=False,
                       connect_args={'check_same_thread': False})  # echo = True shows all SQL calls

Base = declarative_base()


# Declaration of data
class Courses(Base):
    __tablename__ = 'Courses'
    course_name = Column(String)
    date_time = Column(String, primary_key=True)  # A type for datetime.date() objects.
    student = Column(String)

    def __repr__(self):
        return "Course Name='%s', student ='%s', Date/time = %s" % (
            self.course_name, self.student, str(self.date_time))


Base.metadata.create_all(engine)  # Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()
    
@app.route("/API/courses/<path:course>", methods = ['GET', 'POST'])
def new_course(course):
    if request.method == "GET":
        if not (course == "all"):
            b = session.query(Courses).filter(Courses.course_name == course).first()
            if not b:   
                return "", 122
            a = session.query(Courses.student).filter(Courses.course_name == course).all()
            gatesData = list(itertools.chain(*a))
            return jsonify(gatesData), 200
        else:
            a = session.query(Courses.course_name).group_by(Courses.course_name).all()
            gatesData = list(itertools.chain(*a))
            return jsonify(gatesData), 200
        
    if request.method == "POST":
        j = request.json
        student = j["name"]
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%y , %H:%M:%S")
        course = Courses(course_name = course, student = student, date_time = dt_string)
        session.add(course)
        try:
            session.commit()
        except:
            session.rollback()
            return "", 521
        return "", 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8003, debug=True)