from abstract_model import AbstractModel
import replicate


class Vicuna13bModel(AbstractModel):
    def _send_prompt(self, prompt) -> str:
        response = replicate.run(
            "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
            input={
                "prompt": prompt,
                "max_length": 5000
            }
        )
        response = ' '.join(list(response)).replace("\n"," ")
        print(f"Response: {response}")
        return response
