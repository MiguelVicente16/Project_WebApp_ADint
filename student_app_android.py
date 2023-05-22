from distutils.command.build_scripts import first_line_re
from flask import Flask, redirect, request, url_for, render_template
import requests
import json
import os
import sys
import datetime as dt
import matplotlib
import matplotlib.dates as mdates
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user

from oauthlib.oauth2 import WebApplicationClient
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='templates')


############################################################ FENIX LOGIN ############################################################

FENIX_CLIENT_ID = 1132965128044847
FENIX_CLIENT_SECRET = "rcfkvQNULxx/oRHoqjXS4Bf4NsnT+nBkNfnb5GX5noghCtk2chbKnG6bcl+SSBSGDEb+T61gFw+hGpSAsuzZsA=="


# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///User_database.sqlite"
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    courses = db.Column(db.JSON(256), unique=True)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
client = WebApplicationClient(FENIX_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("student_webpage.html", student_name = current_user.name, user_name = current_user.username
            , email = current_user.email)
    else:
        return render_template("login_page.html")

@app.route("/login")
def login():
    authorization_endpoint = "https://fenix.tecnico.ulisboa.pt/oauth/userdialog"#google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    token_endpoint = "https://fenix.tecnico.ulisboa.pt/oauth/access_token"
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(FENIX_CLIENT_ID, FENIX_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))

    courses_info_endpoint = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person/courses?academicTerm=2022/2023"
    uri, headers, body = client.add_token(courses_info_endpoint)
    courses_info_response = requests.get(uri, headers=headers, data=body)

    userinfo_endpoint = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person"
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email"):
        username = userinfo_response.json()["username"]
        email = userinfo_response.json()["email"]
        name = userinfo_response.json()["name"]

        courses =  []
        for k in courses_info_response.json()["enrolments"]:
            courses.append({"acron": k["acronym"], "nome": k["name"] , "url":k["url"] })
        user = User(username = username ,email = email,name=name,courses = courses)
        try:
            db.session.add(user)
            db.session.commit()
            # Log in the new local user account
            login_user(user)
        except:
            db.session.rollback()
            user = db.session.query(User).filter(User.username == username).first()
            login_user(user)
        return redirect(url_for("index"))
    else:
        return "User email not available.", 400

    return "XXX"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# hook up extensions to app
db.init_app(app)
#####################################################################################################################################


##################### Endpoint to create a table with list of all activities #####################
#
# Recieve a AJAX Get request
# Send a GET REST request to proxy server with the variable activity = "tabel" to specify the get request
# Return a dictionary with activities information
#
@app.route("/table", methods = ['GET'])
@login_required
def table():
    if request.method == "GET":
        activity = "table"
        m = {}
        m["name"] = current_user.name
        try:
            resp_activity = requests.get("http://localhost:8010/API/activities/"+activity, json = m)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
                    raise SystemExit(e)
        if resp_activity.status_code == 521:
            return "HTTP: 521 - Erro na database, por favor tente outra vez."
        table = resp_activity.json()
        return {"table":table}
##################################################################################################


