import sys

import numpy as np
from scipy.spatial.distance import euclidean


def dtw(wave1, wave2):
    # 初始化
    len1 = len(wave1)
    len2 = len(wave2)
    # 记录代价，dp递归
    D = np.empty((len1 + 1, len2 + 1))
    # 记录路径，用于回溯
    P = np.empty((len1 + 1, len2 + 1, 2))
    D[0][0] = 0
    P[0][0] = [0, 0]
    for i in range(1, len1 + 1):
        D[i][0] = sys.maxsize
    for j in range(1, len2 + 1):
        D[0][j] = sys.maxsize

    # 递归方程计算
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            d = euclidean(wavedata1[i - 1], wavedata2[j - 1])  # 欧氏距离
            a1 = 2 * d + D[i - 1][j - 1]    # 权重为2
            a2 = d + D[i - 1][j]    # 权重为1
            a3 = d + D[i][j - 1]    # 权重为1
            minD = min(a1, a2, a3)
            # 路径记录
            if minD == a1:
                P[i][j] = [i - 1, j - 1]
            elif minD == a2:
                P[i][j] = [i - 1, j]
            else:
                P[i][j] = [i, j - 1]
            D[i][j] = minD
    # 回溯路径
    w = 0
    m = P[len1][len2]
    while True:
        pm = P[int(m[0])][int(m[1])]
        if pm[0] + 1 == m[0] and pm[1] + 1 == m[0]:
            w += 2
        else:
            w += 1
        if pm[0] == 0 and pm[1] == 0:
            break
        m = pm
    return D[len1][len2] / w
