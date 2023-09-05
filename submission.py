# 5bit
# ASCON: 4, 11, 31, 20, 26, 21, 9, 2, 27, 5, 8, 18, 29, 3, 6, 28, 30, 19, 7, 14, 0, 13, 17, 24, 16, 12, 1, 25, 22, 10, 15, 23

# 4bit
## PRESENT: 12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2
## SKINNY: 12, 6, 9, 0, 1, 10, 2, 11, 3, 8, 5, 13, 4, 14, 7, 15
## GIFT: 1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14
## RECTANGLE: 6, 5, 12, 10, 1, 14, 7, 9, 11, 0, 3, 13, 8, 15, 4, 2
# AES: 0, 6, 2, 4, 9, 3, 13, 5, 1, 14, 12, 7, 8, 10, 11, 15
# Midori Sbox: 0xc, 0xa, 0xd, 0x3, 0xe, 0xb, 0xf, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6
# PRINCE Sbox: 0xB, 0xF, 0x3, 0x2, 0xA, 0xC, 0x9, 0x1, 0x6, 0x7, 0x8, 0x0, 0xE, 0x5, 0xD, 0x4
# PRINCE Sbox inv: 0xB, 0x7, 0x3, 0x2, 0xF, 0xD, 0x8, 0x9, 0xA, 0x6, 0x4, 0x0, 0x5, 0xE, 0xC, 0x1
# GF16_inv: 0, 1, 3, 2, 14, 13, 8, 10, 15, 6, 7, 12, 4, 9, 5, 11
# Lblock Sbox: 0xe, 0x9, 0xf, 0x0 , 0xd, 0x4, 0xa, 0xb, 0x1, 0x2, 0x8, 0x3, 0x7, 0x6, 0xc, 0x5
# Led Sbox: 0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2

# 3bit
# LOWMC: 0, 1, 3, 6, 7, 4, 5, 2
# PYJAMASK-3: 1, 3, 6, 5, 2, 4, 7, 0
# SEA: 0, 5, 6, 7, 4, 3, 1, 2

Cipher = "PRESENT"
bitnum = 4
GateNum = 3
AncNum = 1
DEPTH = 30
S = bitnum + AncNum
aNum = (bitnum + AncNum) * GateNum * 3
Size = pow(2, bitnum)
Sbox = [ 12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2 ]
file_path = Cipher + "_Gate" + str(GateNum) + "_Anc" + str(AncNum) + "_depth" + str(DEPTH) + ".cvc"
A = [[0 for j in range(256)] for i in range(8)]

def decompose(flag):
    for i in range(Size):
        tem = 0
        if flag == 0:
            tem = i
        else:
            tem = Sbox[i]
        for j in range(bitnum - 1, -1, -1):
            A[j][i] = tem % 2
            tem //= 2
def to_bin(value, num):
    bin_chars = ""
    temp = value
    for i in range(num):
        bin_char = bin(temp % 2)[-1]
        temp = temp // 2
        bin_chars = bin_char + bin_chars
    return bin_chars.upper()
def State_Variable(w, len):
    with open(file_path, 'a') as f:
        for i in range(0, len):
            f.write(w + "_" + str(i))
            if i == len - 1:
                f.write(": BITVECTOR(" + str(Size) + ");\n")
            else:
                f.write(" , ")
def State_arr_Variable(w, len):
    with open(file_path, 'a') as f:
        for i in range(0, len):
            f.write(w + "_" + str(i) + ": ARRAY BITVECTOR(6) OF BITVECTOR(" + str(Size) + ");")
            f.write("\n")
