import os
from dotenv import find_dotenv, load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field

load_dotenv(find_dotenv())

llm = ChatOpenAI(   
    openai_api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo")

boilerplate_prompt = """\
You are an AI expert in writing the boilerplate code for the test case description given as {test_case_description} using \
{tool} in {programming_language} language. Adhere to the following rules\

RULES:\
1. All the dynamic values, locators, urls must be replaced with some placeholders like SEARCH_TEXT, LOCATOR, URL etc based on the test case description.\
2. Ensure that the code is both syntactically and semantically correct.\
3. List all the key concepts used in the test case boilerplate code that will make it easier to understand.\
4. List all the potential error scenarios that may occur during the implementation of this boilerplate code and throughout its execution.\
"""

boilerplate_prompt_template = PromptTemplate(template=boilerplate_prompt,
                                             input_variables=["test_case_description", "tool", "programming_language"])

chain_1 = LLMChain(llm=llm, prompt=boilerplate_prompt_template)

boilerplate_formatting_prompt = """
Response:
{response}

Formatting instructions:
{formatting_instructions}

MAKE SURE THAT SCHEMA FORMAT IS NOT RETURNED
"""

boilerplate_formatting_prompt_template = PromptTemplate(template=boilerplate_formatting_prompt, input_variables=[
    "response", "formatting_instructions"])

chain_2 = LLMChain(llm=llm, prompt=boilerplate_formatting_prompt_template)


class BoilerplateCodeParser(BaseModel):
    programming_language: str = Field(
        "Programming language used to generate boilerplate code for a given test case description")
    tool: str = Field(
        "Tool used to generate boilerplate code for a given test case description")
    code: str = Field(
        "Boilerplate code for the test case that aligns with the test description")
    concepts_with_description: list[str] = Field(
        "useful concepts with description used in test code")
    possible_errors_with_description: list[str] = Field(
        "possible errors with description that may occur during test code implementation and its execution")


parser = PydanticOutputParser(pydantic_object=BoilerplateCodeParser)


def main(test_case_description, programming_language, tool):
    response_1 = chain_1.run({
        "test_case_description": test_case_description,
        "tool": tool,
        "programming_language": programming_language,
    })

    response_2 = chain_2.run({
        "response": response_1,
        "formatting_instructions": parser.get_format_instructions()
    })

    return response_2

