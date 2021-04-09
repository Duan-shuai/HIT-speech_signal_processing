import numpy as np

from file_handle import file_handle
from sound_handle import sound_handle

f = file_handle()
s = sound_handle()

for n in range(10):
    filename_read = str(n+1) + '.wav'
    params, wave_data = f.readfile(filename_read)
    framerate = params[2]  # 采样频率

    # 能量
    ener = s.energy(wave_data)
    # 过零率
    zcr = s.zero_cross_ratio(wave_data)

    # 端点检测
    enerlimit = 32500000  # 能量门限
    wav_vad = s.vad(wave_data, ener, enerlimit)
    # wav_vad = s.endPointDetect(wave_data, ener, zcr)
    wave_vad_final = np.array(wav_vad).astype(np.short)

    # 写入文件
    filename_ener = str(n+1) + '_en.txt'
    filename_zcr = str(n+1) + '_zero.txt'
    filename_vad = str(n + 1) + '.pcm'

    f.writefile(filename_ener, ener)
    f.writefile(filename_zcr, zcr)
    f.write_vad(filename_vad, wave_vad_final, framerate)
