from DES import DES
from AuxUtils import get_key
import cv2
from RNGvideo import Primes, RNGutils


def main():
	primes = Primes.Primes()
	rng = RNGutils.RNGutils()
	video = cv2.VideoCapture('RNGvideo/video_sample.mp4')
	w, h = int(video.get(3)), int(video.get(4))

	while True:
		key = str(get_key(video=video, rng=rng, primes=primes, w=w, h=h))
		key2 = str(get_key(video=video, rng=rng, primes=primes, w=w, h=h))
		key3 = str(get_key(video=video, rng=rng, primes=primes, w=w, h=h))
		if len(key) == 8 and len(key2) == 8 and len(key3) == 8:
			break

	des = DES()

	with open('test', 'r') as f:
		with open('ciphered', 'w') as ciphered:
			with open('deciphered', 'w') as deciphered:
				text = f.read()
				text = text.strip()
				pos = 0
				pos2 = 32
				while len(text) > pos:
					to_ciph = text[pos:pos2]
					pos += 32
					pos2 += 32
					pad = len(to_ciph) % 8
					progress = round(pos/len(text), 3)
					print(f'progress: {progress}') if progress <= 1 else print('')

					ciph = des.run(key=key, text=to_ciph, encrypt=True, padding=pad)
					ciph1 = des.run(key=key2, text=ciph, encrypt=False)
					ciph2 = des.run(key=key3, text=ciph1, encrypt=True).encode("utf-8").hex() + '\n'
					ciphered.write(ciph2)

					deciph = des.run(key=key3, text=bytes.fromhex(ciph2).decode("utf-8"), encrypt=False)
					deciph1 = des.run(key=key2, text=deciph, encrypt=True)
					deciph2 = des.run(key=key, text=deciph1, encrypt=False, padding=pad)
					deciphered.write(deciph2)


if __name__ == '__main__':
	main()
