from Final.Connectors.Connector import Connector
from Final.model.Statistic import Statistic

connector=Connector(server="localhost",port=3306,database="fraud",username="root",password="Huygia@123")
connector.connect()
pm=Statistic()
pm.connector=connector
pm.execFraud()
dfGender=pm.processGenderDistribution()
print(dfGender)
pm.visualizePieChart(dfGender,"gender","count","Gender Distribution")

dfCategory=pm.processCategoryDistribution()
print(dfCategory)
pm.visualizePieChart(dfCategory,"category","count","Categories Distribution",legend=False)

dfGenderCategory=pm.processGenderAndCategoryCounter()
print(dfGenderCategory)
pm.visualizeCountPlot(pm.df,"category","amt","gender","Distribution gender and category")
