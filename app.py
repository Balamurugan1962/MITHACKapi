from flask import Flask,jsonify
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS
from llm_api import generate_question,generate_question_feedback

app = Flask(__name__)
cors = CORS(app,origins=['*'])
api = Api(app)



"""
Bellow function is for Generating Question analysis
"""
getQuestion_post_parse = reqparse.RequestParser()
getQuestion_post_parse.add_argument("Topic",type=str,location = 'form',help='Give the topic',required= True)
getQuestion_post_parse.add_argument("Type",type=str,location = 'form',help='Give the Type',required= True)

#For Genenrating the questions
class getQuestion(Resource):
    def get(self):
        return jsonify({"Reply": "Hosted successfully"})
    
    def post(self):
        data = getQuestion_post_parse.parse_args()
        responce = generate_question(data["Topic"],data["Type"])

        return responce
    

api.add_resource(getQuestion,'/getQuestions')




"""
Bellow function is for Assignment Feedback analysis
"""


getAssignmentFeedback_post_parse = reqparse.RequestParser()
# getAssignmentFeedback_post_parse.add_argument("Topic",)

class getAssignmentFeedback(Resource):
    def post(self):
        return jsonify({"Message" : "NOT Yet ready"})
    
api.add_resource(getAssignmentFeedback,'/getAssignmentFeedback')

getAssignmentFeedback_post_parse = reqparse.RequestParser()







"""
Bellow function is for Quiz Feedback analysis
"""
getQuizFeedback_post_parse = reqparse.RequestParser()

getQuizFeedback_post_parse.add_argument("Questions", type=dict, action='append', location='json', help="Provide list of question objects")
getQuizFeedback_post_parse.add_argument("Score", type=int, action='append', location='json', help="Provide list of integer scores")

class getQuizFeedback(Resource):
    def post(self):
        request = getQuizFeedback_post_parse.parse_args()
        responce = generate_question_feedback(request["Questions"],request["Score"])
        return responce
    
api.add_resource(getQuizFeedback,'/getQuizFeedback')
    






if __name__ == "__main__":
    app.run(host="0.0.0.0",port='5002')