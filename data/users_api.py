import flask
import requests
from . import db_session
from .users import User
from flask import jsonify, request, make_response

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'email', 'about', 'city_from', 'created_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>/city', methods=['GET'])
def get_user_city(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return None

    toponym_to_find = user.city_from
    geocoder_api_server = "https://geocode-maps.yandex.ru/1.x"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": 'json'}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    ll = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
    static_api_server = "https://static-maps.yandex.ru/1.x/"
    static_params = {
        "l": 'sat',
        "ll": ','.join(ll),
        'z': 12,
        'size': '450,450'}

    response = requests.get(static_api_server, params=static_params)
    response = make_response(response.content)
    response.headers.set('Content-Type', 'image/jpeg')
    return response


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'})
    return jsonify(
        {
            'user': user.to_dict(only=(
                'name', 'email', 'about', 'city_from', 'created_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'about', 'email', 'city_from', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    check = db_sess.query(User).filter(User.email == request.json.get('email')).first()

    if check:
        return jsonify({'error': 'User already exists'})

    user = User(
        name=request.json.get('name'),
        email=request.json.get('email'),
        city_from=request.json.get('city_from'),
        about=request.json.get('about')
    )
    user.set_password(request.json.get('password'))

    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'})
    db_sess.query(User).filter(User.id == user_id).update({
        User.name: request.json.get('name'),
        User.email: request.json.get('email'),
        User.about: request.json.get('about'),
        User.city_from: request.json.get('city_from')
    })

    if request.json.get('password'):
        user.set_password(request.json.get('password'))

    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/login', methods=['POST'])
def login_user():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == request.json.get('email')).first()
    if not user:
        return jsonify({'error': 'User not found'})
    if user and user.check_password(request.json.get('password')):
        return jsonify({'success': 'OK', 'message': 'User logging in', 'user_id': user.id})

    return jsonify({'success': 'Fail', 'message': 'Wrong password'})
