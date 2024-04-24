from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
import sounddevice
import pygame
import speech_recognition as sr
import time
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
)

pygame.mixer.init()

def generate_response(prompt):
    start_time = time.time()
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150
    )
    elapsed_time = time.time() - start_time
    print(f"Response Gen: {elapsed_time} seconds")
    return response.choices[0].text.strip()

def recognize_speech():
    start_time = time.time()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("say something...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")
        elapsed_time = time.time() - start_time
        print(f"Speech recognition: {elapsed_time} seconds")
        return user_input
    except sr.UnknownValueError:
        print("Sorry I couldn't understand that")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition request failed: {e}")
        return ""

def text_to_speech(text):
    start_time = time.time()
    tts = gTTS(text)
    tts.save("response.mp3")
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.wait()
    elapsed_time = time.time() - start_time
    print(f"tts: {elapsed_time} seconds")

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
