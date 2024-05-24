import openai

def setup_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)

def transcribe_audio(client, audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        return transcript.text

def fetch_ai_response(client, input_text):
    messages = [{"role":"user","content": input_text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages) 
    return response.choices[0].message.content

def text_to_audio(client, text, audio_path):
    response = client.audio.speech.create(model="tts-1", voice="nova", input=text)
    response.stream_to_file(audio_path)