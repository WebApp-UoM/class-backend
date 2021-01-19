from flask.globals import request
from flask.json import jsonify
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import model, repository
import sys

auth_repo = repository.AuthRepo()
'''
def authenticate(username, password):
    print(auth_repo.login(username), file=sys.stderr)
    user = model.User.from_dict(auth_repo.login(username))
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    username = payload['identity']
    user = model.User.from_dict(auth_repo.login(username))
    return user
'''