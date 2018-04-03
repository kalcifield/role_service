from flask import Flask, request, jsonify
import json
from database import Dynamodb

with open("../config.json") as json_data:
    config = json.load(json_data)

app = Flask(__name__)


@app.route('/api/roles/load', methods=['POST'])
def load_role():
    user_id = request.json["userId"]
    db = Dynamodb()
    roles = db.load(user_id)
    return jsonify({"roles": roles})


if __name__ == '__main__':
    app.run(host=config["host"], port=config["port"], debug=True)
