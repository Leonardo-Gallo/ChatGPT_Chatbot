from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
import sounddevice
import speech_recognition as sr
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
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
    with sr.Microphone(device_index=3) as source:
        print("say something...")
        audio = recognizer.listen(source, timeout=1)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry I couldn't understand that")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition request failed: {e}")
        return ""

def text_to_speech(text):
    tts = gTTS(text)
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def main():
    print("welcome to my chatbot!")

    with ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            user_input = executor.submit(recognize_speech).result()

            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("goodbye..")
                break

            prompt = f"You: {user_input}\nGPT-3: "
            response = executor.submit(generate_response, prompt).result()

            print(f"GPT-3: {response}")
            executor.submit(text_to_speech, response)

if __name__ == "__main__":
    main()