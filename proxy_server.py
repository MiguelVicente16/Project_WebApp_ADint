from flask import Flask, request
import requests
app = Flask(__name__, template_folder='templates')


    
@app.route("/API/services/<path:service>",methods = ['GET', 'POST'])
def proxyServices(service):
    if request.method == "GET":
        try:
            response = requests.get("http://localhost:8020/API/services/"+service)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response.status_code != 200:
            return "",521
        return response.json(), 200
    if request.method == "POST":
        try:
            resp = requests.post("http://localhost:8020/API/services/"+service, json = request.json)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if resp.status_code == 120:
            return "",120
        if resp.status_code == 521:
            return "",521
        return "", 201
    
@app.route("/API/courses/<path:course>", methods = ['GET', 'POST'])
def proxyCourses(course):
    if request.method == "GET":
        try:
            response = requests.get("http://localhost:8003/API/courses/"+course)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response.status_code == 122:
            return "",122
        if response.status_code != 200:
            return "",521
        return response.json(),200
    if request.method == "POST":
        try:
            resp = requests.post("http://localhost:8003/API/courses/"+course, json = request.json)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if resp.status_code == 120:
            return "",120
        if resp.status_code == 521:
            return "",521

        return "", 201

@app.route("/API/activities/<path:arg>", methods = ['GET', 'POST'])
def proxyActivities(arg):
    if request.method =="GET":
        j = {}
        j = request.json
        try:
            response = requests.get("http://localhost:8077/API/activities/"+arg, json=j)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response.status_code == 122:
            return "",122
        if response.status_code != 200:
            return "", 521
        return response.json(),200
    if request.method == "POST":
        j = {}
        j = request.json
        try:
            resp = requests.post("http://localhost:8077/API/activities/"+arg, json = j)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if resp.status_code == 521:
            return "",521
        return "", 201


@app.route("/API/evaluations/<path:service>", methods = ['GET', 'POST'])
def proxyEvaluations(service):
    if request.method =="GET":
        if not (service=='all'):
            try:
                response = requests.get("http://localhost:8006/API/evaluations/"+service)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            if response.status_code == 122:
                return "",122
            elif response.status_code == 200:
                return response.json(),200
            return "",521
        else:
            try:
                response = requests.get("http://localhost:8006/API/evaluations/all")
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            if response.status_code != 200:
                return "",521
            return response.json(),200
    if request.method == "POST":
        try:
            service=request.json["name"]
            response_service = requests.get("http://localhost:8020/API/services/"+service)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        if response_service.status_code == 120:
            try:
                resp = requests.post("http://localhost:8006/API/evaluations/"+service, json = request.json)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                raise SystemExit(e)
            if resp.status_code == 521:
                return "",521
            return "", 201
        else:
            return "", 121


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8010, debug=True)