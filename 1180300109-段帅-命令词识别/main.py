import sys

import dtw
import mfc_handle

wordlist = ['关闭', '开启', '明亮', '昏暗', '节电模式']
modellist = []
count = 0
right = 0

close = mfc_handle.read_mfc('./mfc/close0.mfc')
modellist.append(close)
open = mfc_handle.read_mfc('./mfc/open0.mfc')
modellist.append(open)
up = mfc_handle.read_mfc('./mfc/up0.mfc')
modellist.append(up)
down = mfc_handle.read_mfc('./mfc/down0.mfc')
modellist.append(down)
save = mfc_handle.read_mfc('./mfc/save0.mfc')
modellist.append(save)


def recognition(name):
    # name = '.mfc/close' + str(i) + '.mfc'
    mfcc = mfc_handle.read_mfc(name)

    min = sys.maxsize
    flag = -1
    for k in range(len(modellist)):
        dtws = dtw.dtw(modellist[k], mfcc)
        if dtws < min:
            min = dtws
            flag = k + 1

    print(name + '识别结果为:' + wordlist[flag - 1] + '\n')
    return flag


for i in range(1, 10):
    name1 = './mfc/close' + str(i) + '.mfc'
    name2 = './mfc/open' + str(i) + '.mfc'
    name3 = './mfc/up' + str(i) + '.mfc'
    name4 = './mfc/down' + str(i) + '.mfc'
    name5 = './mfc/save' + str(i) + '.mfc'
    flag1 = recognition(name1)
    flag2 = recognition(name2)
    flag3 = recognition(name3)
    flag4 = recognition(name4)
    flag5 = recognition(name5)
    if flag1 == 1:
        right += 1
    if flag2 == 2:
        right += 1
    if flag3 == 3:
        right += 1
    if flag4 == 4:
        right += 1
    if flag5 == 5:
        right += 1
    count = count + 5
print('正确率为：' + str(right / count * 100) + '%\n')