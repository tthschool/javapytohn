from openai import OpenAI
import os
import time
from data import question ,update_anwser , mess

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
        tools=[{"type": "retrieval"}],
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
    answer_list = []
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for each in messages.data:
                answer_list.append(each.content[0].text.value)
            break
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
        for k , v in questions.items():
            key = k
            value = v
        thead = create_thread(client = client)
        create_message = create_messages(thread=thead , client= client , question= value)
        run =run_mess(thread= thead , assistant= assistant , client=client)
        message = retrieve(thread= thead , client= client , run= run)
        # print(message[0])
        print(message)
        if key != 0 :
            session = update_anwser(key , message[0])

    # print(mess(key))



