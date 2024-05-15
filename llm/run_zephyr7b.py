from model_implementations.Zephyr7bModel import Zephyr7bModel

m = Zephyr7bModel("Zephyr7b", use_survey_data=True)
m.run()
m.close_logfile()
