"""
Provide endpoints and entrypoints for the server.
"""
from flask import (
    Flask,
    jsonify,
    request,

)

server = Flask(__name__)


@server.route('/investments-payback/month', methods=['POST'])
def calculate_investments_payback():
    """
    Calculate investments payback per month.
    """
    request_parameters = request.get_json()
    return jsonify(request_parameters)


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=8000)
