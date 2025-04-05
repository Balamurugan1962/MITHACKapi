feedback_prompt = """
You are an educational assistant.

Given:
•⁠  ⁠A list of questions with correct answers and user answers.
•⁠  ⁠A list of binary scores (1 = correct, 0 = incorrect).

Generate overall feedback for the learner in this JSON format:

{
  "score_summary": "<e.g., You got 3 out of 5 correct.>",
  "weak_topics_summary": "<Brief summary of what topics the learner struggled with.>",
  "feedback": "<Constructive feedback to encourage and guide improvement.>",
  "suggestions": [
    "<Short tip 1>",
    "<Short tip 2>"
  ]
}

Be concise, positive, and helpful.
"""




prompt_for_mcq = """
You are a smart MCQ generator.

Generate GIVEN NUMBER OF **new** multiple choice questions from the topic: **'user given topic'**.

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




prompt_for_coding = """Generate GIVEN NUMBER OF coding problem in the following JSON format:
{
"Questions": [
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
  ]
}
The question should be related to the topic: **user given topic**.
Include 2–3 test cases, including edge cases and make sure the problem is original and beginner-friendly.
Strictly output in the above JSON format only.
 }}
 """




prompt_for_text_question="""
Generate GIVEN NUMBER OF text-based theory question in the following JSON format only:
"Questions": [
    {{
  "question_type": "text",
  "question": "<Insert a conceptual or theoretical question here>",
  "answer": "<Insert the correct answer to the question here>"
}}, ....
]

The question must be from the topic: **user given topic**.
Do not add any explanation or text outside the JSON.
Keep the answer concise and correct.
"""

