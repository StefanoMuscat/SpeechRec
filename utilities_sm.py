
import subprocess
from spellchecker import SpellChecker
import tensorflow as tf
import speech_recognition as sr
import pyautogui

# Definire la lista di comandi vocali predefiniti
def open_terminal():
    subprocess.run(["gnome-terminal"])

def play_music():
    subprocess.run(["rhythmbox", "music.mp3"])

def open_website(url):
    subprocess.run(["firefox", url])

# Definire un dizionario di comandi vocali predefiniti
commands = [ ("apri terminale", open_terminal),
                ("riproduci musica", play_music),
                ("apri sito web", open_website)]


def correct_text(text):
    spell = SpellChecker()
    corrected_text = spell.correction(text)
    return corrected_text

def use_google_speech_recognition(audio,r):
    recognized_text = ""
    # Gestisci l'eccezione per quando non viene riconosciuto alcun testo
    try:
        recognized_text = r.recognize_google(audio,language="it-IT", show_all=False)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return
    
    print("Google Speech Recognition thinks you said: " + recognized_text)
    corrected_text = correct_text(recognized_text)
    # Check if the corrected_text is a NoneType
    if corrected_text is None:
        print("Google Speech Recognition could not understand audio")
    else: 
        print("Google Speech Recognition thinks you said: " + corrected_text)
        # Save the corrected text as audio file
        with open("corrected_text.wav", "wb") as f:
            f.write(audio.get_wav_data())
            

    if corrected_text == "aggiungi comando rapido":
        new_command = input("What is the new quick command you want to add? ")
        new_function = input("What function should be executed when the command is triggered? ")
        commands.append((new_command, eval(new_function)))

        with open("quick_commands.txt", "a") as f:
            f.write(f"{new_command},{new_function}\n")
    else: 
        # Stampa il testo dove c'è il cursore
        pyautogui.typewrite(recognized_text)
    
    for command, function in commands:
        if corrected_text == command:
            function()            
            
        
def use_deep_speech(audio, model):
    audio_data = audio.get_wav_data()
    input_data = tf.constant(audio_data, dtype=tf.float32)
    input_data = tf.reshape(input_data, [1, -1, 1])
    prediction = model.predict(input_data)
    recognized_text = prediction.numpy()[0]
    print("DeepSpeech thinks you said: " + recognized_text)

    if recognized_text == "aggiungi comando rapido":
        new_command = input("What is the new quick command you want to add? ")
        new_function = input("What function should be executed when the command is triggered? ")
        commands.append((new_command, eval(new_function)))

        with open("quick_commands.txt", "a") as f:
            f.write(f"{new_command},{new_function}\n")
    else: 
        # Stampa il testo dove c'è il cursore
        pyautogui.typewrite(recognized_text)
        
        
    for command, function in commands:
        if recognized_text == command:
            function()
            break


def inizialized():
    print("Start Inizialization")
    choice = input("Do you want to use Google Speech Recognition or DeepSpeech? (g/d): ")
    
    if choice == "g":
        # Inizializza il recognizer e il correttore ortografico
        r = sr.Recognizer()
        
        # Imposta la soglia di energia
        r.energy_threshold = 4000
        
        
    elif choice == "d":
        # Carica il modello DeepSpeech
        model = tf.saved_model.load("deepspeech-0.6.1-models/deepspeech-0.6.1-models")
        # use_deep_speech(audio, model=model)
    else:
        print("Invalid choice")
    return r 

