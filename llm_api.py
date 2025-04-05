from groq import Groq
import json
import os
from dotenv import load_dotenv
from prompts import prompt_for_coding,prompt_for_mcq,prompt_for_text_question,feedback_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


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

    
# print(generate_question("OS"))
# generate_question("os")
