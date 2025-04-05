from flask import Flask,jsonify
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS
from llm_api import generate_question,generate_question_feedback,generate_assugnment_feedback,chat
from werkzeug.datastructures import FileStorage
from pdfParsing import parse_PDF

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
getAssignmentFeedback_post_parse.add_argument("Question",type=FileStorage,location='files',required=True,help="PDF file is required")
getAssignmentFeedback_post_parse.add_argument("Answer",type=FileStorage,location='files',required=True,help="PDF file is required")

class getAssignmentFeedback(Resource):
    def post(self):
        data = getAssignmentFeedback_post_parse.parse_args()
        Answer_pdf_file = data["Answer"]
        Question_pdf_file = data["Question"]
        
        Answer_extracted_text = parse_PDF(Answer_pdf_file)
        Question_extracted_text = parse_PDF(Question_pdf_file)
        feedback = generate_assugnment_feedback(Question_extracted_text,Answer_extracted_text)
        return jsonify(feedback)
    
api.add_resource(getAssignmentFeedback,'/getAssignmentFeedback')








"""
Bellow function is for Quiz Feedback analysis
"""
getQuizFeedback_post_parse = reqparse.RequestParser()

getQuizFeedback_post_parse.add_argument("Questions", type=dict, action='append', location='json', help="Provide list of question objects",required=True)
getQuizFeedback_post_parse.add_argument("Score", type=int, action='append', location='json', help="Provide list of integer scores",required=True)

class getQuizFeedback(Resource):
    def post(self):
        data = getQuizFeedback_post_parse.parse_args()
        responce = generate_question_feedback(data["Questions"],data["Score"])
        return responce
    
api.add_resource(getQuizFeedback,'/getQuizFeedback')

"""
Bellow function is for ChatBot
"""
ChatBot_post_parse = reqparse.RequestParser()
ChatBot_post_parse.add_argument("Message",type = str,location='form',help = "Send the messeges",required=True)
class ChatBot(Resource):
    def post(self):
        args = ChatBot_post_parse.parse_args()
        reply = chat(args["Message"])
        print(reply)
        return jsonify({"reply" : reply})

    def get(self):
        return jsonify({"Hello":"Hiii"})
    
api.add_resource(ChatBot,'/ChatBot')






if __name__ == "__main__":
    app.run(host="0.0.0.0",port='5003')