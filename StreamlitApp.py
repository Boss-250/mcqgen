import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

with open("/home/kube/mcqgen/Response.json","r") as file:
    

    RESPONSE_JSON = json.loads(file.read())

st.title("MCQs Creator Application with langchain 🦜️🔗")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a pdf or txt file")

    mcq_count= st.number_input("No. of MCQs", min_value = 3, max_value = 50)

    subject = st.text_input("Insert object", max_chars = 20)

    tone = st.text_input("Complexity Level of Questions", max_chars = 20, placeholder = "Simple")

    button = st.form_submit_button("Create MCQs")

    if button and  uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."): 
            try:
               text = read_file(uploaded_file)
               response = generate_evaluate_chain(text = text,mcq_count=mcq_count,subject=subject,tone=tone,)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

        if isinstance(response, dict):    
            quiz = response.get("quiz", None)
            if quiz is not None:
                table_data = get_table_data(quiz)
            if table_data is not None:
                df=pd.DataFrame(table_data)
                df.index = df.index +1 
                st.table(df)

                st.text_area(label = "Review", value = response["review"])
            else:
                st.error("Error in the table data")
        else:
            st.write(response)      