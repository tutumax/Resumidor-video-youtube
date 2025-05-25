from pytubefix import YouTube
from pytubefix.cli import on_progress
import speech_recognition as sr
import os

url = input("Digite a Url do seu video do Youtube: ")

try:
    yt = YouTube(url, on_progress_callback=on_progress)
    print(f"Título: {yt.title}")

    ys = yt.streams.get_audio_only()
    audio_path = ys.download(output_path=r'C:\Downloads')


    base, ext = os.path.splitext(audio_path)
    wav_path = base + '.wav'
    os.system(f'ffmpeg -y -i "{audio_path}" "{wav_path}"')

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)

    frase = recognizer.recognize_google(audio, language='pt-BR')
    print("Transcrição:", frase)
except Exception as e:
    print(f"Erro durante download ou transcrição: {e}")

try:
    from openai import OpenAI

    client = OpenAI(
      api_key = 'SUA_API_KEY',
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": (
                    "Resuma o seguinte texto do YouTube de forma clara, destacando os principais pontos e ideias centrais. "
                    "Organize o conteúdo em tópicos ou seções conforme o vídeo avança. Seja objetivo, sem introduções longas.\n\n"
                    f"{frase}"
                ),
            },
        ]
    )

    print(completion.choices[0].message)
except Exception as e:
    print(f"Erro ao chamar a API OpenAI: {e}")