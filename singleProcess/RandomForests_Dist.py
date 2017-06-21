# coding=utf-8
import pickle
from random import randint

import datetime

from multiprocessing import Queue

from multiprocessing import Process
from time import sleep

from singleProcess.DataReader import readData, readDataAsGen
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
    """bagging 集成所有树的结果"""
    prediction_counter = {
        "0" : 0,
        "1" : 0
    }
    for tree in forests:
        one_prediction = predict_class_type(tree, one_data)
        prediction_counter[str(one_prediction)] += 1

    return int(max(prediction_counter.items(), key=lambda x : x[1])[0])

def get_sample_dataSet(dataSet, sample_ratio):
    """有放回地随机获取数据集"""
    sample_size = round(len(dataSet) * sample_ratio)
    sample_dataSet = []
    while len(sample_dataSet) < sample_size:
        random_index = randint(0, len(dataSet)-1)
        # print(random_index)
        sample_dataSet.append(dataSet[random_index])
    return sample_dataSet

def get_random_forest(dataSet, param, filename="rf.model", process_num=4):
    """训练随机森林，并返回模型"""
    # 配置参数
    tree_num = param["tree_num"]
    sample_radio = param["sample_radio"]
    feature_num =param["feature_num"]
    max_depth =param["max_depth"]
    min_size = param["min_size"]

    part_of_forest = []
    process_list = []
    one_proc_tree_num = round(tree_num / process_num)
    for i in range(process_num):
        one_queue = Queue()
        part_of_forest.append(one_queue)
        one_process = Process(target=build_tree_mulprocess, args=(dataSet, sample_radio, feature_num, max_depth, min_size, one_proc_tree_num, one_queue, "pro-" + str(i)))
        process_list.append(one_process)

    # 启动所有进程
    for one_process in process_list:
        one_process.start()


    print("here_0")


    while not (part_of_forest[0].qsize() == one_proc_tree_num and part_of_forest[1].qsize() == one_proc_tree_num and part_of_forest[2].qsize() == one_proc_tree_num and part_of_forest[3].qsize() == one_proc_tree_num):
        pass

    # 汇聚所有进程
    # for one_process in process_list:
    #     one_process.join()
    #     print("ha")


    print("here")

    # 集成所有进程的结果
    forest = []
    for one_part in part_of_forest:
        while not one_part.empty():
            forest.append(one_part.get())
    # 保存模型
    save_forest(filename, forest)
    return forest

def build_tree_mulprocess(dataSet, sample_radio, feature_num, max_depth, min_size, tree_num, part_of_forest, proc_name):
    """一个用于建树的进程"""
    print("[ Info ]: creating a new process ...")
    # sleep(5)
    for i in range(tree_num):
        print("------ " + proc_name +  " training tree :" + str(i + 1) + " ------")
        sample_dataSet = get_sample_dataSet(dataSet, sample_radio)
        tree = build_tree(sample_dataSet, feature_num, max_depth, min_size)
        part_of_forest.put(tree)
        print(proc_name + " ...........")
    print(proc_name + " end")




def predict(test_dataSet, forest=None, filename="rf.model"):
    if forest == None:
        print("[ Info ]: 使用已有模型进行预测")
        forest = load_forest(filename)
    else:
        print("[ Info ]: 训练新的模型进行预测")
    labels = []
    i = 0
    for one_data in test_dataSet:
        if i % 1000 == 0:
            print("----- predicting: " + str(i) + " -----")

        i += 1
        labels.append(bagging(forest, one_data))
    return labels

def accuracy(labels, test_dataSet):
    """计算正确率"""
    acc = 0
    i = 0
    for one_data in test_dataSet:
        if labels[i] == one_data[0]:
            acc += 1
        i += 1
    acc_percent = (float(acc) / i)
    print("正确数：" + str(acc))
    print("正确率：" + str(acc_percent))


def save_forest(filename, model):
    f = open(filename, "wb")
    pickle.dump(model, f)
    f.close()


def load_forest(filename):
    f = open(filename, 'rb')
    forest = pickle.load(f)
    f.close()
    return forest

def get_submission_file(labels, output_filename=None):
    if output_filename == None:
        output_filename = datetime.datetime.now().strftime('submission_%m_%d_%H_%M');
    file = open(output_filename, 'w')
    file.write("id,label\n")
    for i in range(len(labels)):
        one_line = str(i) + "," + str(labels[i]) + "\n"
        file.write(one_line)
    file.close()



if __name__ == '__main__':
    param = {
        "tree_num" : 1000,
        "sample_radio" : 0.08,
        "feature_num" : 30,
        "max_depth" : 5,
        "min_size" : 10
    }

    a_time = datetime.datetime.now()

    train_filename = "train_data_min.txt"
    test_filename = "train_data_100000.txt"
    train_dataSet = readData(train_filename)
    forest = get_random_forest(train_dataSet, param)

    test_dataSet = readDataAsGen(test_filename)
    test_dataSet_2 = readDataAsGen(test_filename)

    b_time = datetime.datetime.now()
    print("[ Info ]: 建树花费时间：" +str((b_time - a_time).seconds) + " s")


    # labels = predict(test_dataSet, forest)
    # print("----- 正在计算预测正确率 -----")
    # accuracy(labels, test_dataSet_2)
    #
    # print("----- 正在写入标签 -----")
    # get_submission_file(labels)


# 正确数：94651
# 正确率：0.94651