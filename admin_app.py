from flask import Flask, render_template, request
import requests
app = Flask(__name__, template_folder='templates')
     

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/services", methods = ['POST', 'GET'])
def create_service():
    if request.method == 'POST':
        j ={}
        text = request.form
        service = text["service_name"]
        j["content"] = text["service_content"]
        try:
            resp = requests.post("http://localhost:8010/API/services/"+service, json = j)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if resp.status_code == 120:
            message = "HTTP: 120 - Service Already Exist"
            return render_template("create_service.html", message = message)
        if resp.status_code == 521:
            message = "HTTP: 521 - Erro na database, por favor tente outra vez."
            return render_template("create_service.html", message = message)
        else: 
            message = "New presential service created successfully"
            return render_template("create_service.html", message = message)
    elif request.method == 'GET':
        return render_template("create_service.html")

@app.route("/list_services", methods = ['GET', 'POST'])
def list_all_services():

    if request.method == "GET":
        try:
            service="all"
            response_service = requests.get("http://localhost:8010/API/services/"+service)
            lista = response_service.json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response_service.status_code != 200:
            message = "HTTP: 521 - Erro na database, por favor tente outra vez."
            return render_template("list_all_services.html", lista2 = lista, message = message)
        lista = response_service.json()
        return render_template("list_all_services.html", lista2 = lista)
    elif request.method =="POST":
        text = request.form
        service = text["service"]
        j = {}
        j["content"] = "Delete"
        try:
            resp = requests.post("http://localhost:8010/API/services/"+service, json = j)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if resp.status_code == 120:
            message = "HTTP: 120 - Service Already Exist"
            return render_template("list_all_services.html",lista2 = lista, message = message)
        if resp.status_code == 521:
            message = "HTTP: 521 - Erro na database, por favor tente outra vez."
            return render_template("list_all_services.html",lista2 = lista, message = message)
        else: 
            message = "HTTP: 202 - Service Deleted"
            try:
                service="all"
                response_service = requests.get("http://localhost:8010/API/services/"+service)
                lista = response_service.json()
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            if response_service.status_code != 200:
                message = "HTTP: 521 - Erro na database, por favor tente outra vez."
                return render_template("list_all_services.html", lista2 = lista, message = message)
            lista = response_service.json()
            return render_template("list_all_services.html",lista2 = lista, message = message)

@app.route("/evaluations/", methods = ['GET', 'POST'])
def list_evaluation_service():
    
    try:
        service="all"
        response_service = requests.get("http://localhost:8010/API/services/"+service)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    if response_service.status_code != 200:
        message = "HTTP: 521 - Erro na database, por favor tente outra vez."
        return render_template("list_evaluation.html", lista = lista_lists, message = message)

    lista = response_service.json()
    if request.method == 'POST':
        text = request.form
        service = text["service"]
        try:
            response = requests.get("http://localhost:8010/API/evaluations/"+service)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response.status_code == 122:
            message = "HTTP: 122 - This service has zero evaluations"
            return render_template("list_evaluation.html",service = service, message = message,lista2 = lista)
        elif response.status_code != 200:
            message = "HTTP: 521 - Erro na database, por favor tente outra vez."
            return render_template("list_evaluation.html",service = service, message = message,lista2 = lista)
        lista_lists = response.json()
        return render_template("list_evaluation.html",service = service, lista = lista_lists, lista2 = lista)
    elif request.method =='GET':
        return render_template("list_evaluation.html",lista2 = lista)

@app.route("/activities/", methods = ['GET','POST'])
def activities():
    k = {}
    try:
        activity="all"
        response = requests.get("http://localhost:8010/API/activities/"+activity,json = k)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    if response.status_code != 200:
        message = "HTTP: 521 - Erro na database, por favor tente outra vez."
        return render_template("list_student_activities.html", message = message)
    lista = response.json()
    if request.method == 'POST':
        j={}
        text = request.form
        j["area"] = "Student"
        student = text["student"]
        try:
            response = requests.get("http://localhost:8010/API/activities/"+student, json=j)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response.status_code == 122:
            message = "HTTP: 122 - This student doesn't have any activity registed"
            return render_template("list_student_activities.html",student = student, message = message, lista = lista_lists, lista2 = lista)
        elif response.status_code != 200:
            message = "HTTP: 521 - Erro na database, por favor tente outra vez."
            return render_template("list_student_activities.html",student = student, message = message, lista = lista_lists, lista2 = lista)
        lista_lists = response.json()
        return render_template("list_student_activities.html",student = student, lista = lista_lists, lista2 = lista)
    elif request.method =='GET':
        return render_template("list_student_activities.html", lista2 = lista)

@app.route("/courses/", methods = ['POST', 'GET'])
def courses():
    try:
        course="all"
        response = requests.get("http://localhost:8010/API/courses/"+course)
        lista = response.json()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    if response.status_code != 200:
        message = "HTTP: 521 - Erro na database, por favor tente outra vez."
        return render_template("list_attendances.html", message = message,  lista2 = lista)
    if request.method == 'POST':
        text = request.form
        course = text["course"]
        try:
            response = requests.get("http://localhost:8010/API/courses/"+course)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response.status_code == 122:
            message = "This course doesn't have any attendances"
            return render_template("list_attendances.html",course = course, message = message,  lista2 = lista)
        elif response.status_code != 200:
            message = "HTTP: 521 - Erro na database, por favor tente outra vez."
            return render_template("list_attendances.html", course = course, message = message,  lista2 = lista)
        lista_lists = response.json()
        return render_template("list_attendances.html",service = course, lista = lista_lists, lista2 = lista)
    elif request.method =='GET':
        return render_template("list_attendances.html", lista2 = lista)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)