"""
This is a dummy web app with only 1 end-point.

The app runs on port 10000
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    """
    This end-point has the form:

    /?id={VALUE}

    Returns:
    - 404: if 'id' value is different of '9'
    - 200: if 'id' value is '9'
    - 400: if 'id' value doesn't exits
    """
    input_id = request.args.get("id", None)

    if not input_id:
        return "id value is needed", 400

    if input_id == "9":
        return "found!", 200
    else:
        return "Not found data for this value", 404


if __name__ == '__main__':
    app.run(port=10000)
