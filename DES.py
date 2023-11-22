def binary_to_hex(binary_string):
  try:
    decimal_number = int(binary_string, 2)
    hex_string = hex(decimal_number)[2:]
    return hex_string.upper() 
  except ValueError:
    return "Invalid binary input"

def hex_to_binary(hex_string):
  try:
    hex_string = hex_string.lstrip('0x')
    decimal_number = int(hex_string, 16)
    binary_string = bin(decimal_number)[2:]
    return binary_string
  except ValueError:
    return "Invalid hexadecimal input"

def binary_to_decimal(binary):
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

def decimal_to_binary(num):
	res = bin(num).replace("0b", "")
	if(len(res) % 4 != 0):
		div = len(res) / 4
		div = int(div)
		counter = (4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res
  
def xor(a, b):
	ans = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			ans = ans + "0"
		else:
			ans = ans + "1"
	return ans

def shift_left(k, nth_shifts):
	return k[nth_shifts:] + k[:nth_shifts]
  
def permute(k, arr, n):
  permutation = ""
  for i in range(0, n):
    permutation = permutation + k[arr[i] - 1]
  return permutation

# Table of Position of 64 bits at initial level: Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
  60, 52, 44, 36, 28, 20, 12, 4,
  62, 54, 46, 38, 30, 22, 14, 6,
  64, 56, 48, 40, 32, 24, 16, 8,
  57, 49, 41, 33, 25, 17, 9, 1,
  59, 51, 43, 35, 27, 19, 11, 3,
  61, 53, 45, 37, 29, 21, 13, 5,
  63, 55, 47, 39, 31, 23, 15, 7]

# Straight Permutation Table
per = [16, 7, 20, 21,
	29, 12, 28, 17,
	1, 15, 23, 26,
	5, 18, 31, 10,
	2, 8, 24, 14,
	32, 27, 3, 9,
	19, 13, 30, 6,
	22, 11, 4, 25]

# Final Permutation Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
	39, 7, 47, 15, 55, 23, 63, 31,
	38, 6, 46, 14, 54, 22, 62, 30,
	37, 5, 45, 13, 53, 21, 61, 29,
	36, 4, 44, 12, 52, 20, 60, 28,
	35, 3, 43, 11, 51, 19, 59, 27,
	34, 2, 42, 10, 50, 18, 58, 26,
	33, 1, 41, 9, 49, 17, 57, 25]

# Expansion D-box Table
exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
  6, 7, 8, 9, 8, 9, 10, 11,
  12, 13, 12, 13, 14, 15, 16, 17,
  16, 17, 18, 19, 20, 21, 20, 21,
  22, 23, 24, 25, 24, 25, 26, 27,
  28, 29, 28, 29, 30, 31, 32, 1]

# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
  [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
  [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
  [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

  [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
  [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
  [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
  [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

  [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
  [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
  [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
  [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

  [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
  [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
  [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
  [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

  [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
  [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
  [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
  [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

  [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
  [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
  [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
  [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

  [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
  [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
  [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
  [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

  [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
  [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
  [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
  [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


# KEY ======================================
key = "AABB09112726CCDD"
key = hex_to_binary(key)

keyp = [57, 49, 41, 33, 25, 17, 9,
  1, 58, 50, 42, 34, 26, 18,
  10, 2, 59, 51, 43, 35, 27,
  19, 11, 3, 60, 52, 44, 36,
  63, 55, 47, 39, 31, 23, 15,
  7, 62, 54, 46, 38, 30, 22,
  14, 6, 61, 53, 45, 37, 29,
  21, 13, 5, 28, 20, 12, 4]

# getting 56 bit key from 64 bit using the parity bits
key = permute(key, keyp, 56)

# Number of bit shifts
shift_table = [1, 1, 2, 2,
  2, 2, 2, 2,
  1, 2, 2, 2,
  2, 2, 2, 1]

# Key- Compression Table : Compression of key from 56 bits to 48 bits
key_comp = [14, 17, 11, 24, 1, 5,
  3, 28, 15, 6, 21, 10,
  23, 19, 12, 4, 26, 8,
  16, 7, 27, 20, 13, 2,
  41, 52, 31, 37, 47, 55,
  30, 40, 51, 45, 33, 48,
  44, 49, 39, 56, 34, 53,
  46, 42, 50, 36, 29, 32]

# Splitting
left = key[0:28] # rkb for RoundKeys in binary
right = key[28:56] # rk for RoundKeys in hexadecimal

rkb = []
rk = []

for i in range(0, 16):
	# Shifting the bits by nth shifts by checking from shift table
	left = shift_left(left, shift_table[i])
	right = shift_left(right, shift_table[i])

	# Combination of left and right string
	combine_str = left + right

	# Compression of key from 56 to 48 bits
	round_key = permute(combine_str, key_comp, 48)

	rkb.append(round_key)
	rk.append(binary_to_hex(round_key))
    
rkb_reversed = rkb[::-1]
rk_reversed = rk[::-1]
     
def encrypt(plain_text):
  plain_text = hex_to_binary(plain_text)

  # Initial Permutation
  plain_text = permute(plain_text, initial_perm, 64)

  # Splitting
  left = plain_text[0:32]
  right = plain_text[32:64]
  for i in range(0, 16):
    # Expansion D-box: from 32 bits to 48 bits
    right_expanded = permute(right, exp_d, 48)

    # XOR RoundKey[i] and right_expanded
    xor_x = xor(right_expanded, rkb[i])

    # S-box: subtituting the value from s-box table by calculating row and column
    sbox_str = ""
    for j in range(0, 8):
      row = binary_to_decimal(int(xor_x[j*6] + xor_x[j*6+5]))
      col = binary_to_decimal(int(xor_x[j*6+1] + xor_x[j*6+2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
      val = sbox[j][row][col]
      sbox_str = sbox_str + decimal_to_binary(val)

    # Straight D-box: After substituting rearranging the bits
    sbox_str = permute(sbox_str, per, 32)
    
    # XOR left and sbox_str
    result = xor(left, sbox_str)
    left = result

    # Swapper
    if(i != 15):
      left, right = right, left
    
  # Combination
  combine = left + right

	# Final permutation: final rearranging of bits to get cipher text
  cipher_text = permute(combine, final_perm, 64)
  return binary_to_hex(cipher_text)


def decrypt(plain_text):
  plain_text = hex_to_binary(plain_text)

  # Initial Permutation
  plain_text = permute(plain_text, initial_perm, 64)

  # Splitting
  left = plain_text[0:32]
  right = plain_text[32:64]

  for i in range(0, 16):
    # Expansion D-box: from 32 bits to 48 bits
    right_expanded = permute(right, exp_d, 48)

    # XOR RoundKey[i] and right_expanded
    xor_x = xor(right_expanded, rkb_reversed[i])

    # S-box: subtituting the value from s-box table by calculating row and column
    sbox_str = ""
    for j in range(0, 8):
      row = binary_to_decimal(int(xor_x[j*6] + xor_x[j*6+5]))
      col = binary_to_decimal(int(xor_x[j*6+1] + xor_x[j*6+2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
      val = sbox[j][row][col]
      sbox_str = sbox_str + decimal_to_binary(val)

    # Straight D-box: After substituting rearranging the bits
    sbox_str = permute(sbox_str, per, 32)
    
    # XOR left and sbox_str
    result = xor(left, sbox_str)
    left = result

    # Swapper
    if(i != 15):
      left, right = right, left
    
  # Combination
  combine = left + right

	# Final permutation: final rearranging of bits to get cipher text
  cipher_text = permute(combine, final_perm, 64)
  return binary_to_hex(cipher_text)