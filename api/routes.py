from api.errors import bad_request
from flask import jsonify, request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required
import sys
import auth, model, repository
from repository import AdminRepo, AuthRepo
from . import bp
from . import errors

admin_repo = repository.AdminRepo()
auth_repo = repository.AuthRepo()

@bp.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    user = model.User.from_dict(auth_repo.login(username))
    if user and safe_str_cmp(user.password, password):
        jwt = create_access_token(identity=username)
        resp = jsonify({'login': True})
        set_access_cookies(resp, jwt)
        return resp, 200
    return jsonify({'login': False}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

@bp.route('/subjects', methods=['GET'])
@jwt_required
def get_subjects():
    result = admin_repo.getAllSubjects()
    return jsonify(result)

@bp.route('/directions/<year>', methods=['GET'])
def get_direction(year='HS3'):
    result = admin_repo.getDirection(year)
    return jsonify(result)

@bp.route('/directions', methods=['GET'])
def get_directions():
    result = admin_repo.getAllDirections()
    return jsonify(result)

@bp.route('/classes', methods=['GET'])
def get_classes():
    result = admin_repo.getAllClasses()
    return jsonify(result)

@bp.route('/teachers', methods=['GET'])
def get_teachers():
    result = admin_repo.getAllTeachers()
    return jsonify(result)

@bp.route('/teacher', methods=['POST'])
def add_teacher():
    data = request.get_json() or {}
    if 'firstname' not in data or 'lastname' not in data:
        return bad_request('must include necessary fields!')
    result = admin_repo.addTeacher(data)
    if not result:
        return bad_request('could not add to database.')
    response = jsonify({'username:': result[0], 'password': result[1]})
    response.status_code = 201
    return response

@bp.route('/student', methods=['POST'])
def add_student():
    data = request.get_json() or {}
    if 'firstname' not in data or 'lastname' not in data or 'year' not in data:
        return bad_request('must include necessary fields!')
    result = admin_repo.addStudent(data)
    if not result:
        return bad_request('could not add to database.')
    response = jsonify({'username:': result[0], 'password': result[1]})
    response.status_code = 201
    return response

@bp.route('/direction', methods=['POST'])
def add_direction():
    data = request.get_json() or {}
    if 'name' not in data or 'year' not in data:
        return bad_request('must include necessary fields!')
    result = admin_repo.addDirection(data)
    if not result:
        return bad_request('could not add to database.')
    response = jsonify({'success:': result})
    response.status_code = 201
    return response

@bp.route('/subject', methods=['POST'])
def add_subject():
    data = request.get_json() or {}
    if 'name' not in data or 'year' not in data:
        return bad_request('must include necessary fields!')
    result = admin_repo.addSubject(data)
    if not result:
        return bad_request('could not add to database.')
    response = jsonify({'success:': result})
    response.status_code = 201
    return response

@bp.route('/class', methods=['POST'])
def add_class():
    data = request.get_json() or {}
    if 'direction' not in data or 'year' not in data:
        return bad_request('must include necessary fields!')
    result = admin_repo.addClass(data)
    if not result:
        return bad_request('could not add to database.')
    response = jsonify({'success:': result})
    response.status_code = 201
    return response