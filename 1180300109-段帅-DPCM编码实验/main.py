from code_eight import code_eight
from code_four import code_four
from file_handle import file_handle

filename_read = '1.wav'
filename_8dpc0 = './量化因子法/1_8bit.dpc'
filename_8pcm0 = './量化因子法/1_8bit.pcm'
filename_4dpc0 = './量化因子法/1_4bit.dpc'
filename_4pcm0 = './量化因子法/1_4bit.pcm'
filename_8dpc1 = './对数变换法/1_8bit.dpc'
filename_8pcm1 = './对数变换法/1_8bit.pcm'
filename_4dpc1 = './对数变换法/1_4bit.dpc'
filename_4pcm1 = './对数变换法/1_4bit.pcm'
a1 = 900
a2 = 100
a11 = 10
a21 = 50

f = file_handle()
params, wave_data = f.readfile(filename_read)
c4 = code_four()
c8 = code_eight()

# flag == 0：量化因子法--4bit
# 编码
code4data0 = c4.code(wave_data, a1, flag=0)
# 存压缩文件
f.write_4dpc(filename_4dpc0, code4data0)
# 读压缩文件
read4data0 = f.read_4dpc(filename_4dpc0)
# 解码
decode4data0 = c4.decode(read4data0, a1, flag=0)
# 存pcm文件
f.write_pcm(filename_4pcm0, decode4data0)
# snr
print(c4.snr(decode4data0, wave_data))

# flag == 1：对数变换法--4bit
# 编码
code4data1 = c4.code(wave_data, a11, flag=1)
# 存压缩文件
f.write_4dpc(filename_4dpc1, code4data1)
# 读压缩文件
read4data1 = f.read_4dpc(filename_4dpc1)
# 解码
decode4data1 = c4.decode(read4data1, a11, flag=1)
# 存pcm文件
f.write_pcm(filename_4pcm1, decode4data1)
# snr
print(c4.snr(decode4data1, wave_data))

# flag == 0:量化因子法--8bit
code8data0 = c8.code(wave_data, a2, flag=0)
# 存压缩文件
f.write_8dpc(filename_8dpc0, code8data0)
# 读压缩文件
read8data0 = f.read_8dpc(filename_8dpc0)
# 解码
decode8data0 = c8.decode(read8data0, a2, flag=0)
# 存pcm文件
f.write_pcm(filename_8pcm0, decode8data0)
# snr
print(c8.snr(decode8data0, wave_data))

# flag == 1:对数变换法
code8data1 = c8.code(wave_data, a2, flag=1)
# 存压缩文件
f.write_8dpc(filename_8dpc1, code8data1)
# 读压缩文件
read8data1 = f.read_8dpc(filename_8dpc1)
# 解码
decode8data1 = c8.decode(read8data1, a2, flag=1)
# 存pcm文件
f.write_pcm(filename_8pcm1, decode8data1)
# snr
print(c8.snr(decode8data1, wave_data))