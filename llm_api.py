from groq import Groq
import json
import os
from dotenv import load_dotenv
from prompts import prompt_for_coding,prompt_for_mcq,prompt_for_text_question,feedback_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat(content):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content" : "Just go along with what the user is saying"
            },
            {
                "role": "user",
                "content": content
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content



def callgroq(user_prompt,system_prompt):
    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[
            {
                    "role": "system",
                    "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.8,
        max_completion_tokens=1910,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )
    answer = completion.choices[0].message.content

    return answer


def generate_question(topic,type):
    user_prompt = "user given topic = {topic}".format(topic=topic)
    if type=="MCQ":
        answer = callgroq(user_prompt,prompt_for_mcq)
    elif type=='TEXT':
        answer = callgroq(user_prompt,prompt_for_text_question)
    else:
        answer = callgroq(user_prompt,prompt_for_coding)
    parsed = json.loads(answer)
    # print(parsed)
    return parsed



"""
Generating prompt for question analysis
"""





def generate_question_feedback(questions,score):
    user_prompt = "" + "\n\n" + json.dumps({"responses": questions,"scores": score}, indent=2)
    answer = callgroq(user_prompt,feedback_prompt)
    parsed = json.loads(answer)
    return parsed



assignment_feedback_system_prompt = """
Role:
You are an academic evaluator.

Input Format:
The user will provide:
•⁠  ⁠An assignment question (what was asked).
•⁠  ⁠A full assignment answer (student's entire submission as a single string).

Output Format (Strictly respond in this JSON format):
{
  "score_summary": "<e.g., Good effort. Score: 7 out of 10>",
  "what_was_good": "<Brief highlights of strengths in the answer>",
  "what_was_missing_or_wrong": "<Brief areas that need improvement>",
  "suggestions": [
    "<Tip 1>",
    "<Tip 2>"
  ]
}

Rules:
•⁠  ⁠Evaluate the entire assignment holistically (do NOT evaluate question-by-question).
•⁠  ⁠Be concise, constructive, and positive.
•⁠  ⁠Avoid repeating the student’s exact words.
•⁠  ⁠Do NOT include any text outside the JSON object.
"""





def generate_assugnment_feedback(question,answer):
    user_prompt = """
Assignment Question:
{assignment_question}

Assignment Answer:
\"\"\"
{assignment_answer}
\"\"\"
""".format(assignment_answer = answer,assignment_question = question)
    
    answer = callgroq(user_prompt,assignment_feedback_system_prompt)
    parsed = json.loads(answer)
    return parsed
    

    


    
# print(generate_question("OS"))
# generate_question("os")
