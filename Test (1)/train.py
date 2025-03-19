from Final.Connectors.Connector import Connector
from Final.model.FraudLightGBM import FraudLightGBM

connector=Connector(server="localhost",port=3306,database="fraud",username="root",password="Huygia@123")
connector.connect()
pm=FraudLightGBM(connector=connector)
pm.processTrain(
    ['gender', 'Age', 'zip', 'job', 'state', 'category', 'amt'],
    'is_fraud',0.2,0)

#pm.processTrain(["gender","age","payment_method"],"price")
#pm.visualizeActualAndPredictResult()
eresult=pm.evaluate()
print(eresult)

# Dự đoán
prediction = pm.predictIs_fraud(
'M',
     45,
     120.58,
     16314,
     'Retail merchandiser',
     'PA',
     'food_dining')

print(prediction)