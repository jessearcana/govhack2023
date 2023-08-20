import os
# from langchain.llms import OpenAI
import openai


if os.environ.get("OPENAI_API_KEY") is None:
    # try to load it from a file
    try:
        with open("openai_api_key.txt", "r") as f:
            os.environ["OPENAI_API_KEY"] = f.read()
    except:
        raise("OPENAI_API_KEY not set and cannot read key from openai_api_key.txt")

prompt = "write an engaging story about a hypothetical family holiday based on the following. There will be a description of the holiday customers, an example of a previous holiday, then some ideas for the proposed holiday, then chatgpt will generate a marketing/sales influenced story about how the proposed holiday could play out. Holiday Customers:" 

# llm = openai(temperature=0)
# create a chat completion



def get_openAI_summary(inDat):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt + str(inDat)}])
    return chat_completion.choices[0].message.content


# get_openAI_summary([])