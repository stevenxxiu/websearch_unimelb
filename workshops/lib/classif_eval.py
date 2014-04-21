
class ConfusionMatrix:
    def __init__(self, tp, fp, tn, fn):
        self.tp = tp
        self.fp = fp
        self.tn = tn
        self.fn = fn

    @classmethod
    def generate(cls, predict_y, test_y):
        tp = fp = tn = fn = 0
        for predict_class, test_class in zip(predict_y, test_y):
            if predict_class == 1 and test_class == 1:
                tp += 1
            elif predict_class == 1 and test_class == 0:
                fp += 1
            elif predict_class == 0 and test_class == 1:
                fn += 1
            elif predict_class == 0 and test_class == 0:
                tn += 1
        return cls(tp, fp, tn, fn)

    def accuracy(self):
        tp, fp, tn, fn = self.tp, self.fp, self.tn, self.fn
        try:
            return (tp+tn)/(tp+fp+tn+fn)
        except ZeroDivisionError:
            return 0

    def f1(self, beta=1.0):
        tp, fp, tn, fn = self.tp, self.fp, self.tn, self.fn
        try:
            return ((1 + beta**2)*tp)/((1 + beta**2)*tp + beta**2*fn + fp)
        except ZeroDivisionError:
            return 0
