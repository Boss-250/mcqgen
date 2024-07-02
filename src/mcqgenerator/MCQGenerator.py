import os
from getpass import getpass
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
from langchain_ai21 import ChatAI21
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain

load_dotenv()

api_key = os.environ["AI21_API_KEY"]    



llm = ChatAI21(api_key = api_key, model = "jamba-instruct-preview", temprature = 0.7)

template = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
crete a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template
)

prompt1 = quiz_generation_prompt

key = output_key1 = "quiz"

quiz_chain = LLMChain = prompt1 | llm | key


template2 = """
You are an expert english grammarian and writer. Given a Multiple choice Quiz {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
if the quiz is not at per with the cognitive and analytical abilities of the student,\
update the quiz questions which need to be changed and change the tone such that it perfectly fits the student ablities.
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template2
)

prompt2 = quiz_evaluation_prompt

output_key2 = ["review"]

key2 = output_key2

review_chain = LLMChain = llm | prompt2 | key2


generate_evaluate_chain = SequentialChain(chains=[quiz_chain, review_chain], 
                                          input_variables=["text", "number", "subject", "tone", "response_json"],
                                          output_variables=["quiz", "review"],verbose=True)

