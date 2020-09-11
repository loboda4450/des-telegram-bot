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

        if len(key) == 8:
            break

    text = input('Tell me what you desire:\n')
    des = DES()

    ciph = (des.run(key=key, text=text, encrypt=True)).encode("utf-8").hex()
    deciph = des.run(key=key, text=bytes.fromhex(ciph).decode("utf-8"), encrypt=False)

    print(f'Key: {key}\nCiphered: {ciph}\nDeciphered: {deciph}')


if __name__ == '__main__':
    main()
