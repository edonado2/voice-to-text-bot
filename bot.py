import telebot
import os
import speech_recognition as sr
from pydub import AudioSegment
from config import *

bot = telebot.TeleBot(TELEGRAM_TOKEN)

DEFAULT_LANGUAGE = 'es-ES' 

# Function to handle voice messages
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    try:
        # Download the voice note from Telegram
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the downloaded voice note
        voice_note_path = 'voice_note.ogg'
        with open(voice_note_path, 'wb') as f:
            f.write(downloaded_file)

        # Convert .ogg file to .wav for transcription
        audio = AudioSegment.from_ogg(voice_note_path)
        audio.export("voice_note.wav", format="wav")

        # Transcribe the audio in the selected language
        recognizer = sr.Recognizer()
        with sr.AudioFile('voice_note.wav') as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=DEFAULT_LANGUAGE)

        # Send the transcription as a text message
        bot.send_message(message.chat.id, f"Transcripción: {text}")

        # Clean up the files
        os.remove("voice_note.ogg")
        os.remove("voice_note.wav")

    except Exception as e:
        bot.send_message(message.chat.id, "Lo siento, no pude transcribir la nota de voz.")
        print(e)

bot.polling()
