# coding=utf-8


def get_gini_index(leftDataSet, rightDataSet):
    """计算基尼系数（数据集的不纯度），越小说明分得越准确"""
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

