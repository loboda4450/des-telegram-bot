import cv2

from telethon import TelegramClient, events
from DES import DES
from RNGvideo import Primes, RNGutils
from AuxUtils import get_key


with open("config.txt", "r") as config:
    cfg = [line.rstrip() for line in config]


client = TelegramClient('bot', int(cfg[0].strip()), cfg[1].strip()).start(bot_token=cfg[2].strip())
config.close()
des = DES()
primes = Primes.Primes()
rng = RNGutils.RNGutils()
video = cv2.VideoCapture('RNGvideo/video_sample.mp4')
w, h = int(video.get(3)), int(video.get(4))


@client.on(events.InlineQuery)
async def querylist(event):
    if 2 < len(event.text) < 257:
        if event.text[-2:] == '.c':
            key = get_key(video=video, rng=rng, primes=primes, w=w, h=h)
            ciph = des.run(key=key, text=event.text[:-2], encrypt=True).encode("utf-8").hex()

            await event.answer(
                [event.builder.article('cipher',
                                       text=f'```Ciphered: {ciph}'
                                            f'\nCiphered with key: {key}'
                                            f'\nCopy and paste to decipher: {key} {ciph}.d```')])

        elif event.text[-2:] == '.d':
            data = event.text.split(' ')

            if len(data[0]) == 8:
                await event.answer([event.builder.article(
                    f'decipher', text=f'```Key: {data[0]}\n'
                                      f'Deciphered: {des.run(key=data[0], text=bytes.fromhex(data[1][:-2]).decode("utf-8"), encrypt=False)}```')])
            else:
                await event.answer([event.builder.article('**KEY ERROR**', text='Key is not 8 signs long')])

        else:
            await event.answer([event.builder.article('Wrong switch',
                                                      text=f'**USAGE**:\n__message.c__ to cipher'
                                                           f'\n__key + message.d__ to decipher')])

    else:
        await event.answer([event.builder.article('**USAGE**',
                                                  text=f'**USAGE**:\n__message.c__ to cipher'
                                                       f'\n__key + message.d__ to decipher'
                                                       f'\nmessage to cipher must be upto 255 chars long (without switch)')])


@client.on(events.NewMessage)
async def answer(event):
    if 2 < len(event.text) < 257:
        if event.text[-2:] == '.c':
            key = get_key(video=video, rng=rng, primes=primes, w=w, h=h)
            ciph = (des.run(key=key, text=event.text[:-2], encrypt=True)).encode("utf-8").hex()
            await event.reply(
                f'```Ciphered: {ciph}'
                f'\nCiphered with key: {key}'
                f'\nCopy and paste to decipher: {key} {ciph}.d```')

        elif event.text[-2:] == '.d':
            data = event.text.split(' ')
            if len(data[0]) == 8:
                deciph = des.run(key=data[0], text=bytes.fromhex(data[1][0: -2]).decode("utf-8"), encrypt=False)
                await event.reply(f'```Key: {data[0]}\n'
                                  f'Deciphered: {deciph}```')

            else:
                await event.reply('**KEY ERROR!**\nKey is not 8 signs long')

    else:
        await event.reply('**USAGE**:\n__message.c__ to cipher\n__key + message.d__ to decipher'
                          '\nmessage to cipher must be upto 255 chars long (without switch)')


client.start()
client.run_until_disconnected()
