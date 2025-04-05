from flask import Flask,jsonify
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS
from llm_api import generate_question

app = Flask(__name__)
cors = CORS(app,origins=['*'])
api = Api(app)


getQuestion_put_parse = reqparse.RequestParser()
getQuestion_put_parse.add_argument("Topic",type=str,location = 'form',help='Give the topic',required= True)
getQuestion_put_parse.add_argument("Type",type=str,location = 'form',help='Give the Type',required= True)


class getQuestion(Resource):
    def get(self):
        return jsonify({"Reply": "Hosted successfully"})
    
    def post(self):
        data = getQuestion_put_parse.parse_args()
        responce = generate_question(data["Topic"],data["Type"])

        return responce
    

api.add_resource(getQuestion,'/getQuestions')

if __name__ == "__main__":
    app.run(host="0.0.0.0",port='5002')