import tiktoken, json, openai
from datetime import datetime
import consts
import json
from tools import serp_api
import ast




encoding = tiktoken.encoding_for_model("gpt-3.5-turbo" if not consts.USE_GPT4 else "gpt-4")


def openai_call(prompt, temperature=0.8, max_tokens=0, role="assistant"):
    messages = [
        {
            "role": "system",
            "content": f"You are BabyAGI-asi, an Autonomous and Self-Improving LLM-based agent. There are no users, just BabyAGI. Strictly follow your objective. Today's date: {datetime.now().strftime('%d/%m/%Y')}. Knowledge cut-off: set/2021. When writing code you cannot write comments before or after the code, neither you can wrap the codes in `` code blocks. Just write the code in the required language, if you need to add comments, add inside the code, in the language comment format, if possible."
            if role == "assistant"
            else "You are BabyAGI-asi, you must strictly follow the user's intructions",
        },
        {"role": role, "content": prompt},
    ]
    #print(prompt)
    output_lenght = 4000-count_tokens(str(messages)) if not consts.USE_GPT4 else 8000 - count_tokens(messages) if max_tokens == 0 else max_tokens
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo" if not consts.USE_GPT4 else "gpt-4",
        messages=messages,
        temperature=temperature,
        max_tokens=output_lenght,
        n=1,
    )
    text = response.choices[0].message.content.strip()
    return text


def count_tokens(text):
    return len(encoding.encode(str(text)))


def split_answer_and_cot(text):
    if consts.VIEWER:
        print("*************************")
        print(text)
        print("*************************")
    cot = ast.literal_eval(text)["chain of thoughts"]
    code = ast.literal_eval(text)["answer"] 

    if consts.VIEWER:
        print("=-=-=-=-=-=-=-=-=-=")
        print(code)
        print("=-=-=-=-=-=-=-=-=-=")
    return [code, cot]


def get_oneshots():
    one_shots, p_one_shots = [], []
    with open('src/memories/one-shots.json', 'r') as f:
        one_shots += json.loads(f.read())

    with open('src/memories/private-one-shots.json', 'r') as f:
        p_one_shots += json.loads(f.read())

    return one_shots, p_one_shots

def recover_fields(namedoc):
    response = serp_api.get_erp_api_result('get_doc', doctype="DocType", name=namedoc)
    fields = []
    for fld in response["fields"]:
        if fld["fieldtype"] != "Section Break" and fld["fieldtype"] != "Column Break":
            fields.append(fld["fieldname"])   
    return fields

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True