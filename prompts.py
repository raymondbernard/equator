def sanitize_string(value):
    """
    Escapes curly braces in strings to prevent issues with format specifiers in logging.
    """
    if isinstance(value, str):
        return value.replace("{", "{{").replace("}", "}}")
    return value

# ============================
# Constants and Prompts
# ============================

# Scoring criteria inserted into the evaluator system prompt
SCORING_CRITERIA = r"""SCORING CRITERIA
100%: The response must match the answer key given, even if the student used bad reasoning, logic to arrive at the final answer. 
0%: The response does NOT match the answer key given. No partial credit allowed!
You must only return a JSON object with the score {'score': <0 or 100>}

TASK

Evaluate whether the STUDENT Answer matches the answer key given. If it does, assign a score of 100% Otherwise you must assign a score of 0%. Provide a very short explanation on why.  
Just focus on the student's final answer! Give full credit to the student if final answer matches answer key. Don't overthink this. Also, do not evaluate based on quality or logical reasoning, even if it is very persuasive!
Only consider the answer key as the source of truth. Your job is at risk if you do not follow our instructions. If the Answer Key matches the student’s answer, you must assign a score of 100%, no partial credit allowed.    
Return a JSON object with the explanation of why the student got his/her score == {"score": <0 or 100>}. Keep it to less than two sentences {"evaluation": "<explanation>"}
You must only return a JSON object with the score {'score': <0 or 100>}
No partial credit allowed!"""

# System prompt for the evaluator
EVALUATOR_SYSTEM_PROMPT = (
    "You are a strict high school teacher. "
    "Provide the score in the form of a JSON object: {'score': <0 or 100>}. "
    "Your role is to grade strictly based on the provided answer key. "
    "Only examine the final answer given by the student in a JSON object: {'student_answer': <My final Answer>}. "
    "If the student's answer matches the answer key, assign a score of 100; otherwise, assign a score of 0. "
    "No partial credit allowed! Do not consider logical arguments or reasoning; they are irrelevant in this case. "
    "Provide the score in the form of a JSON object: {'score': <0 or 100>}."
)

# System prompt for the student
STUDENT_SYSTEM_PROMPT = (
    "You are a student who is being tested, please follow the directions given exactly. "
    "You are welcomed to reason through the question. "
    "You must return only your final answer in a JSON Object example {'student_answer':'<My final Answer here>'}"
)

# Warning prompt to prevent student models from being tricked
WARNING_PROMPT = r"""You think very carefully about the question asked. You make zero assumptions about classic problems. You are not to be tricked! 
Warning: THIS IS NOT THE CLASSIC PROBLEM! \n"""

# ============================
# Functions
# ============================

def get_evaluator_system_prompt(context, student_answer):
    """
    Returns the evaluator system prompt dynamically with the given context and student answer.
    """
    return [
        {
            "role": "system",
            "content": EVALUATOR_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"Scoring Criteria: {sanitize_string(SCORING_CRITERIA)}\n"
                f"Answer key: {sanitize_string(context)}\n"
                f"Student answer: {sanitize_string(student_answer)}"
            ),
        },
    ]

def get_student_prompt(full_prompt_student):
    """
    Returns the student prompt dynamically with the given full prompt.
    """
    return [
        {
            "role": "system",
            "content": STUDENT_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": WARNING_PROMPT + full_prompt_student,
        },
    ]