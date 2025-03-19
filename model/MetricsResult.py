class MetricsResult:
    def __init__(self,TruePositive,FalsePositive,TrueNegative,FalseNegative,accuracy,f1_score,recall,percision):
        self.TP = TruePositive
        self.FP = FalsePositive
        self.TN = TrueNegative
        self.FN = FalseNegative
        self.Acc = accuracy
        self.F1S = f1_score
        self.R = recall
        self.P = percision
    def __str__(self):
        return (
            f"TP = {self.TP}\n"
            f"FP = {self.FP}\n"
            f"TN = {self.TN}\n"
            f"FN = {self.FN}\n"
            f"Accuracy = {self.Acc * 100:.2f}%\n"
            f"F1 Score = {self.F1S * 100:.2f}%\n"
            f"Recall = {self.R * 100:.2f}%\n"
            f"Precision = {self.P * 100:.2f}%"
        )
