"""
This is a dummy web app simulate user auth
"""

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/user/auth", methods=["POST"])
def home():
    """

    Query:

    url: /user/auth

    POST data:

    {
        "user": "myuser"
        "password" "mypassword"
    }

    Response format:

    {
        message="XXX"
    }

    Returns:
    - 403: is user/password are different to: admin:batman
    - 200: is user/password are equal to: admin:batman
    - 400: when query is malformed
    """

    try:
        user = request.json["user"]
        password = request.json["password"]
    except KeyError:
        return jsonify(message="Invalid query"), 400
    except TypeError as e:
        return jsonify(message=f"Invalid query: {e}"), 400

    if user != "admin" or password != "batman":
        return jsonify(message="Invalid user / password"), 403
    else:
        return jsonify(message="Authentication done"), 200


if __name__ == '__main__':
    app.run(port=11000)
