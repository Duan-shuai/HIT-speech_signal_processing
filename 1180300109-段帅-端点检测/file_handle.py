import wave

import numpy as np


class file_handle:
    def readfile(self, filename):
        f = wave.open(filename, "rb")
        # 只读，返回wave_read
        params = f.getparams()
        # 返回一个tuple:
        # (声道数nchannels,量化位数sampwidth(byte),采样频率framerate,采样点数nframes,...)
        print(params)
        str_data = f.readframes(params[3])
        # readframes返回的是二进制数据（一大堆bytes，且不包含文件头)
        f.close()
        wave_data_origin = np.fromstring(str_data, dtype=np.short)
        # 根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
        # 由于我们的声音格式是以两个字节表示一个取样值，因此采用short数据类型转换。
        return params, wave_data_origin

    def writefile(self, filename, data):
        fw = open(filename, 'w')
        for i in range(len(data)):
            m = str(data[i]) + "\n"
            fw.writelines(m)
        fw.close()

    def write_vad(self, filename, wave_vad_final, framerate):
        fw = wave.open(filename, 'wb')
        fw.setnchannels(1)  # 双声道
        fw.setsampwidth(2)  # 16位
        fw.setframerate(framerate)  # 取样频率
        fw.writeframes(wave_vad_final.tostring())  # 转换为二进制数据写入文件
        fw.close()