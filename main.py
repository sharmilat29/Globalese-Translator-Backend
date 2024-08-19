from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from gtts import gTTS
import epitran
import os


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to my API!"}

#print(GoogleTranslator().get_supported_languages())

#print("GTTS supports")

class TranslationRequest(BaseModel):
  input_text: str
  target_language: str

@app.post("/translate_to_audio")
def translate_to_audio(request: TranslationRequest):
  print("in this function")
  try:
    translated = GoogleTranslator(source = 'auto', target = request.target_language).translate(request.input_text)
    epi = epitran.Epitran('tel-Telu')
    print(epi.transliterate(translated))
    return {"translated_text": translated}
  except Exception as e:
    raise HTTPException(status_code=500, detail="Translation failed")

  try:
    tts = gTTS(translated, lang = request.target_language, slow = True)
    audio_file = "output.mp3"
    tts.save(audio_file)
  except Exception as e:
    raise HTTPException(status_code=500, detail="Audio generation failed")

  return FileResponse(audio_file, media_type = "audio/mpeg")
