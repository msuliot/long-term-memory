import os
import sys
import json
from colorama import Fore, Style, init
from mongo_helper import MongoHelper
import msuliot.openai_helper as oai # https://github.com/msuliot/package.helpers.git

# OpenAI Chat model
model_for_openai_chat = "gpt-4o"

# Initialize colorama
init()

# Load environment variables
from env_config import envs
env = envs()

# Short Term Memory and Long Term Memory global variables
stm = []
ltm = []

# color print functions
def print_green(text):
    print(Fore.GREEN + text + Style.RESET_ALL)

def print_cyan(text):
    print(Fore.CYAN + text + Style.RESET_ALL)

def print_yellow(text):
    print(Fore.YELLOW + text + Style.RESET_ALL)

def print_blue(text):
    print(Fore.BLUE + text + Style.RESET_ALL)

def print_red(text):
    print(Fore.RED + text + Style.RESET_ALL)

def print_magenta(text):
    print(Fore.MAGENTA + text + Style.RESET_ALL)

def display_color(color, text):
    return color + text + Style.RESET_ALL  

# Message functions
def add_to_STM(message):
    global stm
    for m in message:
        stm.append(m)

def add_to_LTM(message):
    global ltm
    for m in message:
        ltm.append(m)

def create_message(role, content):
    json_message = {
        "role": role, 
        "content": content
    }
    return json_message

# Memory functions
def get_long_term_memory(mongo, pid):
    conversations = mongo.summary_find(pid)

    if conversations:
        message= []
        for conversation in conversations['conversations']:
            content = f"conversation date: {conversation['date']}, summary: {conversation['summary']}"
            message.append(create_message("user", content))

        add_to_LTM(message)

    print("Get Long Term Memory from MongoDB for", pid)


def save_short_term_memory(message):
    add_to_STM(message)
    print("Save Question and Answer to Short Term Memory")


# simulate login
def login():
    uid = input(display_color(Fore.GREEN,"Please enter your User ID: "))
    if not uid:
        return
    print(f"Validating User ID {uid}")
    return uid

# Converstion functions
def conversation_end(mongo, cid, pid):
    print_magenta(f"Thank you, Have a great day?")
    print_cyan(f"End: Conversation ID: {cid}")
    
    if not stm:
        print_blue("Short Term Memory is empty, removing temporary conversation")
        mongo.conversation_delete(cid)
        return
    else:
        the_summary = create_conversation_summary(cid, pid)
        mongo.summary_update(cid, pid, the_summary)
 

def create_conversation_summary(cid, pid):
    print_cyan(f"Save Long Term Memory conversation summary in MongoDB for {pid} with Conversation ID: {cid}")
    oaic = oai.openai_chat(env.openai_key, model_for_openai_chat)
    content = "Summarize all questions and answers from this conversation by documenting the facts for later recall in future conversations. \nTry to keep the summary to three hundred characters or less.\n"
    
    for m in stm:
        content += m["content"] + "\nQuestion: " + m["content"] + "\nAnswer: " + m["content"] + "\n"
    
    oaic.add_message("user", content)
    # oaic.execute_stream()
    response = oaic.execute()
    return response


# Greeting functions and question
def initial_greeting(profile):
    print_magenta(f"Welcome to the AI Chatbot, {profile["name"]}! How can I help you today?")


def get_question():
    question = input(display_color(Fore.GREEN,"question:> "))
    return question


# OpenAI Chat functions
def get_chat_completion_messages(conbine_message):

    oaic = oai.openai_chat(env.openai_key, model_for_openai_chat)
    oaic.add_message("system", "you are an AI system created to answer questions accurately, and precise. Try to keep responses to 500 characters.")
    for m in conbine_message:
        oaic.add_message(m["role"], m["content"])

    response = oaic.execute() 
    print("Calling ChatGPT sending Short Term Memory + Question")
    print("Answer from ChatGPT")
    return response


def main():
    global stm, ltm
    mongo = MongoHelper()
    os.system('clear') # Clear the screen on MacOS and Linux

    # Simulate Login
    uid = login()
    if not uid:
        print_red("User ID is required")
        sys.exit()

    # # Get user profile
    profile = mongo.profile_find(uid)
    if not profile:
        print_red(f"Profile not found for {uid}")
        sys.exit()

    # Get Profile
    profile_id = str(profile['_id'])
    print("Profile ID:", profile_id)
    
    # Start conversation
    conversation_id = mongo.conversation_create(profile_id)
    print("Conversation ID:", conversation_id)

    # Get long term memory
    get_long_term_memory(mongo, profile_id)
    
    # Main loop to get user questions and provide answers
    while True:
        message = []
        question = get_question() 

        if question in ("exit", "quit", "bye", "end", "done", "thanks"):
            conversation_end(mongo, conversation_id, profile_id)
            break
        if question == "stm":
            pretty_json = json.dumps(stm, indent=2)
            print(pretty_json)
            continue
        if question == "ltm":
            pretty_json = json.dumps(ltm, indent=2)
            print(pretty_json)
            continue

        message.append(create_message("user", question))
        conbine_message = ltm + stm + message

        response = get_chat_completion_messages(conbine_message)
        message.append(create_message("assistant", response))

        save_short_term_memory(message)
        mongo.conversation_update(conversation_id, create_message("user", question))
        mongo.conversation_update(conversation_id, create_message("assistant", response))
        
        print(Fore.YELLOW + "Answer:", response + Style.RESET_ALL)


if __name__ == "__main__":
    main()