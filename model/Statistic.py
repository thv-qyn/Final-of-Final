from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
class Statistic:
    def __init__(self,connector=None):
        self.connector = connector
        self.lasted_df=None
    def execFraud(self,tableName=None):
        if tableName==None:
            sql="select * from fraud"
        else:
            sql = "select * from %s"%tableName
        self.df=self.connector.queryDataset(sql)
        self.lasted_df=self.df
        return self.df
    def printHead(self,row):
        print(self.df.head(row))
    def printTail(self,row):
        print(self.df.tail(row))
    def printInfo(self):
        print(self.df.info())
    def printDecsribe(self):
        print(self.df.describe())
    def dateProcessing(self):
        self.df['trans_date_trans_time'] = pd.to_datetime(self.df['trans_date_trans_time'] , format = '%d/%m/%Y')
        self.df['month'] = self.df['trans_date_trans_time'].dt.month
        self.df['year'] = self.df['trans_date_trans_time'].dt.year
        self.df['dow'] = self.df['trans_date_trans_time'].dt.day_name()
        self.lasted_df = self.df
    def processGenderDistribution(self):
        self.dfGender = self.df.gender.value_counts().reset_index()
        self.lasted_df = self.dfGender
        return self.dfGender
    def processAgeDistribution(self):
        self.dfAges = self.df.Age.value_counts().reset_index()
        self.dfAges.sort_values(by=['Age'], ascending=True, inplace=True)
        self.lasted_df = self.dfAges
        return self.dfAges

    def visualizePieChart(self,df,columnLabel,columnStatistic,title,legend=True):
        explode=[0.1]
        for i in range(len(df[columnLabel])-1):
            explode.append(0)
        plt.figure(figsize=(8, 6))
        plt.pie(df[columnStatistic], labels=df[columnLabel], autopct='%1.2f%%',explode=explode)
        if legend:
            plt.legend(df[columnLabel])
        plt.title(title)
        plt.show()
    def visualizePlotChart(self,df,columnX,columnY,title):
        plt.figure(figsize=(8, 6))
        plt.plot(df[columnX], df[columnY])
        plt.legend([columnX,columnY])
        plt.title(title)
        plt.xlabel(columnX)
        plt.ylabel(columnY)
        plt.grid()
        plt.show()
    def processCategoryDistribution(self):
        self.dfCategory = self.df.category.value_counts().reset_index()
        self.lasted_df = self.dfCategory
        return self.dfCategory
    def processGenderAndCategoryCounter(self):
        self.df_gender_order = self.df[['gender', 'category']]\
                                   .groupby(['gender', 'category'])\
                                   .value_counts()\
                                   .reset_index(name="count")
        self.lasted_df = self.df_gender_order
        return self.df_gender_order
    def visualizeCountPlot(self,df,columnX,columnY,hueColumn,title):
        plt.figure(figsize=(8, 6))
        ax=sns.countplot(x=columnX,hue=hueColumn,data=df)
        plt.title(title)
        plt.xlabel(columnX)
        plt.ylabel(columnY)
        plt.grid()
        plt.legend()
        plt.show()
    def visualizeBarPlot(self,df,columnX,columnY,hueColumn,title,alpha=0.8,width=0.6):
        plt.figure(figsize=(8, 6))
        plt.ticklabel_format(useOffset=False, style='plain')
        ax=sns.barplot(data=df,x=columnX,y=columnY,hue=hueColumn,alpha=alpha,width=width)
        plt.title(title)
        plt.xlabel(columnX)
        plt.ylabel(columnY)
        plt.grid()
        plt.legend()
        plt.show()
    def visualizeBarChart(self,df,columnX,columnY,title):
        plt.figure(figsize=(8, 6))
        plt.ticklabel_format(useOffset=False, style='plain')
        plt.bar(df[columnX],df[columnY])
        plt.title(title)
        plt.xlabel(columnX)
        plt.ylabel(columnY)
        plt.grid()
        plt.show()
    def visualizeScatterPlot(self,df,columnX,columnY,title):
        plt.figure(figsize=(8, 6))
        plt.ticklabel_format(useOffset=False, style='plain')
        sns.scatterplot(data=df,x= columnX,y=columnY)
        plt.title(title)
        plt.xlabel(columnX)
        plt.ylabel(columnY)
        plt.grid()
        plt.show()
    def processState(self):
        self.dfState = self.df['state'].value_counts().reset_index(name="count").rename(columns={"index": "state"})
        self.lasted_df = self.dfState
        return self.dfState
    def processis_Fraud(self):
        self.dfIF = self.df['is_fraud'].value_counts().reset_index(name="count").rename(columns={"index": "is_fraud"})
        self.lasted_df =self.dfIF
        return  self.dfIF

    def processStateGender(self):
        self.dfSG = self.df[['gender', 'state']]\
                                   .groupby(['gender', 'state'])\
                                   .value_counts()\
                                   .reset_index(name="count")
        self.lasted_df = self.dfSG
        return self.dfSG
    def visualizeLinePlotChart(self,df,columnX,columnY,tile,hue=None):
        plt.figure(figsize=(8, 6))
        plt.ticklabel_format(useOffset=False,style="plain")
        sns.lineplot(data=df,x=columnX, y=columnY, marker='o', color='orange',hue=hue)
        plt.xlabel(columnX)
        plt.ylabel(columnY)
        plt.title(tile)
        plt.legend(loc='upper right')
        plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.show()

    def processFraudByDoW(self):
        self.dfFDoW = self.df.copy(deep=True)
        self.dfFDoW['trans_date_trans_time'] = pd.to_datetime(self.dfFDoW['trans_date_trans_time'],
            format='%Y-%m-%d %H:%M:%S')
        self.dfFDoW['dow'] = self.dfFDoW['trans_date_trans_time'].dt.day_name()

        self.dfFDoW = self.dfFDoW.groupby(['dow'], as_index=False).agg({'is_fraud': 'sum'})
        return self.dfFDoW