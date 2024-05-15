from abstract_model import AbstractModel
import requests

BEARER = "" # Insert bearer token from huggingface

API_URL = "" # Insert API URL or use public rate limited API below
headers = {
	"Accept" : "application/json",
	"Authorization": "Bearer " + BEARER,
	"Content-Type": "application/json" 
}
# API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
# headers = {"Authorization": "Bearer " + BEARER}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if (response.status_code != 200): 
        print("Statuscode", response.status_code)
        print("Content", response.content)
        raise ValueError
    return response.json()

class Zephyr7bModel(AbstractModel):
    no_answers = []
    answers = []
    i = 0
    def _send_prompt(self, prompt) -> str:
        *prompt, question = prompt.split('\n')
        prompt = '\n'.join(prompt[:-1]) + "\nQ: \"" + question + "\"\nA: "
        self.i += 1
        print(f"Sending prompt {self.i}")
        try: response = query({"inputs": prompt, "parameters": {"return_full_text": False}})[0]['generated_text']
        except ValueError:
            print("No Answers:", self.no_answers)
            print("Answers:", self.answers)
            print("Max len with answer:", max(b for _,b in self.answers))
            if self.no_answers: print("Min len with no answer:", min(b for _,b in self.no_answers))
            else: print("Everything answered!")
            print("Stopped at i", self.i)
            exit()
        if not response.strip():
            # print("Input:", prompt)
            # print("Output empty")
            print("i", self.i)
            self.no_answers.append((self.i, len(prompt)))
        else: self.answers.append((self.i, len(prompt)))
        return response

# No Answers: [(2, 1727), (4, 1720), (5, 1730), (7, 1722), (8, 1736), (9, 1736), (12, 1707), (15, 1704), (18, 1706), (19, 1712)]