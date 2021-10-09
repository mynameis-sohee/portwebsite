import pickle

# load the model from disk
# loaded_model = pickle.load(open('컨테이너수송량예측.sav', 'rb'))
# result = loaded_model.predict([[2021, 10, 1, 40, 1]]).round(2)
# print(result)

loaded_model = pickle.load(open('정박지대기율예측.sav', 'rb'))
result = loaded_model.predict([[2021, 10, 1, 40, 1]]).round(2)
print(result)