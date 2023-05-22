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
DATABASE_FILE = "evaluations_database.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s' % DATABASE_FILE, echo=False,
                       connect_args={'check_same_thread': False})  # echo = True shows all SQL calls

Base = declarative_base()


# Declaration of data
class Evaluations(Base):
    __tablename__ = 'Evaluations'
    service = Column(String)
    date_time = Column(String, primary_key=True)  # A type for datetime.date() objects.
    evaluation = Column(String)

    def __repr__(self):
        return "Student='%s', Activitie='%s', Date/time = %s" % (
            self.service, self.evaluation, str(self.date_time))


Base.metadata.create_all(engine)  # Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()
 
@app.route("/API/evaluations/<path:service>", methods = ['GET', 'POST'])
def evaluations(service):
    if request.method == "GET":
        if not (service=='all'):
            b = session.query(Evaluations).filter(Evaluations.service == service).first()
            if not b:   
                return "", 122
            a = session.query(Evaluations.evaluation).filter(Evaluations.service == service).all()
            gatesData = list(itertools.chain(*a))
            return jsonify(gatesData), 200
        else:
            gatesData = [[]]*2
            a = session.query(Evaluations.service).all()
            gatesData[0] = list(itertools.chain(*a))
            a = session.query(Evaluations.evaluation).all()
            gatesData[1] = list(itertools.chain(*a))
            return jsonify(gatesData), 200
    if request.method == "POST":
        j = request.json
        service = j["name"]
        evaluation = j["content"]
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%y , %H:%M:%S")
        row = Evaluations(service = service, evaluation = evaluation, date_time = dt_string)
        session.add(row)
        try:
            session.commit()
        except:
            session.rollback()
            return "", 521
        return "", 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8006, debug=True)