from AuxTables import ip_1_table, expansion_table, permutation_table, ip_table, pc_1_table, pc_2_table, shift_table
from AuxUtils import split, string_to_bit_conv, bits_to_string_conv, permute, xor, expand, substitute, shift, padd, \
	depadd


class DES:
	def __init__(self):
		self.key = None
		self.text = None
		self.keys = list()

	def run(self, key, text, encrypt=True, padding=False):
		self.key = key
		self.text = text

		if encrypt and padding:
			self.text += padd(self.text)

		self.keygen()
		text_blocks = split(self.text, 8)
		result = list()
		for block in text_blocks:
			block = string_to_bit_conv(block)
			block = permute(block, ip_table)
			left, right = split(block, 32)
			for i in range(16):
				right_extended = expand(right, expansion_table)
				if encrypt:
					tmp = xor(self.keys[i], right_extended)
				else:
					tmp = xor(self.keys[15 - i], right_extended)

				tmp = xor(left, permute(substitute(tmp), permutation_table))
				left = right
				right = tmp
			result += permute(right + left, ip_1_table)

		final_res = bits_to_string_conv(result)

		return depadd(final_res) if not encrypt and padding else final_res

	def keygen(self):
		self.keys = []
		key = string_to_bit_conv(self.key)
		key = permute(key, pc_1_table)
		left, right = split(key, 28)
		for i in shift_table:
			left, right = shift(left, right, i)
			tmp = left + right
			self.keys.append(permute(tmp, pc_2_table))
