from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


topic = "DBMS" 

prompt_for_mcq = """
You are a smart MCQ generator.

Generate FIVE **new** multiple choice questions from the topic: **'user given topic'**.

Each question must:
- Be from a **different sub-topic** of 'user given topic'.
- Be **unique** and not repeated from past calls.
- Have **4 options**.
- Have the **correct answer text** only (no letter/number).
- Include a **list of tags** related to the sub-topic.

Output ONLY in strict JSON format:
{
  "Questions": [
    {
      "Question": "<your question>",
      "Options": ["<option A>", "<option B>", "<option C>", "<option D>"],
      "Answer": "<correct option text only>",
      "tags": ["<tag1>", "<tag2>", ...]
    },
    ...
  ]
}

Ensure the questions vary **every time**, even for the same topic. Introduce randomness or shuffle sub-topics internally if needed.
"""

prompt_for_coding = """Generate a coding problem in the following JSON format:
{
  "question_type": "coding",
  "question": "<Write the problem statement here>",
  "test_cases": [
    {
      "input": "<test input 1>",
      "output": "<expected output 1>"
    },
    {
      "input": "<test input 2>",
      "output": "<expected output 2>"
    }
  ],
  "tags": ["<relevant tag 1>", "<tag 2>", "<difficulty level>"]
}
The question should be related to the topic: **user given topic**.
Include 2–3 test cases, including edge cases and make sure the problem is original and beginner-friendly.
Strictly output in the above JSON format only.
 }}
 """

prompt_for_text_question="""
Generate a text-based theory question in the following JSON format only:

{{
  "question_type": "text",
  "question": "<Insert a conceptual or theoretical question here>",
  "answer": "<Insert the correct answer to the question here>"
}}

The question must be from the topic: **user given topic**.
Do not add any explanation or text outside the JSON.
Keep the answer concise and correct.
"""



def callgroq(topic,system_prompt):
    user_prompt = "user given topic = {topic}".format(topic=topic)
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

    if type=="MCQ":
        answer = callgroq(topic,prompt_for_mcq)
    elif type=='TEXT':
        answer = callgroq(topic,prompt_for_text_question)
    else:
        answer = callgroq(topic,prompt_for_coding)
    parsed = json.loads(answer)
    # print(parsed)
    return parsed

# print(generate_question("OS"))
# generate_question("os")
