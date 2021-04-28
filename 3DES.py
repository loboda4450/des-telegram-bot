# one day i'll finish it.. i swear..

import DES


class TDES:
	def __init__(self):
		self.des = DES.DES()

	def run(self, key, text, cipher):
		if cipher:
			ciph = self.des.run(key=key[0], text=text, encrypt=True, padding=pad)
			ciph1 = self.des.run(key=key[1], text=ciph, encrypt=False)
			ciph2 = self.des.run(key=key[2], text=ciph1, encrypt=True).encode("utf-8").hex()
			print(ciph2)
		else:
			deciph = self.des.run(key=key[2], text=bytes.fromhex(text).decode("utf-8"), encrypt=False)
			deciph1 = self.des.run(key=key[1], text=deciph, encrypt=True)
			deciph2 = self.des.run(key=key[0], text=deciph1, encrypt=False, padding=pad)
			print(deciph2)
