from groq import Groq
import json

client = Groq()
topic = "DBMS" 

prompt = """Give me a json object containing a question,list of 4 options and answer.
            Generate ONE multiple choice question from the topic: {topic}.
            The question must be from {topic} subject.
            Format strictly as follows:
            {{
            Question: <your question>
            Options: [ <option A>,<option B>,<option C>,<option D> ] 
            Answer: <correct option text only>
            tags: <list of all topics of given question>
            }}
            """.format(topic = topic)
completion = client.chat.completions.create(
    model="llama-3.2-90b-vision-preview",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0,
    max_completion_tokens=1910,
    top_p=1,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
)

answer = completion.choices[0].message.content
parsed = json.loads(answer)

print(parsed)
