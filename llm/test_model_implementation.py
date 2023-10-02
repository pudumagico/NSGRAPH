from abstract_model import AbstractModel as __AbstractModel


class TestModel(__AbstractModel):
    def _send_prompt(self, prompt) -> str:
        return "This is a mock Model"