##################### Endpoint to plot the hours spent in each activity by a student #####################
#
# Recieve a AJAX Get request
# Send a GET REST request to proxy server with the variable activity = "plot" to specify the get request
# Return a dictionary with plot image url
#
@app.route("/output", methods = ['GET'])
@login_required
def plot_activities():
    if(request.method == "GET"):
        plt.figure()
        plt.xlabel('Day', fontsize = 16)
        plt.ylabel('Total of Hours', fontsize = 16)
        plt.grid(True)
        plt.title("Total of hours per day in each type of activity")
        today = dt.datetime.today().strftime("%d/%m/%y")
        today = datetime.strptime(today,"%d/%m/%y")
        past = (today - dt.timedelta(days=5))
        then = (today + dt.timedelta(days=5))
        date_generated = [past + dt.timedelta(days=x) for x in range(0, (then-past).days)]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        y_max = 0
        save = 0
        y1 = [0] * 10
        y2 = [0] * 10
        y3 = [0] * 10
        for count in range(3):
            arg = "plot"
            j = {}
            if (count == 0):
                j["area"] = "Personal"
            elif(count == 1):
                j["area"] = "Academic"
            else:
                j["area"] = "Administrative"
            
            try:
                response = requests.get("http://localhost:8010/API/activities/"+arg, json = j)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            
            response_date = {}
            response_date = response.json()
            date_1 = []
            for k in response_date:
                new_day = 0
                d1 = datetime.strptime(k["start"], "%d/%m/%y , %H:%M")
                d2 = datetime.strptime(k["end"], "%d/%m/%y , %H:%M")
                delta = d2-d1
                for j in date_1:
                    if(d1.day == j["Day"]):
                        sum = delta.seconds/3600 + j["Total"]
                        new_day = 1
                        hours = sum
                        j["Total"] = hours
                        if y_max < hours:
                            y_max = hours
                if(new_day == 0):
                    hours = delta.seconds/3600
                    Date = d1.strftime("%d/%m/%Y")
                    if(hours > 24):
                        hours = 24
                    date_1.append({"Day":d1.day,"Date": Date, "Total":hours})
                    if y_max < hours:
                        y_max = hours
            for k in date_1:
                if (count == 0):
                    date = datetime.strptime(k["Date"],"%d/%m/%Y")
                    if (date in date_generated):
                        y1[date_generated.index(date)] = k["Total"]
                elif(count == 1):
                    date = datetime.strptime(k["Date"],"%d/%m/%Y")
                    if (date in date_generated):
                        y2[date_generated.index(date)] = k["Total"]
                else:
                    date = datetime.strptime(k["Date"],"%d/%m/%Y")
                    if (date in date_generated):
                        y3[date_generated.index(date)] = k["Total"]
            if (save < y_max):
                save = y_max

        plt.plot(date_generated,y1, linewidth=2.0, linestyle='-',color='b',alpha=0.5,marker='o', label = "Personal")
        plt.plot(date_generated,y2,linewidth=2.0, linestyle='-',color='r',alpha=0.5,marker='x', label = "Academic")
        plt.plot(date_generated,y3,linewidth=2.0, linestyle='-',color='k',alpha=0.5,marker='s', label = "Administrative")
        plt.yticks(np.arange(0,save, step = 2))
        plt.gcf().autofmt_xdate()
        plt.legend(loc="upper left")
        img = BytesIO()
        plt.savefig(img)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        return {"plot_url":plot_url}
###########################################################################################################


########################################## Endpoint to create a new evaluation of a service ##########################################
#
# - IF recieve a AJAX Get request:
#   . Send a GET REST request to proxy server with the variable student equal to user name that will be used in the activities database
#     to return the services that this student went 
#   . Return a dictionary with the services that this student went 
# - IF recieve a AJAX Post request:
#   . Send a POST REST request to proxy server with the variable service equal to name of the service 
#     that was evaluated to be used in the services database
#   . Return error message
#
@app.route("/evaluations/new", methods = ['POST', 'GET'])
@login_required
def evaluationsNew():

    if request.method == 'POST':
        j ={}
        service = request.get_json()["service"]
        j["name"] = service
        j["content"] = request.get_json()["evaluation"]
        try:
            resp = requests.post("http://localhost:8010/API/evaluations/"+service, json = j)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if resp.status_code == 421:
            return "Problema na database, por favor tente outra vez."
        else: 
            message = "New service evaluation created successfully"
            return {"message": message}

    elif request.method == 'GET':
        
        area={}
        area["area"] = "Administrative"
        student = current_user.name
        try:
            response = requests.get("http://localhost:8010/API/activities/"+student, json = area)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response.status_code == 122:
            message = "HTTP: 122 - This student doesn't have any activity registed"
            return message
        elif response.status_code != 200:
            message = "HTTP: 521 - Erro na database, por favor tente outra vez."
            return message
        lista_lists = response.json()
        return { "lista": lista_lists}
#####################################################################################################################################


