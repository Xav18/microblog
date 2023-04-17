from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html'] #determines the adapted response to the error, true if JSON is the better format, false if it's HTML


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404 #sends user to the error 404 page


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback() #goes back to the previous db state
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500 #to error 500 page