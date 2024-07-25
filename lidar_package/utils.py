import math
from math import atan, pi, floor

def _CheckSum(data):
    try:
        ocs = _HexArrToDec((data[6], data[7]))
        LSN = data[1]
        cs = 0x55AA ^ _HexArrToDec((data[0], data[1])) ^ _HexArrToDec((data[2], data[3])) ^ _HexArrToDec((data[4], data[5]))
        for i in range(0, 2 * LSN, 2):
            cs = cs ^ _HexArrToDec((data[8 + i], data[8 + i + 1]))
        return cs == ocs
    except Exception as e:
        return False

def _HexArrToDec(data):
    littleEndianVal = 0
    for i in range(0, len(data)):
        littleEndianVal = littleEndianVal + (data[i] * (256 ** i))
    return littleEndianVal

def _AngleCorr(dist):
    if dist == 0:
        return 0
    else:
        return (atan(21.8 * ((155.3 - dist) / (155.3 * dist))) * (180 / pi))

def _Calculate(d):
    ddict = []
    LSN = d[1]
    Angle_fsa = ((_HexArrToDec((d[2], d[3])) >> 1) / 64.0)
    Angle_lsa = ((_HexArrToDec((d[4], d[5])) >> 1) / 64.0)
    Angle_diff = Angle_lsa - Angle_fsa if Angle_fsa < Angle_lsa else 360 + Angle_lsa - Angle_fsa
    for i in range(0, 2 * LSN, 2):
        dist_i = _HexArrToDec((d[8 + i], d[8 + i + 1])) / 4
        Angle_i_tmp = ((Angle_diff / float(LSN)) * (i / 2)) + Angle_fsa
        Angle_i = Angle_i_tmp if Angle_i_tmp < 360 else Angle_i_tmp - 360
        Angle_i += _AngleCorr(dist_i)
        ddict.append((dist_i, Angle_i))
    return ddict

def _Mean(data):
    length_of_data_without_zero = sum([i != 0 for i in data])
    return float(sum(data) / length_of_data_without_zero) if (len(data) > 0 and length_of_data_without_zero != 0) else 0