from abstract_model import AbstractModel
import replicate


class FlanT5XL(AbstractModel):
    def _send_prompt(self, prompt) -> str:
        response = replicate.run(
            "replicate/flan-t5-xl:7a216605843d87f5426a10d2cc6940485a232336ed04d655ef86b91e020e9210",
            input={
                "prompt": prompt,
                "max_length": 5000,
                "repetition_penalty": 0.01
            }
        )
        response = ' '.join(list(response)).replace("\n"," ")
        print(f"Response: {response}")
        return response
