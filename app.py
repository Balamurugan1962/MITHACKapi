from flask import Flask,jsonify
from flask_restful import Api,Resource

app = Flask(__name__)
api = Api(app)


class Init(Resource):
    def get(self):
        return jsonify({"Reply": "Hosted successfully"})
    

api.add_resource(Init,'/')

if __name__ == "__main__":
    app.run(host="0.0.0.0",port='5002')