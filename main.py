from flask import Flask, request, jsonify, json
from functools import wraps
import requests
from flask_bcrypt import Bcrypt

import db
import model
import uuid

app = Flask(__name__)
bcrypt = Bcrypt(app)


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'jwtToken' in request.headers:
            jwt_token = request.headers['jwtToken']
            verification_result = model.verify_jwt_token(jwt_token)
            print(verification_result)
            if verification_result[1] == 200:
                return f(*args, **kwargs)
            else:
                return verification_result
        else:
            return json.dumps({'message': 'Token is missing'}), 401

    return decorated_function


@app.route('/', methods=['GET'])
def hello():
    return 'hello world'


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data['email']
    password = data['password']
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    username = email.split('@')[0]
    jwt_token = model.generate_jwt_token(username)
    return {
        'user_id': username,
        'email': email,
        'jwt_token': jwt_token,
        'pw_hash': pw_hash
    }


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    users = db.get_user(email)
    if users:
        user = users[0]
        print(user)
        pw_hash = user['pw_hash']
        user_id = user['user_id']
        is_valid = bcrypt.check_password_hash(pw_hash, password)
        if is_valid:
            return {
                'user_id': user_id,
                'email': email,
                'jwt_token':user['jwt_token']
            }
    return json.dumps({'message': 'Invalid password'}), 400


@app.route('/country', methods=['GET'])
@token_required
def get_country_info():
    request_args = request.args
    country_name = None
    if request_args and 'country_name' in request_args:
        country_name = request_args['country_name']
    if country_name is not None:
        rest_api_url = 'https://restcountries.com/v3.1/name/' + country_name + '?fullText=true'
        try:
            # Make a GET request to the API
            response = requests.get(rest_api_url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                country_data = response.json()
                # You can process the country_data here as needed
                # return jsonify(country_data)
            else:
                # Handle API request error
                return jsonify({'error': 'Failed to retrieve country information'}), response.status_code
        except Exception as e:
            # Handle exceptions, e.g., network errors
            return jsonify({'error': str(e)}), 500
    data = country_data[0]
    response = {
        'country_name': data['name']['common'],
        'capital': data['capital'],
        'official_name': data['name']['official'],
        'population': data['population'],
        'languages': data['languages'],
        'latitude-longitude': data['latlng'],
        'region': data['region'],
        'timezones': data['timezones'],
        'unMember': data['unMember']
    }
    return response


@app.route('/country/filter-population', methods=['GET'])
@token_required
def get_filter_population():
    request_args = request.args
    population = None
    order = None
    if request_args and 'population' in request_args:
        population = int(request_args['population'])
    if request_args and 'order' in request_args:
        order = request_args['order']

    if population and order is not None:
        rest_api_url = 'https://restcountries.com/v3.1/all?fields=name,population'
        try:
            # Make a GET request to the API
            response = requests.get(rest_api_url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                country_data = response.json()
                # You can process the country_data here as needed
                # return jsonify(country_data)
            else:
                # Handle API request error
                return jsonify({'error': 'Failed to retrieve country information'}), response.status_code
        except Exception as e:
            # Handle exceptions, e.g., network errors
            return jsonify({'error': str(e)}), 500
    filtered_data = []
    for country in country_data:
        if country['population'] > population:
            filtered_data.append(country)
    response = []
    for data in filtered_data:
        res = {
            'common_name': data['name']['common'],
            'official_name': data['name']['official'],
            'population': data['population']
        }
        response.append(res)
    if order == 'desc':
        sorted_response = sorted(response, key=lambda x: x["population"])
    else:
        sorted_response = sorted(response, key=lambda x: x["population"], reverse=True)
    return sorted_response


@app.route('/country/filter-area', methods=['GET'])
@token_required
def get_filter_area():
    request_args = request.args
    area = None
    order = None
    if request_args and 'area' in request_args:
        area = int(request_args['area'])
    if request_args and 'order' in request_args:
        order = request_args['order']

    if area and order is not None:
        rest_api_url = 'https://restcountries.com/v3.1/all?fields=name,area'
        try:
            # Make a GET request to the API
            response = requests.get(rest_api_url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                country_data = response.json()
                # You can process the country_data here as needed
                # return jsonify(country_data)
            else:
                # Handle API request error
                return jsonify({'error': 'Failed to retrieve country information'}), response.status_code
        except Exception as e:
            # Handle exceptions, e.g., network errors
            return jsonify({'error': str(e)}), 500
    filtered_data = []
    for country in country_data:
        if country['area'] > area:
            filtered_data.append(country)
    response = []
    for data in filtered_data:
        res = {
            'common_name': data['name']['common'],
            'official_name': data['name']['official'],
            'area': data['area']
        }
        response.append(res)
    if order == 'desc':
        sorted_response = sorted(response, key=lambda x: x["area"])
    else:
        sorted_response = sorted(response, key=lambda x: x["area"], reverse=True)
    return sorted_response


@app.route('/country/filter-language', methods=['GET'])
@token_required
def get_filter_language():
    request_args = request.args
    language = None
    if request_args and 'language' in request_args:
        language = request_args['language']

    if language is not None:
        rest_api_url = 'https://restcountries.com/v3.1/all?fields=name,languages'
        try:
            # Make a GET request to the API
            response = requests.get(rest_api_url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                country_data = response.json()
                # You can process the country_data here as needed
                # return jsonify(country_data)
            else:
                # Handle API request error
                return jsonify({'error': 'Failed to retrieve country information'}), response.status_code
        except Exception as e:
            # Handle exceptions, e.g., network errors
            return jsonify({'error': str(e)}), 500
    response_list = []
    for data in country_data:
        res = {
            'common_name': data['name']['common'],
            'official_name': data['name']['official'],
            'languages': data['languages']
        }
        response_list.append(res)
    filtered_response = []
    for response in response_list:
        languages = response['languages']
        if language in languages:
            filtered_response.append(response)

    return filtered_response


if __name__ == '__main__':
    app.run(debug=True)
