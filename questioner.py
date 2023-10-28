import os
import requests
import json
import time

def send_and_receive(question, url):
    headers = {'Content-Type': 'application/json'}
    data = {'q': question}
    response = requests.post(url,headers=headers,json=data)
    return response


def get_last_message(url):
    response = requests.get(url)
    if response.status_code == 200 and response.text:
        return response
    return 'No valid response received'

def main():
    questions_folder = "questions"
    answers_folder = "answers"
    service_url = "http://localhost:8081"
    suffix1="Podaj w kilku słowach nazwę metody jaką można rozwiązać ten problem"
    suffix2="Podaj równania i nierówności potrzebne do rozwiązania tego problemu"
    suffix3="Rozwiąź to zadanie" 
    if not os.path.exists(answers_folder):
        os.makedirs(answers_folder)

    for filename in os.listdir(questions_folder):
        question_file_path = os.path.join(questions_folder, filename)
        answer_file_path = os.path.join(answers_folder, filename)
        if not os.path.exists(answer_file_path):
            f = open(answer_file_path,'w')
            f.close

        with open(question_file_path, 'r') as question_file, open(answer_file_path, 'a') as answer_file:
            answer_file.write(f"{suffix2}::\n")
            for id,line in enumerate(question_file):
                line = line.strip()
                if line:
                     # Sending question and getting the answer
                    response = send_and_receive(f"{line} \\n {suffix2}" , f"{service_url}/chat")
                    # Podaj nazwę metody jaką można rozwiązać ten problem
                    # Writing the answer to the answer file
                    print(response)

                    # Sleeping for 30 seconds
                    time.sleep(10)

                    # Getting the last message
                    last_message = get_last_message(f"{service_url}/lastmsg")

                    answer_file.write(str(last_message.text) + '\n')
                    
                    # Printing the last message
                    print(f"{filename}:line:{id} Last Message: {last_message.text}")
                    # print(last_message.content)
                    # print(last_message.apparent_encoding)
                    # print(last_message.raw)
                    # print(last_message.json)


    print("Processing complete.")

if __name__ == "__main__":
    main()
