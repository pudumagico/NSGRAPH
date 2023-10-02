import os
from prompt_builder import PromptBuilder


class AbstractModel:
    def __init__(self, model_name: str, log_path: str = "../logs", use_survey_data: bool = False):
        self._model_name = model_name + ("_survey" if use_survey_data else "")
        self.__logfile = None
        self._setup_logfile(log_path)
        self.__get_prompts = PromptBuilder().survey_prompts if use_survey_data else PromptBuilder.generated_prompts

    def _setup_logfile(self, log_path):
        if not os.path.exists(log_path): os.makedirs(log_path)
        file_index = 1
        while os.path.exists(os.path.join(log_path, self._model_name + str(file_index) + ".csv")): file_index += 1
        self.__logfile = open(os.path.join(log_path, self._model_name + str(file_index) + ".csv"), "w+")
        self.__logfile.write("model, example_count, prompt_index, difficulty_index, solution, response\n")

    def _log_result(self, example_count: int, prompt_index: int, difficulty_index: int, solution: str, response: str):
        self.__logfile.write("; ".join([self._model_name, str(example_count), str(prompt_index), str(difficulty_index), solution, response]) + "\n")
        self.__logfile.flush()

    def _send_prompt(self, prompt: str) -> str:
        pass

    def close_logfile(self):
        if self.__logfile:
            self.__logfile.close()
            self.__logfile = None

    def run(self, skip_amount: int = 0):
        i = 0
        for example_count in range(1, 4):
            for prompt, prompt_index, solution, difficulty in self.__get_prompts(example_count):
                i += 1
                if i <= skip_amount: continue
                response = self._send_prompt(prompt).replace(";", ",")
                self._log_result(example_count, prompt_index, difficulty, solution, response)
