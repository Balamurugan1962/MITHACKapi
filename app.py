from flask import Flask,jsonify
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app,origins=['*'])
api = Api(app)


Init_put = reqparse.RequestParser()
Init_put.add_argument("Test",location = 'form',help='Give Text for the test')


class Init(Resource):
    def get(self):
        return jsonify({"Reply": "Hosted successfully"})
    
    def post(self):
        data = Init_put.parse_args()
        reply = {}
        reply["Test"] = data["Test"]
        return jsonify(reply)
    

api.add_resource(Init,'/')

if __name__ == "__main__":
    app.run(host="0.0.0.0",port='5002')