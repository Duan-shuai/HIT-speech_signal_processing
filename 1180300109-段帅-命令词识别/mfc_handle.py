import struct
import numpy as np


# 读取mfc文件
def read_mfc(filename):
    fid = open(filename, 'rb')
    nframes, frate, nbytes, feakind = struct.unpack('>IIHH', fid.read(12))
    # nframes = struct.unpack(">i", fid.read(4))
    # frate = struct.unpack(">i", fid.read(4))  # 100 ns 内的
    # nbytes = struct.unpack(">h", fid.read(2))  # 特征的字节数
    # feakind = struct.unpack(">h", fid.read(2))
    ndim = int(nbytes / 4)  # 39维度
    mfcc0 = np.empty((nframes, ndim))
    for i in range(nframes):
        for j in range(ndim):
            mf = fid.read(4)
            c = struct.unpack('>f', mf)
            mfcc0[i][j] = c[0]
    fid.close()
    return mfcc0
