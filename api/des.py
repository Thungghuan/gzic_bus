def str_enc(data, first_key, second_key, third_key):
    # function strEnc from https://sso.scut.edu.cn/cas/common/js/des.js
    leng = len(data)
    first_key_bt = (
        first_length
    ) = second_key_bt = second_length = third_key_bt = third_length = None
    enc_data = None
    if first_key is not None and first_key != "":
        first_key_bt = get_key_bytes(first_key)
        first_length = len(first_key_bt)
    if second_key is not None and second_key != "":
        second_key_bt = get_key_bytes(second_key)
        second_length = len(second_key_bt)
    if third_key is not None and third_key != "":
        third_key_bt = get_key_bytes(third_key)
        third_length = len(third_key)
    if leng > 0:
        if leng < 4:
            bt = str_to_bt(data)
            enc_byte = None
            if (
                first_key is not None
                and first_key != ""
                and second_key is not None
                and second_key != ""
                and third_key is not None
                and third_key != ""
            ):
                temp_bt = bt
                for x in range(first_length):
                    temp_bt = enc(temp_bt, first_key_bt[x])
                for y in range(second_length):
                    temp_bt = enc(temp_bt, second_key_bt[y])
                for z in range(third_length):
                    temp_bt = enc(temp_bt, third_key_bt[z])
                enc_byte = temp_bt
            elif (
                first_key is not None
                and first_key != ""
                and second_key is not None
                and second_key != ""
            ):
                temp_bt = bt
                for x in range(first_length):
                    temp_bt = enc(temp_bt, first_key_bt[x])
                for y in range(second_length):
                    temp_bt = enc(temp_bt, second_key_bt[y])
                enc_byte = temp_bt
            elif first_key is not None and first_key != "":
                temp_bt = bt
                for x in range(first_length):
                    temp_bt = enc(temp_bt, first_key_bt[x])
                enc_byte = temp_bt
            enc_data = bt64_to_hex(enc_byte)
        else:
            iterator = int(leng / 4)
            remainder = leng % 4
            enc_data = ""
            for i in range(iterator):
                temp_data = data[i * 4 : i * 4 + 4]
                temp_byte = str_to_bt(temp_data)
                enc_byte = None
                if (
                    first_key is not None
                    and first_key != ""
                    and second_key is not None
                    and second_key != ""
                    and third_key is not None
                    and third_key != ""
                ):
                    temp_bt = temp_byte
                    for x in range(first_length):
                        temp_bt = enc(temp_bt, first_key_bt[x])
                    for y in range(second_length):
                        temp_bt = enc(temp_bt, second_key_bt[y])
                    for z in range(third_length):
                        temp_bt = enc(temp_bt, third_key_bt[z])
                    enc_byte = temp_bt
                elif (
                    first_key is not None
                    and first_key != ""
                    and second_key is not None
                    and second_key != ""
                ):
                    temp_bt = temp_byte
                    for x in range(first_length):
                        temp_bt = enc(temp_bt, first_key_bt[x])
                    for y in range(second_length):
                        temp_bt = enc(temp_bt, second_key_bt[y])
                    enc_byte = temp_bt
                elif first_key is not None and first_key != "":
                    temp_bt = temp_byte
                    for x in range(first_length):
                        temp_bt = enc(temp_bt, first_key_bt[x])
                    enc_byte = temp_bt
                enc_data += bt64_to_hex(enc_byte)
            if remainder > 0:
                remainder_data = data[iterator * 4 : leng]
                temp_byte = str_to_bt(remainder_data)
                enc_byte = None
                if (
                    first_key is not None
                    and first_key != ""
                    and second_key is not None
                    and second_key != ""
                    and third_key is not None
                    and third_key != ""
                ):
                    temp_bt = temp_byte
                    for x in range(first_length):
                        temp_bt = enc(temp_bt, first_key_bt[x])
                    for y in range(second_length):
                        temp_bt = enc(temp_bt, second_key_bt[y])
                    for z in range(third_length):
                        temp_bt = enc(temp_bt, third_key_bt[z])
                    enc_byte = temp_bt
                elif (
                    first_key is not None
                    and first_key != ""
                    and second_key is not None
                    and second_key != ""
                ):
                    temp_bt = temp_byte
                    for x in range(first_length):
                        temp_bt = enc(temp_bt, first_key_bt[x])
                    for y in range(second_length):
                        temp_bt = enc(temp_bt, second_key_bt[y])
                    enc_byte = temp_bt
                elif first_key is not None and first_key != "":
                    temp_bt = temp_byte
                    for x in range(first_length):
                        temp_bt = enc(temp_bt, first_key_bt[x])
                    enc_byte = temp_bt
                enc_data += bt64_to_hex(enc_byte)
    return enc_data


