from vosk import Model, KaldiRecognizer
from audioplayer import AudioPlayer
import pyaudio
import keyboard
import time
import random
import pyautogui
import json


width, height = pyautogui.size()


def thanks():
    answers = ['music/хорошо поработали.mp3',
               'music/хаха ну ты это видел ни в какие ворота не лезет с меня хватит ухожу.mp3',
                'music/удачи я погнал.mp3', 'music/музло.mp3']
    AudioPlayer(answers[random.randint(0, len(answers)-1)]).play(block=True)
    exit()


move = {'вперёд': 'w', 'назад': 's',
        'влево': 'a', 'вправо': 'd', 'стоп': '-'}
tower = {'башню на двенадцать': 'pyautogui.moveTo(width//2-750, height//2, duration=0.25)',
         'башню на три': 'pyautogui.moveTo(width//2+375, height//2, duration=0.25)',
         'башню на шесть': 'pyautogui.moveTo(width//2+750, height//2, duration=0.25)',
         'башню на девять': 'pyautogui.moveTo(width//2-375, height//2, duration=0.25)'}
missile = {'огонь': 'pyautogui.click()', 'бронебойн': 'keyboard.press_and_release("1")',
           'кумулятив': 'keyboard.press_and_release("2")', 'фугасн': 'keyboard.press_and_release("3")'}
instruments = {'комплект': 'keyboard.press_and_release("4")', 'форсаж': 'keyboard.press_and_release("5")',
               'адреналин': 'keyboard.press_and_release("6")'}
message = {'прицел': 'keyboard.press_and_release("shift")', 'чат': 'keyboard.press_and_release("enter")',
           'спасибо': 'thanks()', 'выйди': 'keyboard.press_and_release("shift")'}



def make_something(order):
    # вперед, назад, влево, вправо, стоп

    for i in move.keys():
        if i in order:
            print('MOVING!')

            if 'стоп' not in order:
                keyboard.press(move[i])
            else:
                keyboard.release('w')
                keyboard.release('s')
                keyboard.release('a')
                keyboard.release('d')

            break

    # башню на 12,3,6,9
    for j in tower.keys():
        if j in order:
            print("TOWER")
            pyautogui.moveTo(width // 2, height // 2, duration=0)

            exec(tower[j])

            break

    # огонь, бронебойные, кумулятив, фугасы
    for k in missile.keys():
        if k in order:
            print("MISSILE")
            exec(missile[k])
            break

    # ремкомплект, починка, адреналин, аптечка
    for m in instruments.keys():
        if m in order:
            print("MISSILE")
            exec(instruments[m])
            break

    # прицел, чат, спасибо за службу
    for b in message.keys():
        if (b in order) and ('чат' not in order):
            print("MISSILE")
            exec(message[b])
            break
        elif 'чат' in order:
            exec(message['чат'])
            msg_to_send = str(order.split('чат')[1])
            time.sleep(0.5)
            keyboard.write(msg_to_send)
            time.sleep(0.5)
            exec(message['чат'])
            break


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

model = Model("vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model, 16000)


res = ''
while True:
    data = stream.read(2000, exception_on_overflow=False)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = rec.Result()
        text = json.loads(res)
        print(text['text'])
        make_something(text['text'])
