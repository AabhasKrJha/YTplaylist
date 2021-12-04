from flask import jsonify

# from contactor.models import User
from YTplaylist import app

#--------------------------------------------------------------------------------------------

def get_app_info():
    routes = dict()
    for rule in app.url_map._rules:
        if rule.endpoint != "static":
            route = rule.rule
            methods = list(rule.methods)
            docstring = app.view_functions[rule.endpoint].__doc__
            routes[route] = {
                "methods" : methods,
                "about" : docstring
            }

    app_info = {
        "app name" : "YTplaylist",
        "app type" : "API",
        "response type" : "application/json",
        "environment" : {
            "language" : "python",
            "framework" : "flask"
        },
        "endpoints" : routes
    }

    return app_info

#--------------------------------------------------------------------------------------------

@app.route('/')
def index():
    """returns app info"""
    app_info = get_app_info()
    return jsonify(app_info)