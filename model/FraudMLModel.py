import pandas as pd
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
from matplotlib import pyplot as plt
from Final.model.Statistic import Statistic


class FraudMLModel(Statistic):
    def __init__(self, connector=None):
        super().__init__(connector)
        self.le = LabelEncoder()
        self.encoders = {}

    def processTransformByColumns(self, df, columns):
        for col in columns:
            x = df[col]
            df[col] = self.le.fit_transform(x)

    def processTransform(self):
        categorical_feature = ['gender', 'category', 'state','job']
        numerical_feature = ['Age', 'zip', 'amt']
        dropping = ['first','last','cc_num','lat','long','city_pop',
                         'unix_time','merch_lat','merch_long','trans_num','dob','merchant',
                         'trans_date_trans_time','street','city']
        result = ['is_fraud']
        self.dfTransform = self.df.copy(deep=True)
        self.dfTransform.drop(dropping, axis=1, inplace=True)
        # Khởi tạo và lưu encoder cho từng feature
        for col in categorical_feature:
            le = LabelEncoder()
            self.encoders[col] = le
            self.dfTransform[col] = le.fit_transform(self.dfTransform[col])
        for col in numerical_feature:
            self.dfTransform[col] = pd.to_numeric(
                self.dfTransform[col],
                errors='coerce')

            # Xử lý các cột phân loại
        for col in categorical_feature:
            self.dfTransform[col] = self.le.fit_transform(
                self.dfTransform[col].astype(str)  # Đảm bảo định dạng string
            )

        return self.dfTransform

    def _encode_input(self, input_dict):
        """Mã hóa các giá trị phân loại sử dụng encoder đã lưu"""
        encoded = {}

        # Mã hóa từng feature
        for feature in ['gender', 'category', 'state', 'job']:
            try:
                encoder = self.encoders[feature]
                encoded[feature] = encoder.transform([input_dict[feature]])[0]
            except KeyError:
                raise ValueError(f"Thiếu encoder cho feature: {feature}")
            except ValueError as e:
                raise ValueError(f"Giá trị không hợp lệ cho {feature}: {input_dict[feature]}") from e

        # Thêm các feature số
        encoded['Age'] = input_dict['Age']
        encoded['zip'] = input_dict['zip']
        encoded['amt'] = input_dict['amt']

        return encoded

    def buildCorrelationMatrix(self, df):
        plt.figure(figsize=(8, 6))
        df_corr = df.corr(numeric_only=True)  # Generate correlation matrix
        ax = sns.heatmap(df_corr, annot=True)
        plt.show()

