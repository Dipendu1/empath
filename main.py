import os
import struct
import time
import re
import pyttsx3
import pyaudio
import eel
import requests
import speech_recognition as sr
from playsound import playsound
from transformers import pipeline
import cohere
from pymongo import MongoClient
from datetime import datetime

# Initialize Eel with the web folder
eel.init('www')

# Initialize TTS Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('rate', 174)

# Initialize emotion and Cohere models
emotion_model = pipeline("text-classification", model="nateraw/bert-base-uncased-emotion")
co = cohere.Client('2w1VdS2t5bQm9bN76EeeoKnKkPOWX4yc0A88shOZ')

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
db = client['virtual_psychiatrist']
collection = db['responses']

# Load dataset for similarity matching
rows_url = "https://datasets-server.huggingface.co/rows?dataset=ebowwa%2Fhuman-biases-psychiatrist-io&config=default&split=train&offset=0&length=100"
dataset_rows = requests.get(rows_url).json().get("rows", [])

SIMILARITY_THRESHOLD = 0.8  # Set a similarity threshold

# Helper function: Get embeddings for text
def get_embeddings(text):
    response = co.embed(model="small", texts=[text])
    return response.embeddings[0] if response.embeddings else []

# Helper function: Calculate cosine similarity
def cosine_similarity(vec1, vec2):
    dot_product = sum(p * q for p, q in zip(vec1, vec2))
    norm1 = sum(p ** 2 for p in vec1) ** 0.5
    norm2 = sum(q ** 2 for q in vec2) ** 0.5
    return dot_product / (norm1 * norm2)

# Dataset search for similar responses
def search_dataset(user_input):
    user_embedding = get_embeddings(user_input)
    for entry in dataset_rows:
        text = entry['row'].get('text', '')
        if text:
            text_embedding = get_embeddings(text)
            similarity = cosine_similarity(user_embedding, text_embedding)
            if similarity >= SIMILARITY_THRESHOLD:
                return entry['row'].get('response', '')
    return None

# Generate response using Cohere
def generate_cohere_response(emotion, user_input, conversation_history):
    conversation_context = "\n".join(conversation_history[-5:])
    sample_text = "\n".join([item['row'].get('text', '') for item in dataset_rows[:5] if 'text' in item['row']])

    prompt = (
        f"Conversation:\n{conversation_context}\n\n"
        f"Additional context:\n{sample_text}\n\n"
        f"The detected emotion is '{emotion}'. As a virtual psychiatrist, provide an empathetic, solution-oriented response "
        f"to support the user, based on the above context."
    )

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=300,
        temperature=0.5
    )
    return response.generations[0].text.strip()

# Save to MongoDB
def save_to_db(user_input, bot_response, emotion, score):
    collection.insert_one({
        "user_input": user_input,
        "bot_response": bot_response,
        "emotion": emotion,
        "score": score,
        "timestamp": datetime.now()
    })

# Eel exposed functions
@eel.expose
def get_bot_response(user_input, conversation_history):
    results = emotion_model(user_input)
    emotion = results[0]['label']
    score = results[0]['score']

    dataset_reply = search_dataset(user_input)
    if dataset_reply:
        bot_response = f"{dataset_reply} (Matched from dataset)"
    else:
        bot_response = generate_cohere_response(emotion, user_input, conversation_history)
        bot_response = f"{bot_response} (Emotion: {emotion}, Score: {score:.2f})"

    # Save user input and bot response to MongoDB
    save_to_db(user_input, bot_response, emotion, score)

    # Update conversation history with user input and bot response
    conversation_history.append(f"User ({emotion}): {user_input}")
    conversation_history.append(f"Bot: {bot_response}")
    
    return bot_response

# Play assistant sound
@eel.expose
def playAssistantSound():
    music_dir = "web/assets/audio/start_sound.mp3"
    playsound(music_dir)

# Text-to-Speech function
def speak(text):
    engine.say(text)
    eel.DisplayMessage(text)  # Display message on UI
    engine.runAndWait()

# Speech Recognition function
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        return query.lower()
    except Exception as e:
        print(f"Error recognizing speech: {e}")
        return ""

# Command handler
@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
    else:
        query = message

    eel.senderText(query)
    try:
        # Process query and respond
        response = get_bot_response(query, [])
        speak(response)
    except Exception as e:
        print(f"Error in processing command: {e}")

    eel.ShowHood()

# Start the Eel application
if __name__ == '__main__':
    eel.start('index.html', size=(800, 600))
