import wave
import struct
import numpy as np


class file_handle:

    def readfile(self, filename):
        f = wave.open(filename, "rb")
        # 只读，返回wave_read
        params = f.getparams()
        # 返回一个tuple:
        # (声道数nchannels,量化位数sampwidth(byte),采样频率framerate,采样点数nframes,...)
        print(params)
        # 二进制字符串类型
        str_data = f.readframes(params[3])
        # readframes返回的是二进制数据（一大堆bytes，且不包含文件头)
        f.close()
        # 二字节数组，每个占两个字节（16bits）
        wave_data_origin = np.fromstring(str_data, dtype=np.short)
        # 根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
        # 由于我们的声音格式是以两个字节表示一个取样值，因此采用short数据类型转换。
        return params, wave_data_origin

    def write_pcm(self, filename, code):
        fw = wave.open(filename, 'wb')
        fw.setnchannels(1)  # 双声道
        fw.setsampwidth(2)  # 16位
        fw.setframerate(16000)  # 取样频率
        fw.writeframes(np.array(code).astype(np.short).tostring())
        fw.close()

    def write_4dpc(self, filename, code):
        fw = open(filename, 'wb')

        # 第一个占2字节
        fw.write(struct.pack('h', code[0]))  # 转换为字节流

        # 其他占半个字节，通过位运算处理
        length = len(code)
        w = np.int8(np.ones(length // 2)) * int('11111111', 2)
        for i in range(1, length - 1, 2):
            tmp = w[i // 2] & np.int8(code[i])
            tmp = tmp << 4
            w[i // 2] = tmp | np.int8(code[i + 1])
        for i in range(len(w)):
            b = struct.pack('B', w[i])
            fw.write(b)

        fw.close()
    def write_8dpc(self, filename, code):
        fw = open(filename, 'wb')

        # 第一位占2字节
        fw.write(struct.pack('h', code[0]))

        # 其他占一个字节
        for i in range(1, len(code)):
            fw.write(struct.pack('B', int(code[i])))

    def read_4dpc(self, filename):
        code = []
        with open(filename, 'rb') as f:

            # 读取第一个采样值
            a = struct.unpack('h', f.read(2))
            code.append(a[0])
            while True:
                ff = f.read(1)  # 按字节读
                if not ff:  # 文件末尾
                    break
                else:
                    a = struct.unpack('B', ff)  # 字节流转换，返回一个元组
                    code.append(a[0])
        finalcode = []
        finalcode.append(code[0])
        for i in range(len(code) - 1):
            finalcode.append(code[i + 1] // 16)  # 前4位
            finalcode.append(code[i + 1] % 16)  # 后4位
        return finalcode

    def read_8dpc(self, filename):
        code = []
        with open(filename, 'rb') as f:
            a = struct.unpack('h', f.read(2))  # 前两个字节为第一个采样点值
            code.append(a[0])
            while True:
                ff = f.read(1)  # 按字节读
                if not ff:  # 文件末尾
                    break
                else:
                    a = struct.unpack('B', ff)  # 字节流转换，返回一个元组
                    code.append(a[0])
        return code
