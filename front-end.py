import streamlit as st
import json
from test_boilerplate_code_gen_spike import main

st.header("Test Case Boilerplate Generator")

test_case_description = st.text_input("Test Case Description")
programming_language = st.text_input(
    "Programming Language")
tool = st.text_input(
    "Tool")

if st.button("Generate boilerplate"):
    with st.spinner("Generating..."):
        result = json.loads(
            main(test_case_description, programming_language, tool))
        for key, value in result.items():
            key = " ".join(key.split("_")).capitalize()
            with st.expander(key):
                if type(value) == list:
                    for element in value:
                        st.write(element)
                else:
                    st.code(value)
