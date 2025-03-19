from Final.Connectors.Connector import Connector
from Final.model.FraudMLModel import FraudMLModel

connector=Connector(server="localhost",port=3306,database="fraud",username="root",password="Huygia@123")
connector.connect()
pm=FraudMLModel(connector)
pm.execFraud()

dfTransform=pm.processTransform()
print(dfTransform.head())
pm.buildCorrelationMatrix(dfTransform)