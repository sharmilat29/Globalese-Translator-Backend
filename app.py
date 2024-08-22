from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
import io
from deep_translator import GoogleTranslator
from gtts import gTTS
import epitran
import os

#Make dictionary for common language supported across all libraries

gtl_to_gtts = { 'afrikaans': 'af', 'amharic': 'am', 'arabic': 'ar', 'bulgarian' : 'bg', 'bosnian' : 'bs', 'catalan' : 'ca', 
               'chinese (simplified)' : 'zh-CN', 'czech' : 'cs', 'danish' : 'da', 'dutch' : 'nl', 'english' : 'en', 'finnish' : 'fi', 
               'french' : 'fr', 'german' : 'de', 'greek' : 'el', 'gujarati':'gu', 
               'hebrew' : 'iw', 'hindi' : 'hi', 'hungarian' : 'hu', 'icelandic' : 'is', 
               'indonesian' : 'id', 'italian' : 'it', 'japanese' : 'ja',
               'javanese' : 'jw', 'kannada' : 'kn', 'korean' : 'ko', 'latin' : 'la', 
               'latvian' : 'lv', 'lithuanian' : 'lt', 'malay' : 'ms', 'malayalam' : 'ml',
               'marathi' : 'mr', 'myanmar' : 'my', 'nepali' : 'ne', 'norwegian' : 'no', 
               'polish' : 'pl', 'portuguese' : 'pt', 'punjabi' : 'pa', 'romanian' : 'ro',
               'russian' : 'ru', 'serbian' : 'sr', 'sinhala' : 'si', 'swedish' : 'sv', 
               'tamil' : 'ta', 'telugu' : 'te', 'thai' : 'th', 'turkish' : 'tr', 'ukrainian' : 'uk',
               'urdu' : 'ur', 'vietnamese' : 'vi' }

gtl_to_epitran = {'amharic': 'amh-Ethi', 'arabic': 'ara-Arab', 'catalan' : 'cat-Latn', 'chinese (simplified)' : 'cmn-Hans',
                  'czech' : 'ces-Latn', 'english' : 'eng-Latn', 'french' : 'fra-Latn', 'german' : 'deu-Latn', 
                  'hindi' : 'hin-Deva', 'indonesian' : 'ind-Latn', 'italian' : 'ita-Latn',
                  'javanese' : 'jav-Latn', 'malay' : 'msa-Latn', 'malayalam' : 'mal-Mlym',
                  'marathi' : 'mar-Deva', 'myanmar' : 'mya-Mymr', 'polish' : 'pol-Latn', 'portuguese' : 'por-Latn', 'punjabi' : 'pa', 
                  'romanian' : 'ron-Latn',
                  'russian' : 'rus-Cyrl', 'serbian' : 'srp-Latn', 'sinhala' : 'sin-Sinh', 'swedish' : 'swe-Latn', 'tamil' : 'tam-Taml', 'telugu' : 'tel-Telu', 'thai' : 'tha-Thai', 'turkish' : 'tur-Latn', 'ukrainian' : 'ukr-Cyrl',
                  'urdu' : 'urd-Arab', 'vietnamese' : 'vie-Latn' }

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


class TranslationRequest(BaseModel):
  input_text: str
  target_language: str

@app.post("/translate_to_phoneme")
def translate_to_phoneme(request: TranslationRequest):

  translated = GoogleTranslator(source = 'auto', target = request.target_language).translate(request.input_text)
  
  try:
    
    if request.target_language in gtl_to_epitran:
      epi = epitran.Epitran(gtl_to_epitran[request.target_language])
      result = epi.transliterate(translated)
      return {"transliterated_text": result}
    else:
      return {"transliterated_text": "Phoneme generation not supported"}
  except Exception as e:
    raise HTTPException(status_code=500, detail="Phoneme generation failed")

@app.post("/translate_to_audio")
def translate_to_audio(request: TranslationRequest):
  
  translated = GoogleTranslator(source = 'auto', target = request.target_language).translate(request.input_text)
  try:
    tts = gTTS(translated, lang = gtl_to_gtts[request.target_language], slow = True)
    audio_buffer = io.BytesIO()
    tts.save(audio_buffer)
    audio_buffer.seek(0)
    return Response(content = audio_buffer.read(), media_type = "audio/mpeg")
    
  except Exception as e:
    raise HTTPException(status_code=500, detail="Audio generation failed")

if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app)