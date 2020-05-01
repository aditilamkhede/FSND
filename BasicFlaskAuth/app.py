from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen


app = Flask(__name__)

AUTH0_DOMAIN = 'fsndal.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    # print(token)
    return token


def verify_decode_jwt(token):
    try:
        print('In verify', token)
        jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        # print('After jsonurl')
        jwks = json.loads(jsonurl.read())
        print('Before unverified header')
        unverified_header = jwt.get_unverified_header(token)
    except Exception as e:
        print('Error in Try', e)
        raise e

    rsa_key = {}
    # print('before if kid')
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    print('Before rsa_key', rsa_key)
    if rsa_key:
        try:
            # print('Inside Try')
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            print('before return')

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            print('Error')
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def check_auth_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)

    if permission not in payload['permissions']:
        abort(403)

    return True

def requires_auth(permission=""):
    print("in requires_auth")
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            # print("Token", token)
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            print("Payload", payload)
            check_auth_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

@app.route('/headers')
@requires_auth('get:headers')
def headers(payload):
    print(payload)
    return 'Access Granted'
