from abstract_model import AbstractModel
from bardapi import Bard
from time import sleep
import random


class BardModel(AbstractModel):
    def __init__(self, modelname: str, token: str, token2: str = None, **kwargs):
        self.__bard = Bard(token, timeout=100)
        self.__bard2 = Bard(token, timeout=100) if token2 else None
        super().__init__(modelname, **kwargs)

    def _send_prompt(self, prompt) -> str:
        sleeptime = 30 + random.randint(3, 10)
        print(f"Sending next request in {sleeptime} seconds")
        sleep(sleeptime)
        ec = 0
        response = self.__bard.get_answer(prompt)["content"]
        while response.startswith("Response Error"):
            ec += 1
            sleeptime = 10 * ec + random.randint(2, 6) + 30
            print(f"Retrying for the {ec}th time in {sleeptime} seconds.")
            sleep(sleeptime)
            response = self.__bard.get_answer(prompt)["content"]
            if ec == 10 and self.__bard2:
                print(f"Probably being rate limited now. Switching Bard client")
                self.__bard, self.__bard2 = self.__bard2, self.__bard
                ec = 0
            if ec > 20:
                print(f"There seems to be a major issue. The last response was: {response}")
                print(f"exiting now")
                exit()
            if ec > 10:
                print(f"Probably being rate limited now. Waiting for 10 Minutes until next request")
                sleep(10 * 60)

        print(f"Reponse: {response[:25]}...")
        return response