def Logic_Constraint():
    countA = 0
    countQ = 0
    countT = 0
    countb = 0
    depth = 0
    with open(file_path, 'a') as f:
        for k in range(0, GateNum):
            #q
            D1 = to_bin(k, 6)
            D2 = to_bin(k + 1, 6)
            d1 = to_bin(depth, 6)
            d2 = to_bin(depth + 1, 6)
            for q in range(0, 3):
                f.write("ASSERT( Q_" + str(countQ) + " = ")
                countQ += 1
                for i in range(0, bitnum - 1):
                    f.write("BVXOR( a_" + str(countA) + " & X_" + str(i) + "[0bin" + str(d1) + "] , ")
                    countA += 1
                if AncNum == 0:
                    f.write("a_" + str(countA) + " & X_" + str(bitnum -1) + "[0bin" + str(d1) + "]")
                    countA += 1
                    for i in range(0, bitnum):
                        f.write(" )")
                    f.write(";")
                else:
                    f.write("BVXOR( a_" + str(countA) + " & X_" + str(bitnum -1) + "[0bin" + str(d1) + "] , ")
                    countA += 1
                    if AncNum == 1:
                        f.write("a_" + str(countA) + " & Anc_" + str(AncNum - 1) + "[0bin" + str(d1) + "]")
                        countA += 1
                    else:
                        for a in range(0, AncNum - 1):
                            f.write("BVXOR( a_" + str(countA) + " & Anc_" + str(a) + "[0bin" + str(d1) + "] , ")
                            countA += 1
                        f.write("a_" + str(countA) + " & Anc_" + str(AncNum - 1) + "[0bin" + str(d1) + "]")
                        countA += 1
                    for j in range(0, S):
                        f.write(" )")
                    f.write(" ;")
                f.write("\n")
            # t
            f.write("ASSERT( T_" + str(countT) + " = BVXOR( Q_" + str(countQ - 3) + " , BVXOR( Q_" + str(
                countQ - 2) + " , BVXOR( b_" + str(countb) + " & Q_" + str(countQ - 2) + " , BVXOR( b_" + str(
                countb) + " & Q_" + str(countQ - 2))
            f.write(" & Q_" + str(countQ - 1) + " , BVXOR( b_" + str(countb + 1) + " & Q_" + str(
                countQ - 2) + " , b_" + str(countb + 1) + " ) ) ) ) ) ); ")
            f.write("\n")
            countT += 1
            countb += 2
            # b
            for b in range(0, bitnum):
                f.write("ASSERT( ( Q_" + str(countQ - 3) + " = X_" + str(b%bitnum) + "[0bin" + str(d1) + "] ) => ( ( X_" + str(b%bitnum) + "[0bin" + str(d2) + "] = T_" + str(countT-1) + " )")
                for i in range(1, bitnum):
                    f.write(" AND ( X_" + str((b+i)%bitnum) + "[0bin" + str(d2) + "] = X_" + str((b+i)%bitnum) + "[0bin" + str(d1) + "] )")

                for a in range(0, AncNum):
                    f.write(" AND ( Anc_" + str(a) + "[0bin" + str(d2) + "] = Anc_" + str(a) + "[0bin" + str(d1) + "] )" )
                f.write(" ) ); ")
                f.write("\n")
            #anc
            for a in range(0, AncNum):
                f.write("ASSERT( ( Q_" + str(countQ - 3) + " = Anc_" + str(a) + "[0bin" + str(d1) + "] ) => ( ( Anc_" + str(a) + "[0bin" + str(d2) + "] = T_" + str(countT-1) + " )")
                for j in range(0, bitnum):
                    f.write(" AND ( X_" + str(j) + "[0bin" + str(d2) + "] = X_" + str(j) + "[0bin" + str(d1) + "] )")
                for i in range(0, AncNum):
                    if i != a:
                        f.write(" AND ( Anc_" + str(i) + "[0bin" + str(d2) + "] = Anc_" + str(i) + "[0bin" + str(d1) + "] )")
                f.write(" ) ); ")
                f.write("\n")
            depth += 1
            #constrain for depth
            for m in range(0, S):
                f.write("ASSERT( ( b_"+ str(countb - 2) + "[0:0]@b_"+ str(countb - 1) + "[0:0]@a_"+ str(m + S * k * 3) + "[0:0] = 0bin011 ) => ( ( depth_" + str(m) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(m) + "[0bin" + str(D1) + "], 0bin")
                for i in range(0, Size - 1):
                    f.write("0")
                f.write("1) )")
                for m1 in range(1, S):
                    f.write(" AND ( depth_" + str((m + m1)%S) + "[0bin" + str(D2) + "] = depth_" + str((m + m1)%S) + "[0bin" + str(D1) + "] )")
                f.write(" ) );\n")
            r1 = k * S
            r2 = k * S + S - 1
            for r in range(r1, r2):
                for t in range(r + 1, r2 + 1):
                    f.write("ASSERT( ( ( b_"+ str(countb - 2) + "[0:0]@b_"+ str(countb - 1) + "[0:0]@c_"+ str(r) + "[0:0]@c_"+ str(t) + "[0:0] = 0bin0011 ) AND ( BVGE(depth_" + str(r % S) + "[0bin" + str(D1) + "], depth_" + str(t % S) + "[0bin" + str(D1) + "] ) ) ) => ( ( depth_" + str(r % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(r % S) + "[0bin" + str(D1) + "], 0bin")
                    for i in range(0, Size - 1):
                        f.write("0")
                    f.write("1) ) AND")
                    f.write("( depth_" + str(t % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(r % S) + "[0bin" + str(D1) + "], 0bin")
                    for i in range(0, Size - 1):
                        f.write("0")
                    f.write("1) )")
                    for m in range(1, S):
                        if ((r + m)%S) != (t % S):
                            f.write(" AND ( depth_" + str((m + r)%S) + "[0bin" + str(D2) + "] = depth_" + str((m + r)%S) + "[0bin" + str(D1) + "] )")
                    f.write(" ) );\n")

                    f.write("ASSERT( ( ( b_"+ str(countb - 2) + "[0:0]@b_"+ str(countb - 1) + "[0:0]@c_"+ str(r) + "[0:0]@c_"+ str(t) + "[0:0] = 0bin0011 ) AND ( BVGT(depth_" + str(t % S) + "[0bin" + str(D1) + "], depth_" + str(r % S) + "[0bin" + str(D1) + "] ) ) ) => ( ( depth_" + str(r % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(t % S) + "[0bin" + str(D1) + "], 0bin")
                    for i in range(0, Size - 1):
                        f.write("0")
                    f.write("1) ) AND")
                    f.write("( depth_" + str(t % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(t % S) + "[0bin" + str(D1) + "], 0bin")
                    for i in range(0, Size - 1):
                        f.write("0")
                    f.write("1) )")
                    for m in range(1, S):
                        if ((r + m)%S) != (t % S):
                            f.write(" AND ( depth_" + str((m + r)%S) + "[0bin" + str(D2) + "] = depth_" + str((m + r)%S) + "[0bin" + str(D1) + "] )")
                    f.write(" ) );\n")
            for h1 in range(r1, r1 + S - 2):
                for h2 in range(h1 + 1, r1 + S - 1):
                    for h3 in range(h2 + 1, r1 + S):
                        f.write("ASSERT( ( ( b_" + str(countb - 2) + "[0:0]@b_" + str(countb - 1) + "[0:0]@d_" + str(h1) + "[0:0]@d_" + str(h2) + "[0:0]@d_" + str(h3) + "[0:0] = 0bin10111 ) AND ( BVGE(depth_" + str(h1 % S) + "[0bin" + str(D1) + "], depth_" + str(h2 % S) + "[0bin" + str(D1) + "] ) ) AND ( BVGE(depth_" + str(h1 % S)
                                + "[0bin" + str(D1) + "], depth_" + str(h3 % S) + "[0bin" + str(D1) + "] ) ) ) => ( ( depth_" + str(h1 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h1 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) ) AND")
                        f.write("( depth_" + str(h2 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h1 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) ) AND ( depth_" + str(h3 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h1 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) )")
                        for m in range(1, S):
                            if ((h1 + m) % S) != (h2 % S):
                                if ((h1 + m) % S) != (h3 % S):
                                    f.write(" AND ( depth_" + str((m + h1) % S) + "[0bin" + str(D2) + "] = depth_" + str((m + h1) % S) + "[0bin" + str(D1) + "] )")
                        f.write(" ) );\n")
                        f.write("ASSERT( ( ( b_" + str(countb - 2) + "[0:0]@b_" + str(countb - 1) + "[0:0]@d_" + str(h1) + "[0:0]@d_" + str(h2) + "[0:0]@d_" + str(h3) + "[0:0] = 0bin10111 ) AND ( BVGE(depth_" + str(h2 % S) + "[0bin" + str(D1) + "], depth_" + str(h1 % S) + "[0bin" + str(D1) + "] ) ) AND ( BVGE(depth_" + str(h2 % S)
                                + "[0bin" + str(D1) + "], depth_" + str(h3 % S) + "[0bin" + str(D1) + "] ) ) ) => ( ( depth_" + str(h1 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h2 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) ) AND")
                        f.write("( depth_" + str(h2 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h2 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) ) AND ( depth_" + str(h3 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h2 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) )")
                        for m in range(1, S):
                            if ((h1 + m) % S) != (h2 % S):
                                if ((h1 + m) % S) != (h3 % S):
                                    f.write(" AND ( depth_" + str((m + h1) % S) + "[0bin" + str(D2) + "] = depth_" + str((m + h1) % S) + "[0bin" + str(D1) + "] )")
                        f.write(" ) );\n")
                        f.write("ASSERT( ( ( b_" + str(countb - 2) + "[0:0]@b_" + str(countb - 1) + "[0:0]@d_" + str(h1) + "[0:0]@d_" + str(h2) + "[0:0]@d_" + str(h3) + "[0:0] = 0bin10111 ) AND ( BVGE(depth_" + str(h3 % S) + "[0bin" + str(D1) + "], depth_" + str(h2 % S) + "[0bin" + str(D1) + "] ) ) AND ( BVGE(depth_" + str(h3 % S)
                                + "[0bin" + str(D1) + "], depth_" + str(h1 % S) + "[0bin" + str(D1) + "] ) ) ) => ( ( depth_" + str(h1 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h3 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) ) AND")
                        f.write("( depth_" + str(h2 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h3 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) ) AND ( depth_" + str(h3 % S) + "[0bin" + str(D2) + "] = BVPLUS(" + str(Size) + ", depth_" + str(h3 % S) + "[0bin" + str(D1) + "], 0bin")
                        for i in range(0, Size - 3):
                            f.write("0")
                        f.write("111) )")
                        for m in range(1, S):
                            if ((h1 + m) % S) != (h2 % S):
                                if ((h1 + m) % S) != (h3 % S):
                                    f.write(" AND ( depth_" + str((m + h1) % S) + "[0bin" + str(D2) + "] = depth_" + str((m + h1) % S) + "[0bin" + str(D1) + "] )")
                        f.write(" ) );\n")
        #y
        d = to_bin(depth, 6)
        for i in range(0, bitnum):
            f.write("ASSERT( ( Y_" + str(i) + " = X_0[0bin" + str(d) + "] )")
            for j in range(1, bitnum):
                f.write(" OR ( Y_" + str(i) + " = X_" + str(j) + "[0bin" + str(d) + "] )")
            if AncNum == 0:
                f.write(" );\n")
            if AncNum != 0:
                for j in range(0, AncNum):
                    f.write(" OR ( Y_" + str(i) + " = Anc_" + str(j) + "[0bin" + str(d) + "] )")
                f.write(" );\n")
        #depth
        D = to_bin(GateNum, 6)
        DEPTH_1 = to_bin(DEPTH, Size)
        for h in range(0, S):
            f.write("ASSERT( BVLT(depth_" + str(h) + "[0bin" + str(D) + "], 0bin" + str(DEPTH_1))
            f.write(") );\n")
if __name__ == "__main__":
    #state
    State_arr_Variable("X", bitnum)
    State_arr_Variable("Anc", AncNum)
    State_arr_Variable("depth", S)
    State_Variable("Y", bitnum)
    State_Variable("T", GateNum)
    State_Variable("Q", 3 * GateNum)
    State_Variable("a", aNum)
    State_Variable("b", GateNum * 2)
    State_Variable("c", GateNum * S)
    State_Variable("d", GateNum * S)
    #x
    decompose(0)
    with open(file_path, 'a') as f:
        for i in range(0, bitnum):
            f.write("ASSERT( X_" + str(i) + "[0bin000000] " + " = 0bin")
            for j in range(0, Size):
                f.write(str(A[i][j]))
            f.write(" );\n")
    #y
    decompose(1)
    with open(file_path, 'a') as f:
        for i in range(0, bitnum):
            f.write("ASSERT( Y_" + str(i) + " = 0bin")
            for j in range(0, Size):
                f.write(str(A[i][j]))
            f.write(" );\n")
    #anc
    with open(file_path, 'a') as f:
        for a in range(0, AncNum):
            f.write("ASSERT( Anc_" + str(a) + "[0bin000000] " + " = 0bin")
            for i in range(0, Size):
                f.write("0")
            f.write(" );\n")
    #depth
    with open(file_path, 'a') as f:
        for i in range(0, S):
            f.write("ASSERT( depth_" + str(i) + "[0bin000000] " + " = 0bin")
            for j in range(0, Size):
                f.write("0")
            f.write(" );\n")
    #a
    with open(file_path, 'a') as f:
        for i in range(0, aNum):
            f.write("ASSERT( a_" + str(i) + " = 0bin")
            for j in range(0, Size):
                f.write("1")
            f.write(" OR a_" + str(i) + " = 0bin")
            for j in range(0, Size):
                f.write("0")
            f.write(" ); \n")
    j = 0
    n = 0
    with open(file_path, 'a') as f:
        while n + S < aNum:
            n = S * j
            f.write("ASSERT( ( ( a_" + str(n) + " = 0bin")
            for i in range(0, Size):
                f.write("1")
            f.write(" ) ")
            for k in range(1, S):
                f.write("AND ( a_" + str(k + n) + " = 0bin")
                for i in range(0, Size):
                    f.write("0")
                f.write(" ) ")
            for m in range(0, S - 1):
                f.write(") OR ")
                f.write("( ( a_" + str(n) + " = 0bin")
                for i in range(0, Size):
                    f.write("0")
                f.write(" ) ")
                for k in range(1, S):
                    f.write(" AND ( a_" + str(k + n) + " = 0bin")
                    if  k == m + 1:
                        for i in range(0, Size):
                            f.write("1")
                    else:
                        for i in range(0, Size):
                            f.write("0")
                    f.write(" ) ")
            f.write(") );\n")
            j += 1
    with open(file_path, 'a') as f:
        for g in range(0, GateNum):
            m = 3 * g * S
            for i in range(0, S):
                f.write("ASSERT( a_" + str(m + i) + " & a_" + str(m + i + S) + " = 0bin")
                for j in range(0, Size):
                    f.write("0")
                f.write(" );\n")
                f.write("ASSERT( a_" + str(m + i) + " & a_" + str(m + i + S * 2) + " = 0bin")
                for j in range(0, Size):
                    f.write("0")
                f.write(" );\n")
                f.write("ASSERT( a_" + str(m + i + S) + " & a_" + str(m + i + S * 2) + " = 0bin")
                for j in range(0, Size):
                    f.write("0")
                f.write(" );\n")
    #b
    with open(file_path, 'a') as f:
        for i in range(0, GateNum * 2):
            f.write("ASSERT( b_" + str(i) + " = 0bin")
            for j in range(0, Size):
                f.write("1")
            f.write(" OR b_" + str(i) + " = 0bin")
            for j in range(0, Size):
                f.write("0")
            f.write(" ); \n")
        n1 = 0
    with open(file_path, 'a') as f:
        while n1 < GateNum * 2:
            f.write("ASSERT( b_" + str(n1) + " & b_" + str(n1+1) + " = 0bin")
            for j in range(0, Size):
                f.write("0")
            f.write(" );\n")
            n1 = n1 + 2
    #c
    with open(file_path, 'a') as f:
        for g in range(0, GateNum):
            for k in range(0, S):
                f.write("ASSERT( c_" + str(g * S + k) +  " = BVXOR( a_" + str(g * S * 3 + k) + ", a_" + str(g * S * 3 + k + S))
                f.write(" ) );\n")
    #d
    with open(file_path, 'a') as f:
        for g in range(0, GateNum):
            for k in range(0, S):
                f.write("ASSERT( d_" + str(g * S + k) +  " = BVXOR( c_" + str(g * S + k) + ", a_" + str(g * S * 3 + k + S * 2))
                f.write(" ) );\n")

    Logic_Constraint()
    with open(file_path, 'a') as f:
        f.write("QUERY(FALSE);\nCOUNTEREXAMPLE;\n")
