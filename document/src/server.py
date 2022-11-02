from bottle import route, run

@route('/')
def index():
    return "working" 

run(host='0.0.0.0', port=8080)
