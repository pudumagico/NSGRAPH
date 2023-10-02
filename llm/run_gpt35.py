from model_implementations.GPT3_5Model import GPT35Model

token = "<token>"

m = GPT35Model("GPT 3.5", token, use_survey_data=True)
m.run()
m.close_logfile()