def get_key_bytes(key):
    leng = len(key)
    iterator = int(leng / 4)
    remainder = leng % 4
    key_bytes = []
    i = 0
    for i in range(iterator):
        key_bytes.append(str_to_bt(key[i * 4 : i * 4 + 4]))
    if remainder > 0:
        key_bytes.append(str_to_bt(key[i * 4 : leng]))
    return key_bytes


def enc(data_byte, key_byte):
    keys = generate_keys(key_byte)
    ip_byte = init_permute(data_byte)
    ip_left = [0] * 32
    ip_right = [0] * 32
    temp_left = [0] * 32
    for k in range(32):
        ip_left[k] = ip_byte[k]
        ip_right[k] = ip_byte[32 + k]
    for i in range(16):
        for j in range(32):
            temp_left[j] = ip_left[j]
            ip_left[j] = ip_right[j]
        key = keys[i]
        temp_right = xor(
            p_permute(s_box_permute(xor(expand_permute(ip_right), key))), temp_left
        )
        for n in range(32):
            ip_right[n] = temp_right[n]
    final_data = [0] * 64
    for i in range(32):
        final_data[i] = ip_right[i]
        final_data[32 + i] = ip_left[i]
    return finally_permute(final_data)


def generate_keys(key_byte):
    loop = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    key = [0] * 56
    keys = [list() for _ in range(16)]
    for i in range(7):
        for j, k in zip(range(8), range(7, -1, -1)):
            key[i * 8 + j] = key_byte[8 * k + i]
    for i in range(16):
        for j in range(loop[i]):
            temp_left = key[0]
            temp_right = key[28]
            for k in range(27):
                key[k] = key[k + 1]
                key[28 + k] = key[29 + k]
            key[27] = temp_left
            key[55] = temp_right
        access_ord = [
            13,
            16,
            10,
            23,
            0,
            4,
            2,
            27,
            14,
            5,
            20,
            9,
            22,
            18,
            11,
            3,
            25,
            7,
            15,
            6,
            26,
            19,
            12,
            1,
            40,
            51,
            30,
            36,
            46,
            54,
            29,
            39,
            50,
            44,
            32,
            47,
            43,
            48,
            38,
            55,
            33,
            52,
            45,
            41,
            49,
            35,
            28,
            31,
        ]
        temp_key = [0] * 48
        for t_ in range(len(access_ord)):
            temp_key[t_] = key[access_ord[t_]]
        for m in range(48):
            keys[i].append(temp_key[m])
    return keys


def init_permute(original_data):
    ip_byte = [0] * 64
    for i, m, n in zip(range(4), range(1, 9, 2), range(0, 8, 2)):
        for j, k in zip(range(7, -1, -1), range(8)):
            ip_byte[i * 8 + k] = original_data[j * 8 + m]
            ip_byte[i * 8 + k + 32] = original_data[j * 8 + n]
    return ip_byte


