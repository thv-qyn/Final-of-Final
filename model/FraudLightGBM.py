import pandas as pd
from imblearn.over_sampling import SMOTE
from lightgbm import LGBMClassifier
from sklearn.metrics import confusion_matrix, precision_score, \
    recall_score, f1_score, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder

from Final.model.FraudMLModel import FraudMLModel
from Final.model.MetricsResult import MetricsResult
from Final.model.TrainedModel import TrainedModel


class FraudLightGBM(FraudMLModel):
    def __init__(self,connector=None):
        super().__init__(connector)
        self.le = LabelEncoder()
        self.sc_std = StandardScaler()

    def processTrain(
            self,
            columns_input,
            column_target,
            test_size,
            random_state,
            sampling_strategy='auto',
    ):

        self.execFraud()
        self.processTransform()

        print("\nKiểu dữ liệu các cột:")
        print(self.dfTransform.dtypes)

        print("\nMẫu dữ liệu đầu vào:")
        print(self.dfTransform.head(3))

        y = self.dfTransform[column_target].values.ravel()
        X = self.dfTransform[columns_input].astype(int)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state
        )

        # Bước 2: Chuẩn hóa dữ liệu GỐC (trước khi resample)
        self.sc_std = StandardScaler()
        X_train_scaled = self.sc_std.fit_transform(self.X_train)
        X_test_scaled = self.sc_std.transform(self.X_test)

        # Bước 3: Áp dụng SMOTE trên dữ liệu ĐÃ CHUẨN HÓA
        smote = SMOTE(
            sampling_strategy=sampling_strategy,
            random_state=random_state
        )
        self.X_train_res, self.y_train_res = smote.fit_resample(
            X_train_scaled,  # Đã chuẩn hóa
            self.y_train
        )

        # Bước 4: Chuyển về DataFrame và giữ tên cột
        self.X_train_res = pd.DataFrame(
            self.X_train_res,
            columns=self.X_train.columns
        )
        self.X_test_scaled = pd.DataFrame(
            X_test_scaled,
            columns=self.X_test.columns
        )

        # Tìm tham số tối ưu bằng GridSearch
        param_grid = {
            'n_estimators': [200,300],
            'num_leaves': [ 31,62],
            'max_depth': [7,9],
            'learning_rate': [0.05, 0.1],
            'is_unbalance': [True]
        }

        grid_search = GridSearchCV(
            estimator=LGBMClassifier(
                random_state=random_state,
                verbose=-1,
                force_row_wise=True  # Thêm dòng này
            ),
            param_grid=param_grid,
            scoring='f1',
            cv=3,
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(self.X_train_res, self.y_train_res)

        # Lưu model và thông tin
        self.model = grid_search.best_estimator_
        print(f"🔥 Best model parameters: {grid_search.best_params_}")
        print(f"🔥 Best model parameters: {grid_search.best_estimator_}")
        self.trainedmodel = TrainedModel()
        self.trainedmodel.model = self.model
        self.trainedmodel.X_train = self.X_train_res
        self.trainedmodel.X_test = self.X_test_scaled
        self.trainedmodel.y_train = self.y_train_res
        self.trainedmodel.y_test = self.y_test
        self.trainedmodel.columns_input = columns_input
        self.trainedmodel.column_target = column_target

    def evaluate(self):
        pred = self.model.predict(self.X_test_scaled)
        cm = confusion_matrix(self.y_test, pred)

        # Trích xuất giá trị từ confusion matrix
        TN, FP, FN, TP = cm.ravel()

        # Tính các chỉ số
        Acc = accuracy_score(self.y_test, pred)
        P = precision_score(self.y_test, pred)
        R = recall_score(self.y_test, pred)
        F1S = f1_score(self.y_test, pred)

        # Sửa thứ tự tham số theo đúng định nghĩa class MetricsResult
        return MetricsResult(
            TruePositive=TP,
            FalsePositive=FP,
            TrueNegative=TN,
            FalseNegative=FN,
            accuracy=Acc,
            f1_score=F1S,
            recall=R,
            percision=P  # Lưu ý: Sửa thành precision nếu có typo trong class
        )
    def predictIs_fraud(self,gender,Age,amt,zip,job,state,category):
        # Tạo dict input
        input_data = {
            'gender': gender,
            'Age': Age,
            'zip': zip,
            'job': job,
            'state': state,
            'category': category,
            'amt': amt
        }

        # Mã hóa dữ liệu
        try:
            encoded_data = self._encode_input(input_data)
        except ValueError as e:
            print(f"Lỗi mã hóa: {str(e)}")
            return None

        # Tạo DataFrame
        data = pd.DataFrame([[
            encoded_data['gender'],
            encoded_data['Age'],
            encoded_data['zip'],
            encoded_data['job'],
            encoded_data['state'],
            encoded_data['category'],
            encoded_data['amt']
        ]], columns=self.trainedmodel.columns_input)
        input_transform = self.sc_std.transform(data)
        pred = self.predict(input_transform)
        return pred
    def predict(self,columns_input):
        pred = self.model.predict(columns_input)
        return pred

