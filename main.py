from openai import OpenAI
import sounddevice
import speech_recognition as sr
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_KEY")
    )

def generate_response(prompt):
    response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.5,
            max_tokens=150
            )
    return response.choices[0].text.strip()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=8)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("...")
        return recognize_speech()
    except sr.RequestError as e:
        print(f"Speech recognition request failed: {e} Try Again..")
        return recognize_speech()
def listen_for_keyword(keyword):
     detected_word = recognize_speech().lower()
     if keyword in detected_word:
         return True
     else:
         return False

def text_to_speech(text):
    tts = gTTS(text)
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def main():
    os.system("mpg321 intro.mp3")
    while True:

        if listen_for_keyword("hey chatbot"):
            os.system("mpg321 dingding.mp3")

        while True:
            os.system("mpg321 ding.mp3")
            user_input = recognize_speech()
            
            if user_input in ['exit', 'goodbye']:
                break
            elif user_input:
                response = generate_response(user_input)
                text_to_speech(response)
                os.system("mpg321 DING.mp3")
            else:
                continue

if __name__ == "__main__":
    main()
