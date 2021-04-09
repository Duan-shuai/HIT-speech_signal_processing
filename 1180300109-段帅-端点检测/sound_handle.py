import math

import numpy as np


class sound_handle:
    def energy(self, waveData):
        wlen = len(waveData)
        # 每帧采样点数
        step = 256
        # 函数返回数字的上入整数,帧数
        frameNum = math.ceil(wlen / step)
        # 各个窗口的短时能量
        ener = []
        for i in range(frameNum):
            curFrame = waveData[np.arange(i * step, min(i * step + step, wlen))]
            sum = np.longlong(0)
            for j in range(len(curFrame)):
                n = np.longlong(curFrame[j]) ** 2
                sum = sum + n
            ener.append(sum)
        return ener

    def sign(self, list):
        for i in range(len(list)):
            if list[i] >= 0:
                list[i] = 1
            else:
                list[i] = -1
        return list

    def zero_cross_ratio(self, waveData):
        wlen = len(waveData)
        step = 256
        frameNum = math.ceil(wlen / step)
        # 各个窗口的过零率
        zcr = []
        for i in range(frameNum):
            curFrame = waveData[np.arange(i * step, min(i * step + step, wlen))]
            zcr.append(sum(abs(self.sign(curFrame[0:-1]) - self.sign(curFrame[1::]))) / (2 * 256))
        return zcr

    def vad(self, wave_data_origin, ener, enerlimit):
        wave_vad = []
        for i in range(len(ener) - 1):
            if ener[i] > enerlimit:
                for j in range(256):
                    wave_vad.append(wave_data_origin[i * 256 + j])
        return wave_vad

    def endPointDetect(self, wave_data, energy, zeroCrossingRate):
        # 设置能量与过零率门限
        sum = 0
        energyAverage = 0
        for en in energy:
            sum = sum + en
        energyAverage = sum / len(energy)

        sum = 0
        for en in energy[:5]:
            sum = sum + en
        ML = sum / 5
        MH = energyAverage / 4  # 较高的能量阈值
        ML = (ML + MH) / 4  # 较低的能量阈值

        sum = 0
        for zcr in zeroCrossingRate[:5]:
            sum = float(sum) + zcr
        Zs = sum / 5  # 过零率阈值

        A = []
        B = []
        C = []

        # 首先利用较大能量阈值 MH 进行初步检测
        flag = 0
        for i in range(len(energy)):
            if len(A) == 0 and flag == 0 and energy[i] > MH:
                A.append(i)
                flag = 1
            elif flag == 0 and energy[i] > MH and i - 21 > A[len(A) - 1]:
                A.append(i)
                flag = 1
            elif flag == 0 and energy[i] > MH and i - 21 <= A[len(A) - 1]:
                A = A[:len(A) - 1]
                flag = 1

            if flag == 1 and energy[i] < MH:
                A.append(i)
                flag = 0
        print("较高能量阈值，计算后的浊音A:" + str(A))

        # 利用较小能量阈值 ML 进行第二步能量检测
        for j in range(len(A)):
            i = A[j]
            if j % 2 == 1:
                while i < len(energy) and energy[i] > ML:
                    i = i + 1
                B.append(i)
            else:
                while i > 0 and energy[i] > ML:
                    i = i - 1
                B.append(i)
        print("较低能量阈值，增加一段语言B:" + str(B))

        # 利用过零率进行最后一步检测
        for j in range(len(B)):
            i = B[j]
            if j % 2 == 1:
                while i < len(zeroCrossingRate) and zeroCrossingRate[i] >= 3 * Zs:
                    i = i + 1
                C.append(i)
            else:
                while i > 0 and zeroCrossingRate[i] >= 3 * Zs:
                    i = i - 1
                C.append(i)
        print("过零率阈值，最终语音分段C:" + str(C))
        return C