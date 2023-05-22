from flask import Flask,  request
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String
import datetime
from sqlalchemy.orm import sessionmaker
from os import path
import itertools
import datetime


app = Flask(__name__, template_folder='templates')


# SLQ access layer initialization
DATABASE_FILE = "services_data.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s' % DATABASE_FILE, echo=False,
                       connect_args={'check_same_thread': False})  # echo = True shows all SQL calls

Base = declarative_base()


# Declaration of data
class Presential_Services(Base):
    __tablename__ = 'Presential_Services'
    service_name = Column(String)
    date_time = Column(String, primary_key=True)  # A type for datetime.date() objects.
    service_content = Column(String)

    def __repr__(self):
        return "Service Name='%s', Service Content='%s', Date/time = %s" % (
            self.service_name, self.service_content, str(self.date_time))


Base.metadata.create_all(engine)  # Create tables for the data models

Session = sessionmaker(bind=engine)
session = Session()

@app.route("/API/services/<path:service>", methods = ['GET', 'POST'])
def services(service):
    if request.method == "GET":
        if not (service=="all"):
            b = session.query(Presential_Services).filter(Presential_Services.service_name == service).first()
            if b:   
                return "", 120
            else:
                return "", 521
        else:
            a = session.query(Presential_Services.service_name).all()
            gatesData = list(itertools.chain(*a))
            return jsonify(gatesData), 200

    if request.method == "POST":
        j = request.json
        if (j["content"] == "Delete"):
            session.query(Presential_Services).filter(Presential_Services.service_name == service).delete()
            try:
                session.commit()
            except:
                session.rollback()
                return "", 521
            return "", 201
        else:
            service_content = j["content"]

            #Se já existir o serviço, não criar e mandar para trás
            b = session.query(Presential_Services).filter(Presential_Services.service_name == service).first()
            if b:   
                return "", 120
    
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%y , %H:%M:%S")
            service = Presential_Services(service_name = service, service_content = service_content, date_time = dt_string)
            session.add(service)
            try:
                session.commit()
            except:
                session.rollback()
                return "", 521
            return "", 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8020, debug=True)