################################################## Endpoint to create a new activity ################################################
#
# Send a GET REST request to proxy server with the variable service equal "all" to specify what will return from the database
# - IF recieve a AJAX Get request:
#   . Return a dictionary with a list of all services available and a list of all courses that student is registered
# - IF recieve a AJAX Post request:
#   . Send a POST REST request to proxy server with the variable activity equal to name of the new activity to be add to the database
#     and with a dictionary that contains all information of the new activity
#   . Return error message
#
@app.route("/activities/new", methods = ['POST', 'GET'])
@login_required
def activityNew():
    try:
        service="all"
        response = requests.get("http://localhost:8010/API/services/"+service)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    if response.status_code != 200:
        lista_lists = response.json()
        message = "HTTP: 521 - Erro na database, por favor tente outra vez."
        return message
    lista_lists = response.json()

    if request.method == 'POST':
        
        Personal = request.get_json()["Personal"]
        Academic = request.get_json()["Academic"]
        Administrative = request.get_json()["Administrative"]
        code_status = 201
        if (Personal):
            j ={}
            j["name"] = current_user.name
            j["area"] = "Personal"
            j["start"] = dt.datetime.strptime(request.get_json()["date_Personal_start"],"%Y-%m-%dT%H:%M").strftime("%d/%m/%y , %H:%M")
            j["end"] = dt.datetime.strptime(request.get_json()["date_Personal_end"],"%Y-%m-%dT%H:%M").strftime("%d/%m/%y , %H:%M")
            activity = request.get_json()["Personal"]
            if(activity == "Other"):
                activity = request.form.get("newactivity")
            try:
                resp = requests.post("http://localhost:8010/API/activities/"+activity, json = j)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            if resp.status_code == 521:
                code_status = 521
                return "HTTP: 521 - Erro na database, por favor tente outra vez."
 
        if (Academic):
            j ={}
            j["name"] = current_user.name
            j["area"] = "Academic"
            activity = request.get_json()["Academic"]
            j["start"] = dt.datetime.strptime(request.get_json()["date_Academic_start"],"%Y-%m-%dT%H:%M").strftime("%d/%m/%y , %H:%M")
            j["end"] = dt.datetime.strptime(request.get_json()["date_Academic_end"],"%Y-%m-%dT%H:%M").strftime("%d/%m/%y , %H:%M")
            try:
                resp = requests.post("http://localhost:8010/API/activities/"+activity, json = j)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            if resp.status_code == 521:
                code_status = 521
                return "HTTP: 521 - Erro na database, por favor tente outra vez."

            if (activity == "Attend_classes"):
                k = {}
                k["name"] = current_user.name
                course = request.get_json()["Courses"]
                try:
                    resp = requests.post("http://localhost:8010/API/courses/"+course, json = k)
                except requests.exceptions.RequestException as e:  # This is the correct syntax
                    raise SystemExit(e)
                if resp.status_code == 521:
                    code_status = 521
                    return "HTTP: 521 - Erro na database, por favor tente outra vez."


        if(Administrative):
            j ={}
            j["name"] = current_user.name
            j["area"] = "Administrative"
            j["start"] = dt.datetime.strptime(request.get_json()["date_Administrative_start"],"%Y-%m-%dT%H:%M").strftime("%d/%m/%y , %H:%M")
            j["end"] = dt.datetime.strptime(request.get_json()["date_Administrative_end"],"%Y-%m-%dT%H:%M").strftime("%d/%m/%y , %H:%M")
            activity = request.get_json()["Administrative"]
            try:
                resp = requests.post("http://localhost:8010/API/activities/"+activity, json = j)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            if resp.status_code == 521:
                code_status = 521
                return "HTTP: 521 - Erro na database, por favor tente outra vez."

        if code_status != 521: 
            message = "New activity created successfully"
            return  {"lista": lista_lists, "student_name": current_user.name, "user_name": current_user.username
        , "email": current_user.email, "courses": current_user.courses,"message": message}

        
    elif request.method == 'GET':
        return {"lista": lista_lists, "courses": current_user.courses}
#####################################################################################################################################


################################## Endpoint that list the courses that student is registered #######################################
#
# Recieve a AJAX Get request:
#   . Return a dictionary with a list of all courses that student is registered
# 
@app.route("/courses", methods = ['GET'])
@login_required
def courses():
    if request.method == 'GET':
        return {"courses" :current_user.courses}
#####################################################################################################################################

if __name__ == "__main__":
    if "--setup" in sys.argv:
        with app.app_context():
            db.create_all()
            
            db.session.commit()
            print("Database tables created")
    else:
        app.run(host='0.0.0.0', port=8090, debug=True, ssl_context='adhoc')
        