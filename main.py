from deep_translator import GoogleTranslator
from gtts import gTTS
import os

translated = GoogleTranslator(source = 'auto', target = 'telugu').translate(text = 'these are your lungs')
print(translated)

myobj = gTTS(text = translated, lang = 'te', slow = True)
myobj.save("welcome.mp3")

