# coding=utf-8
from singleProcess.DataReader import readData


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
    return int(max(prediction_counter.items(), key=lambda x : x[1])[0])


if __name__ == '__main__':
    tree = {'index': 92, 'value': 91.0, 'left': {'index': 27, 'value': 4.0, 'left': {'index': 110, 'value': 3789142.0, 'left': {'index': 43, 'value': 5.0, 'left': {'index': 33, 'value': 1.0, 'left': {'index': 18, 'value': 1.0, 'left': {'index': 125, 'value': 0, 'left': 1, 'right': 1}, 'right': 0}, 'right': 0}, 'right': 0}, 'right': 0}, 'right': 0}, 'right': {'index': 107, 'value': 137652471.09548613, 'left': {'index': 68, 'value': 0, 'left': 0, 'right': 0}, 'right': 0}}

    dataSet = readData("train_data_min.txt")
    for one_data in dataSet:
        print(predict_class_type(tree, one_data))
