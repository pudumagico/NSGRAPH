from model_implementations.GPT4AllModel import GPT4AllModel

m = GPT4AllModel("GPT4ALL", use_survey_data=True)
m.run()
m.close_logfile()