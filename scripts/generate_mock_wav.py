import os
import io
import numpy as np
import wave
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Definice konverzace
dialogue = [
    {"speaker": "S1", "text": "Dobrý den, vítám vás u testování systému FutuGen v režimu stereo. Moje jméno je Petr."},
    {"speaker": "S2", "text": "Děkuji Petře. Tady je Jana. Proč je tato nahrávka ve steru?"},
    {"speaker": "S1", "text": "Protože chceme simulovat reálný klientský hovor, kde je operátor v levém kanále a klient v pravém."},
    {"speaker": "S2", "text": "To je chytré. Takže systém teď přesně ví, kdo kdy mluví?"},
    {"speaker": "S1", "text": "Přesně tak, i když se překrýváme. Pokud ale začnu mluvit o tvoji kreditní kartě, klasifikátor nás stopne."}
]

print("🎙️ Generuji českou STEREO nahrávku...")

# List pro uložení kanálů
left_channel = []
right_channel = []

for line in dialogue:
    print(f"  -> Generuji {line['speaker']}...")
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy" if line['speaker'] == "S1" else "shimmer",
        input=line['text'],
        response_format="wav"
    )
    
    # Přečteme WAV data
    with io.BytesIO(response.content) as wav_io:
        with wave.open(wav_io, 'rb') as wf:
            params = wf.getparams()
            data = wf.readframes(wf.getnframes())
            samples = np.frombuffer(data, dtype=np.int16)
            
            # Pokud je S1, dáme do levého, pravý ztlumíme
            # Pokud je S2, dáme do pravého, levý ztlumíme
            if line['speaker'] == "S1":
                left_channel.append(samples)
                right_channel.append(np.zeros_like(samples))
            else:
                left_channel.append(np.zeros_like(samples))
                right_channel.append(samples)

# Spojíme všechny úseky
left_full = np.concatenate(left_channel)
right_full = np.concatenate(right_channel)

# Vytvoříme stereo nahrávku
stereo_signal = np.vstack((left_full, right_full)).T.flatten()

# Uložíme jako STEREO WAV
with wave.open("mock.wav", "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(24000) # OpenAI TTS default for WAV
    wf.writeframes(stereo_signal.astype(np.int16).tobytes())

print("✅ STEREO mock.wav byl úspěšně vytvořen (L=S1, R=S2).")
