import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# 正向化
def forward(supplier):
    supplier.neg_total_rate = 1 - supplier.neg_total_rate
    supplier.neg_abs_rate = 1 - supplier.neg_abs_rate
    supplier.p_value = 1 - supplier.p_value

# 预处理
def preProcessing(supplier):
    mean = supplier.mean()
    supplier /= mean

# 生成虚拟母序列
def genVirtualSeries(supplier):
    return supplier.max(axis=1)

# 计算灰色关联系数
def getGcc(supplier, series, rou=0.5):
    diff = supplier.sub(series, axis=0).abs()
    a = diff.min(axis=0).min()
    b = diff.max(axis=0).max()
    gcc = ((a + rou * b) / (diff + rou * b)).mean(axis = 0)
    return gcc

# 计算指标权重
def getWeight(gcc):
    weight = gcc / gcc.sum()
    return weight

# 计算得分
def getScores(supplier, weight):
    scores = supplier.mul(weight, axis=1).sum(axis=1)
    return scores


if __name__ == '__main__':
    supplier = pd.read_csv('supplier.csv', header=0, index_col=0)
    forward(supplier)
    # preProcessing(supplier)
    series = genVirtualSeries(supplier)
    gcc = getGcc(supplier, series)
    weight = getWeight(gcc)
    print(weight)
    scores = getScores(supplier, weight)

    # 保存分数
    scores.to_csv('scores.txt', index=False, sep='\t')