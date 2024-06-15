import google.generativeai as genai
import PIL.Image
import cv2
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
voice = pyttsx3.init()

while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for ambient noise
            audio = recognizer.listen(source)  # Listen for the user's input

            text = recognizer.recognize_google(audio)
            text = text.lower()

            print(f"Recognized: {text}")

            if text == "quit":
                print("Exiting the program.")
                break

            cap = cv2.VideoCapture(0)

        prompt = text

        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
        else:
            cv2.imshow('Captured Image', frame)
            cv2.imwrite('input.jpg', frame)
            print("Analyzing..")
            cv2.destroyAllWindows()

        genai.configure(api_key='YOUR-GEMINI-API-KEY')

        image = PIL.Image.open('input.jpg')
        model = genai.GenerativeModel('gemini-1.5-flash',system_instruction="You are my assistant. i'm infront of you asking questions. The images i provide you are what you see with your eyes. Act like its you seeing them in real time, therefore respond accordingly")
        response=model.generate_content([prompt, image], stream=True)
        response.resolve()
        print(response.text)
        voice.say(response.text)
        voice.runAndWait()

    except sr.UnknownValueError:
        voice.say("Sorry, I did not understand that.")
        print("Sorry, I did not understand that.")
        voice.runAndWait()
        continue        

