from openai import OpenAI
import os
import time
import json
from data import question ,update_anwser , mess
from tools import tools_list , get_stock_price , get_weather
def create_client():
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPEN_AI_ORG")
    )
    return client

def create_assistant(client):
    assistant = client.beta.assistants.create(
        instructions= "you are friendly chatbot",
        model="gpt-4-1106-preview",
        tools= tools_list,
        # file_ids=[file_id]
    )
    return assistant

def create_thread(client):
    thread = client.beta.threads.create()
    return thread

def create_messages(client , thread , question):
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )
def run_mess(client , assistant , thread):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    return run
def retrieve(thread , client,run):
    tool_call = []
    answer_list = []
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for each in messages.data:
                answer_list.append(each.content[0].text.value)
            break
        elif run_status.status == 'requires_action' :
            print("requied action") 
            required_action  = run_status.required_action.submit_tool_outputs.tool_calls
            print(required_action)
            function_list = []
            for each in required_action:
                if each.function.name == "get_stock_price":
                    print(each.function.name)
                    function_call = each.function.name
                    argument = each.function.arguments
                    argument = json.loads(argument)
                    symbol = argument['symbol']
                    output_list = get_stock_price(symbol)
                    tool_call.append({
                        "tool_call_id" : each.id,
                        "output": output_list
                    })

                    print(output_list)
                elif each.function.name == "get_weather":
                    a = each.function.arguments
                    argument = json.loads(a)
                    location = argument["location"]
                    output_list = get_weather(location)
                    output = json.dumps(output_list)
                    tool_call.append({
                        "tool_call_id": each.id,
                        "output": output
                    })
              
                print(tool_call)
            client.beta.threads.runs.submit_tool_outputs(
            thread_id= thread.id,
            run_id= run.id,
            tool_outputs=tool_call
            )
        else:
            print(run_status.status)
            time.sleep(3)
    return answer_list

# def main():
#     print("hl")

# main()
if __name__ == "__main__":
    key = 0
    value = ""
    client = create_client()
    assistant = create_assistant(client=client)
    while True:
        questions = question()
        if questions != None and questions != 0:
            for k , v in questions.items():
                key = k
                value = v
            print(value)
            thead = create_thread(client = client)
            create_message = create_messages(thread=thead , client= client , question= value)
            run =run_mess(thread= thead , assistant= assistant , client=client)
            message = retrieve(thread= thead , client= client , run= run)
            print(message[0])
            print(message)
            if key != 0 :
                session = update_anwser(key , message[0]) 
        else:
            print("no data")
            time.sleep(2)
    print(mess(key))



