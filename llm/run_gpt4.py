from model_implementations.GPT4Model import GPT4Model

token = "<token>"
m = GPT4Model("GPT 4", token, use_survey_data=True)
m.run()
m.close_logfile()