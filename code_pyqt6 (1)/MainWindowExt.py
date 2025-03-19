import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from Final.Chart.ChartHandle import ChartHandle
from Final.code_pyqt6.DatabaseConnectEx import DatabaseConnectEx
from Final.code_pyqt6.MainWindow import Ui_MainWindow
from Final.model.FraudLightGBM import FraudLightGBM
from Final.model.Statistic import Statistic


class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.FraudLightGBM = FraudLightGBM()
        self.Statistic = Statistic()
        self.databaseConnectEx=DatabaseConnectEx()
        self.databaseConnectEx.parent=self
        self.chartHandle= ChartHandle()


    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.verticalLayoutFunctions.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setupPlot()

        self.actionConnection.triggered.connect(self.openDatabaseConnectUI)
        self.pushButtonVD.clicked.connect(self.showData)

        self.pushButtonC.clicked.connect(self.showFraudByCategory)
        self.pushButtonG.clicked.connect(self.showFraudByGender)
        self.pushButtonSaG.clicked.connect(self.showFraudStateAndGender)
        self.pushButtonCaG.clicked.connect(self.showFraudByCategoryAndGender)
        self.pushButtonDoW.clicked.connect(self.showFraudByDoW)
        self.checkEnableWidget(False)

        self.pushButtonTrainModel.clicked.connect(self.processTrainModel)
        self.pushButtonEvaluate.clicked.connect(self.processEvaluateTrainedModel)
        self.pushButtonPredict.clicked.connect(self.processPrediction)

    def show(self):
        self.MainWindow.show()

    def showData(self):
        self.Statistic.connector = self.databaseConnectEx.connector
        self.Statistic.execFraud()
        df = self.Statistic.df
        self.showDataIntoTable(df)

    def checkEnableWidget(self,flag=True):
        self.pushButtonSaG.setEnabled(flag)
        self.pushButtonG.setEnabled(flag)
        self.pushButtonDoW.setEnabled(flag)
        self.pushButtonCaG.setEnabled(flag)
        self.pushButtonC.setEnabled(flag)

    def setupPlot(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)

        # adding tool bar to the layout
        self.verticalLayoutPlot.addWidget(self.toolbar)
        # adding canvas to the layout
        self.verticalLayoutPlot.addWidget(self.canvas)

    def openDatabaseConnectUI(self):
        dbwindow = QMainWindow()
        self.databaseConnectEx.setupUi(dbwindow)
        self.databaseConnectEx.show()

    def showDataIntoTableWidget(self,df):
        self.tableWidgetD.setRowCount(0)
        self.tableWidgetD.setColumnCount(len(df.columns))
        for i in range(len(df.columns)):
            columnHeader = df.columns[i]
            self.tableWidgetD.setHorizontalHeaderItem(i, QTableWidgetItem(columnHeader))
        row = 0
        for item in df.iloc:
            arr = item.values.tolist()
            self.tableWidgetD.insertRow(row)
            j=0
            for data in arr:
                self.tableWidgetD.setItem(row, j, QTableWidgetItem(str(data)))
                j=j+1
            row = row + 1

    def showDataIntoTable(self,df):
        self.tableWidgetData.setRowCount(0)
        self.tableWidgetData.setColumnCount(len(df.columns))
        for i in range(len(df.columns)):
            columnHeader = df.columns[i]
            self.tableWidgetData.setHorizontalHeaderItem(i, QTableWidgetItem(columnHeader))
        row = 0
        for item in df.iloc:
            arr = item.values.tolist()
            self.tableWidgetData.insertRow(row)
            j=0
            for data in arr:
                self.tableWidgetData.setItem(row, j, QTableWidgetItem(str(data)))
                j=j+1
            row = row + 1

    def showFraudByCategory(self):
        self.FraudLightGBM.connector = self.databaseConnectEx.connector
        self.FraudLightGBM.execFraud()
        self.FraudLightGBM.processCategoryDistribution()
        print(self.FraudLightGBM.dfCategory)

        df = self.FraudLightGBM.dfCategory

        self.showDataIntoTableWidget(df)

        columnLabel = "category"
        columnStatistic = "count"
        title = "Categories Distribution"
        legend = False
        self.chartHandle.visualizePieChart(self.figure,self.canvas,df, columnLabel, columnStatistic, title, legend)

    def showFraudByGender(self):
        self.FraudLightGBM.connector = self.databaseConnectEx.connector
        self.FraudLightGBM.execFraud()
        df = self.FraudLightGBM.processGenderDistribution()
        self.showDataIntoTableWidget(df)
        columnLabel = "gender"
        columnStatistic = "count"
        title = "Gender Distribution"
        legend = False
        self.chartHandle.visualizePieChart(self.figure,self.canvas,df, columnLabel, columnStatistic, title, legend)

    def showFraudByDoW(self):
        try:
            self.FraudLightGBM.connector = self.databaseConnectEx.connector
            self.FraudLightGBM.execFraud()
            df = self.FraudLightGBM.processFraudByDoW()

            self.showDataIntoTableWidget(df)
            columnLabel = "dow"
            columnStatistic = "is_fraud"
            title = "Number of Transaction by Day of Week"
            hue = None
            self.chartHandle.visualizeLinePlotChart(self.figure, self.canvas, df, columnLabel, columnStatistic, title, hue)
        except:
            traceback.print_exc()

    def showFraudStateAndGender(self):
        self.FraudLightGBM.connector = self.databaseConnectEx.connector
        self.FraudLightGBM.execFraud()
        df = self.FraudLightGBM.processStateGender()
        self.showDataIntoTableWidget(df)
        columnLabel = "state"
        columnStatistic = "count"
        hue="gender"
        title = "Distribution gender and state"
        self.chartHandle.visualizeMultiBarChart(self.figure,self.canvas,df, columnLabel, columnStatistic,hue, title)

    def showFraudByCategoryAndGender(self):
        self.FraudLightGBM.connector = self.databaseConnectEx.connector
        self.FraudLightGBM.execFraud()
        df = self.FraudLightGBM.processGenderAndCategoryCounter()
        self.showDataIntoTableWidget(df)
        df=self.FraudLightGBM.df
        columnLabel = "category"
        columnStatistic = "count"
        hue="gender"
        title = "Distribution gender and category"
        self.chartHandle.visualizeMultiBarChart(self.figure,self.canvas,df, columnLabel, columnStatistic,hue, title)

    def processTrainModel(self):
        columns_input=['gender', 'Age', 'zip', 'job', 'state', 'category', 'amt']
        column_target="is_fraud"
        test_size=float(self.lineEditTestSize.text())/100
        random_state=int(self.lineEditRandomState.text())
        self.FraudLightGBM = FraudLightGBM()
        self.FraudLightGBM.connector = self.databaseConnectEx.connector
        self.FraudLightGBM.processTrain(
            columns_input,
            column_target,
            test_size,
            random_state)
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Info")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setText("Train machine learning model successful!")
        buttons = QMessageBox.StandardButton.Yes
        dlg.setStandardButtons(buttons)
        button = dlg.exec()
    def processEvaluateTrainedModel(self):
        result = self.FraudLightGBM.evaluate()
        self.lineEditTP.setText(str(result.TP))
        self.lineEditTN.setText(str(result.TN))
        self.lineEditFP.setText(str(result.FP))
        self.lineEditFN.setText(str(result.FN))
        self.lineEditAcc.setText(str(result.Acc))
        self.lineEditR.setText(str(result.R))
        self.lineEditFS.setText(str(result.F1S))
        self.lineEditP.setText(str(result.P))


    def processPrediction(self):
        try:
            gender = self.lineEditG.text()
            Age = int(self.lineEditA.text())
            zip = int(self.lineEditZ.text())
            job = self.lineEditJT.text()
            state = self.lineEditS.text()
            amt = float(self.lineEditATM.text())
            category = self.lineEditC.text()

            predicted_price = self.FraudLightGBM.predictIs_fraud(gender, Age, amt, zip, job, state, category)
            self.lineEditPredictedPrice.setText(str(predicted_price[0]))
        except:
            traceback.print_exc()