def expand_permute(right_data):
    ep_byte = [0] * 48
    for i in range(8):
        if i == 0:
            ep_byte[i * 6 + 0] = right_data[31]
        else:
            ep_byte[i * 6 + 0] = right_data[i * 4 - 1]
        ep_byte[i * 6 + 1] = right_data[i * 4 + 0]
        ep_byte[i * 6 + 2] = right_data[i * 4 + 1]
        ep_byte[i * 6 + 3] = right_data[i * 4 + 2]
        ep_byte[i * 6 + 4] = right_data[i * 4 + 3]
        if i == 7:
            ep_byte[i * 6 + 5] = right_data[0]
        else:
            ep_byte[i * 6 + 5] = right_data[i * 4 + 4]
    return ep_byte


def xor(a, b):
    assert len(a) == len(b)
    return [a[i] ^ b[i] for i in range(len(a))]


def s_box_permute(expand_byte):
    s_box_byte = [0] * 32
    s = [
        # s1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],
        # s2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],
        # s3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],
        # s4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],
        # s5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],
        # s6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],
        # s7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],
        # s8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ],
    ]
    for m in range(8):
        i = expand_byte[m * 6 + 0] * 2 + expand_byte[m * 6 + 5]
        j = (
            expand_byte[m * 6 + 1] * 8
            + expand_byte[m * 6 + 2] * 4
            + expand_byte[m * 6 + 3] * 2
            + expand_byte[m * 6 + 4]
        )
        binary = get_box_binary(s[m][i][j])
        s_box_byte[m * 4 + 0] = int(binary[0])
        s_box_byte[m * 4 + 1] = int(binary[1])
        s_box_byte[m * 4 + 2] = int(binary[2])
        s_box_byte[m * 4 + 3] = int(binary[3])
    return s_box_byte


def get_box_binary(i):
    # no fucking switch (i)
    return format(i, "b").zfill(4)


def p_permute(s_box_byte):
    access_ord = [
        15,
        6,
        19,
        20,
        28,
        11,
        27,
        16,
        0,
        14,
        22,
        25,
        4,
        17,
        30,
        9,
        1,
        7,
        23,
        13,
        31,
        26,
        2,
        8,
        18,
        12,
        29,
        5,
        21,
        10,
        3,
        24,
    ]
    p_box_permute = [0] * 32
    for i in range(32):
        p_box_permute[i] = s_box_byte[access_ord[i]]
    return p_box_permute


# noinspection DuplicatedCode,PyShadowingBuiltins
def str_to_bt(s):
    leng = len(s)
    bt = [0] * 64
    if leng < 4:
        for i in range(leng):
            k = ord(s[i])
            for j in range(16):
                pow = 1
                for m in range(15, j, -1):
                    pow *= 2
                bt[16 * i + j] = int(k / pow) % 2
        for p in range(leng, 4):
            k = 0
            for q in range(16):
                pow = 1
                for m in range(15, q, -1):
                    pow *= 2
                bt[16 * p + q] = int(k / pow) % 2
    else:
        for i in range(4):
            k = ord(s[i])
            for j in range(16):
                pow = 1
                for m in range(15, j, -1):
                    pow *= 2
                bt[16 * i + j] = int(k / pow) % 2
    return bt


def finally_permute(end_byte):
    fp_byte = [0] * 64
    access_ord = [
        39,
        7,
        47,
        15,
        55,
        23,
        63,
        31,
        38,
        6,
        46,
        14,
        54,
        22,
        62,
        30,
        37,
        5,
        45,
        13,
        53,
        21,
        61,
        29,
        36,
        4,
        44,
        12,
        52,
        20,
        60,
        28,
        35,
        3,
        43,
        11,
        51,
        19,
        59,
        27,
        34,
        2,
        42,
        10,
        50,
        18,
        58,
        26,
        33,
        1,
        41,
        9,
        49,
        17,
        57,
        25,
        32,
        0,
        40,
        8,
        48,
        16,
        56,
        24,
    ]
    for i in range(64):
        fp_byte[i] = end_byte[access_ord[i]]
    return fp_byte


def bt64_to_hex(byte_data):
    hex_ = ""
    for i in range(16):
        bt = ""
        for j in range(4):
            bt += str(byte_data[i * 4 + j])
        hex_ += "%X" % int(bt, 2)
    return hex_
