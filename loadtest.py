import pickle

# load the model from disk
# loaded_model = pickle.load(open('컨테이너수송량예측.sav', 'rb'))
# result = loaded_model.predict([[2021, 10, 1, 40, 1]]).round(2)
# print(result)

loaded_model = pickle.load(open('정박지대기율예측.sav', 'rb'))
result = loaded_model.predict([[30.028, 3, 1, 10.2, 359.0, 81.0, 2.7, 1.2, 1, 1, 5.0, 7]]).round(2)
print(result * 100) #퍼센트값이라 *100해줫으면 좋겟음