
class ConfusionMatrix:
    def __init__(self, tp, fp, tn, fn):
        self.tp = tp
        self.fp = fp
        self.tn = tn
        self.fn = fn

    @classmethod
    def generate(cls, classif_classes, test_classes, pos_class, neg_class):
        tp = fp = tn = fn = 0
        for classif_class, test_class in zip(classif_classes, test_classes):
            if classif_class == pos_class and test_class == pos_class:
                tp += 1
            elif classif_class == pos_class and test_class == neg_class:
                fp += 1
            elif classif_class == neg_class and test_class == pos_class:
                fn += 1
            elif classif_class == neg_class and test_class == neg_class:
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
