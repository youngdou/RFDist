# coding=utf-8
from random import randint

from singleProcess.DataReader import readData


def get_gini_index(leftDataSet, rightDataSet):
    """
    计算基尼系数（数据集的不纯度），越小说明分得越准确
    :param leftDataSet:
    :param rightDataSet:
    :return:
    """
    gini_value = 0
    # 二分类问题 0，1
    classes = [0, 1]
    for class_value in classes:
        left_size = len(leftDataSet)
        right_size = len(rightDataSet)
        if left_size != 0:
            class_sum = [row[0] for row in leftDataSet].count(class_value)
            prop = 1.0 * class_sum / left_size
            gini_value += (prop * (1.0 - prop))
        if right_size != 0:
            class_sum = [row[0] for row in rightDataSet].count(class_value)
            prop = 1.0 * class_sum / right_size
            gini_value += (prop * (1.0 - prop))
    return gini_value

def get_features(feature_num, all_feature_num=133):
    """
    随机选取 feature_num 个特征，用于建新的树
    :param feature_num:
    :param all_feature_num:
    :return:
    """
    features = []
    while(len(features) < feature_num):
        random_feature = randint(0, all_feature_num-1)
        if random_feature not in features:
            features.append(random_feature)
    return features

def data_split(dataSet, index, value):
    """
    跟据特征分隔数据集
    :param dataSet:
    :param index:
    :param value:
    :return:
    """
    left_dateSet = []
    right_dataSet = []
    for one_data in dataSet:
        if one_data[index] < value:
            left_dateSet.append(one_data)
        else:
            right_dataSet.append(one_data)
    return left_dateSet, right_dataSet

def get_best_node(dataSet, features):
    """
    跟据基尼系数选取最优特征
    然后进行数据集的分隔
    :param dateSet:
    :param features:
    :return:
    """
    temp_index, temp_value, temp_left, temp_right = 0, 0, None, None
    temp_gini_index = 1000000
    for one_feature in features:
        for one_data in dataSet:
            left_dataSet, right_dataSet = data_split(dataSet, one_feature, one_data[one_feature])
            gini_index = get_gini_index(left_dataSet, right_dataSet)
            if gini_index < temp_gini_index:
                temp_gini_index = gini_index
                temp_index = one_feature
                temp_value = one_data[one_feature]
                temp_left = left_dataSet
                temp_right = right_dataSet
    tree_node = {
        "index" : temp_index,
        "value" : temp_value,
        "left" : temp_left,
        "right" : temp_right
    }
    return tree_node

#决定输出标签
def get_class_type(node_data):
    """
    获取结点的类型
    :param node_data:
    :return:
    """
    output=[row[0] for row in node_data]
    return max(set(output),key=output.count)

def sub_spilt(root,feature_num,max_depth,min_size,depth):
    """分裂获得树"""
    left=root['left']
    right=root['right']
    del(root['left'])
    del(root['right'])

    if not left or not right:
        root['left']=root['right']=get_class_type(left+right)
        #print 'testing'
        return
    if depth > max_depth:
        root['left']=get_class_type(left)
        root['right']=get_class_type(right)
        return

    if len(left) < min_size:
        root['left']=get_class_type(left)
    else:
        features = get_features(feature_num)
        root['left'] = get_best_node(left,features)
        #print 'testing_left'
        sub_spilt(root['left'],feature_num,max_depth,min_size,depth+1)

    if len(right) < min_size:
        root['right']=get_class_type(right)
    else:
        features = get_features(feature_num)
        root['right'] = get_best_node(right,features)
        #print 'testing_right'
        sub_spilt(root['right'],feature_num,max_depth,min_size,depth+1)

def build_tree(dataSet,feature_num,max_depth,min_size):
    features = get_features(feature_num)
    root=get_best_node(dataSet,features)
    sub_spilt(root,feature_num,max_depth,min_size,1)
    return root

# if __name__ == '__main__':
#     dataSet = readData("train_data_min.txt")
#     root = build_tree(dataSet, 5, 10, 10)
    # print(str(root))






















