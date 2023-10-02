from model_implementations.Vicuna13bModel import Vicuna13bModel

m = Vicuna13bModel("Vicuna 13b", use_survey_data=True)
m.run()
m.close_logfile()