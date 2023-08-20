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
story_system_role = "You are an experienced travel agent specialising in South Australian holidays."
story_prompt = "Write an engaging story (3 paragraphs) about a hypothetical holiday based on the following. There will be a description of the holiday customers, an example of a previous holiday, then some ideas for the proposed holiday, then chatgpt will generate a marketing/sales influenced story about how the proposed holiday could play out, including at least 3 key sights, places or activities the customer might enjoy."
# llm = openai(temperature=0)
# create a chat completion

def get_openAI_summary(inDat):
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt + str(inDat)}])
    return chat_completion.choices[0].message.content

def get_openAI_story(token_count,customers="Not specified, assume a family from South Australia.",previous="Not specified, assume they enjoyed their last holiday which included wine tasting, good food, swimming at pristine beaches and enjoying unspoiled natural environments.",proposed="An exciting holiday in South Australia for about 2 weeks, starting in Adelaide and using their own car to see interesting sights."): #Didn't end up needing the token count since max_tokens seems to be on the completion tokens anyway
    story_input = """
Holiday Customer:{}
Previous holidays, sights and activities:{}
Proposed holiday ideas:{}
Generate a potential holiday story 3 paragraphs long, about 500 words in total:
""".format(customers,previous,proposed)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",max_tokens=600, messages=[{"role": "system", "content": story_system_role}, {"role": "user", "content": story_input}])
    return chat_completion.choices[0].message.content

def get_key_activities(story):
    prompt="""
Given the following story you generated for this customer, list the key activities and places mentioned in the story, prioritising things that might require bookings or enquiries. Where possible, combine each activity with the relevant place. Put each activity and place succinctly on a new line. One activity and place per line - max 10 lines.

Story:
"""
    activities=openai.ChatCompletion.create(model="gpt-3.5-turbo",max_tokens=300, messages=[{"role": "system", "content": story_system_role}, {"role": "user", "content": prompt}])
    return activities.choices[0].message.content