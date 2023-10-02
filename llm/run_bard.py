from model_implementations.BardModel import BardModel

token = "XwhH-hzTHk3qFYEmbol1ZL5P4WrrYWXcc3EbvDUMrPDRGoNbvV2z5_15IqLDE6zCKL1rEw."
token2 = "XwhH-kSkuNADBnk9pcvsAG3AZj3Zp7F9NqU5k01XzvYexYnTO79kc6nLbZq3rLOu5L48-g."

bard = BardModel("Bard", token, token2=token2, use_survey_data=True)
bard.run()
bard.close_logfile()