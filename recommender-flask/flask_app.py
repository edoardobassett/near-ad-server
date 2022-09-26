
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify
from flask import request
from recommender import Recommender
from flask_cors import CORS
from update import Updater

app = Flask(__name__)
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

model = Recommender()



@app.route('/')
def hello_world():
    return 'Hello, stranger. May I recommend you where to go?'


@app.route('/add_row', methods=['POST'])
def add_row():
    if request.method == 'POST':
        emitted_by_contract_account_id = request.form.get('emitted_by_contract_account_id')
        token_id = request.form.get('token_id')
        token_new_owner_account_id = request.form.get('token_new_owner_account_id')
        u = Updater()
        success = u.add_row(emitted_by_contract_account_id=emitted_by_contract_account_id, token_id=token_id, token_new_owner_account_id=token_new_owner_account_id)

        res = {'success': success}
        response = jsonify(res)
        response.status_code = 200
        return response

@app.route('/interacted')
def interacted_with():
    account = request.args.get('account', default = 'root.near', type = str)
    contract = request.args.get('contract', default = '', type = str)

    res = {'account': account, 'contract': contract, 'interacted': model.interacted(account, contract)}
    response = jsonify(res)
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    response.status_code = 200
    return response

@app.route('/similar')
def similar_items():
    contract = request.args.get('contract', default = 'asac.near', type = str)
    n_items = request.args.get('n', default = 5, type = int)

    res = {'contract': contract, 'similar': model.similar(contract, n_items)}
    response = jsonify(res)
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    response.status_code = 200
    return response

@app.route('/randomWallet')
def random_wallet():
    res = {'wallet': model.random_wallet()}
    response = jsonify(res)
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    response.status_code = 200
    return response

@app.route('/recommend')
def my_route():
    account = request.args.get('account', default = 'root.near', type = str)
    recommendations = request.args.get('recommendations', default = 10, type = int)

    res = {'account': account, 'recommendations': model.recommend(account, recommendations), 'account_exists': account in model.accounts}
    response = jsonify(res)
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    response.status_code = 200
    return response

