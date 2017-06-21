# coding=utf-8
import pickle
from random import randint

from singleProcess.DataReader import readData
from singleProcess.DecisionTree import build_tree


def predict_class_type(decision_tree, one_test_data):
    """根据决策树进行预测"""
    if one_test_data[decision_tree["index"]] < decision_tree["value"]:
        left_node = decision_tree["left"]
        if type(left_node) == int:
            return left_node
        else:
            return predict_class_type(left_node, one_test_data)
    else:
        right_node = decision_tree["right"]
        if type(right_node) == int:
            return right_node
        else:
            return predict_class_type(decision_tree["right"], one_test_data)

def bagging(forests, one_data):
    prediction_counter = {
        "0" : 0,
        "1" : 0
    }
    for tree in forests:
        one_prediction = predict_class_type(tree, one_data)
        prediction_counter[str(one_prediction)] += 1
    print(str(prediction_counter))
    print(int(max(prediction_counter.items(), key=lambda x : x[1])[0]))
    return int(max(prediction_counter.items(), key=lambda x : x[1])[0])

def get_sample_dataSet(dataSet, sample_ratio):
    """有放回地随机获取数据集"""
    sample_size = round(len(dataSet) * sample_ratio)
    sample_dataSet = []
    while len(sample_dataSet) < sample_size:
        random_index = randint(0, len(dataSet)-1)
        print(random_index)
        sample_dataSet.append(dataSet[random_index])
    return sample_dataSet

def get_random_forest(dataSet, param, filename="rf.model"):
    """训练随机森林，并返回模型"""
    # 配置参数
    tree_num = param["tree_num"]
    sample_radio = param["sample_radio"]
    feature_num =param["feature_num"]
    max_depth =param["max_depth"]
    min_size = param["min_size"]

    forest = []
    for i in range(tree_num):
        sample_dataSet = get_sample_dataSet(dataSet, sample_radio)
        tree = build_tree(sample_dataSet, feature_num, max_depth, min_size)
        forest.append(tree)
    # 保存模型
    save_forest(filename, forest)
    return forest

def predict(test_dataSet, forest=None, filename="rf.model"):
    if forest == None:
        forest = load_forest(filename)
    labels = []
    for one_data in test_dataSet:
        labels.append(bagging(forest, one_data))
    acc, acc_percent = accuracy(labels, test_dataSet)
    print("正确数：" + str(acc))
    print("正确率：" + str(acc_percent))
    return labels

def accuracy(labels, test_dataSet):
    acc = 0
    for i in range(len(test_dataSet)):
        if labels[i] == test_dataSet[i][0]:
            acc += 1
    return acc, (float(acc) / len(test_dataSet))


def save_forest(filename, model):
    f = open(filename, "wb")
    pickle.dump(model, f)
    f.close()

def load_forest(filename):
    f = open(filename, 'rb')
    forest = pickle.load(f)
    f.close()
    return forest


if __name__ == '__main__':
    param = {
        "tree_num" : 10,
        "sample_radio" : 0.5,
        "feature_num" : 10,
        "max_depth" : 5,
        "min_size" : 3
    }

    train_filename = "train_data_min.txt"
    test_filename = "train_data_min.txt"
    dataSet = readData("train_data_min.txt")
    # forest = get_random_forest(dataSet)
    predict(dataSet)

