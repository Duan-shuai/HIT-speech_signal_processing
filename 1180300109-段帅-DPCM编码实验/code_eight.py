import math
import numpy as np


class code_eight:

    def quantification_a(self, d, a):
        if d > 127 * a:
            final_code = 127
        elif d < -128 * a:
            final_code = -128
        else:
            for j in range(-128, 128):
                if (j - 1) * a < d <= j * a:
                    final_code = j
                    break
        final_code = final_code + 128
        # 量化因子法相当于整体平移，由（-128，127）->(0，255)
        return final_code

    def quantification_log(self, d):
        c = math.log(abs(d) + 1)
        if c > 127:
            c = 127
        if d < 0:
            final_code = c + 128  # +10000000
        else:
            final_code = c
        # 对数变换法相当于增加符号位，（1xxx为负数，0xxx为正数）
        return final_code

    def code(self, data, a, flag):
        length = len(data)
        code = list(range(length))
        decode = list(range(length))
        code[0] = data[0]
        decode[0] = data[0]
        for i in range(length - 1):
            code[i + 1] = data[i + 1] - decode[i]   # 编码
            # 量化因子法
            if flag == 0:
                code[i + 1] = self.quantification_a(code[i + 1], a)  # 量化
                decode[i + 1] = decode[i] + (code[i + 1] - 128) * a  # 解码，用于反馈
            # 对数变换法
            else:
                code[i + 1] = self.quantification_log(code[i + 1])
                if code[i+1] >= 8:   # 负数
                    decode[i + 1] = decode[i] - math.exp(code[i + 1] - 128) + 1  # 解码，用于反馈
                else:
                    decode[i + 1] = decode[i] + math.exp(code[i + 1]) - 1  # 解码，用于反馈
        return code

    def decode(self, code, a, flag):
        length = len(code)
        decode = list(range(length))
        decode[0] = np.longlong(code[0])
        # 量化因子法
        if flag == 0:
            for i in range(length - 1):
                decode[i + 1] = np.longlong(decode[i]) + (code[i + 1] - 128) * a
        else:
            for i in range(length - 1):
                if code[i + 1] >= 8:  # 负数
                    decode[i + 1] = decode[i] - math.exp(code[i + 1] - 128) + 1  # 解码，用于反馈
                else:
                    decode[i + 1] = decode[i] + math.exp(code[i + 1]) - 1  # 解码，用于反馈
        return decode

    def snr(self, data1, data2):
        length = len(data1)
        sum1 = np.longlong(0)
        sum2 = np.longlong(0)
        for i in range(length - 1):
            n1 = np.longlong(data1[i]) ** 2 / length  # np.longlong防止计算时溢出
            sum1 = sum1 + n1
            n2 = np.longlong(data1[i] - data2[i]) ** 2 / length
            sum2 = sum2 + n2
        return 10 * np.log10(sum1 / sum2)
