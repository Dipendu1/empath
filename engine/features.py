# import sqlite3
# import struct
# from playsound import playsound
# import eel
# import re
# import os
# import hugchat
# import os
# import webbrowser
# import pyttsx3
# import pyaudio
# import webbrowser
# from pipes import quote
# from pydub import AudioSegment
# from pydub.playback import play
# import time
# from engine.command import speak
# from engine.config import ASSISTANT_NAME

# from hugchat import hugchat
# # import pywhatkit as kit
# # import pvporcupine


# def playAssistantSound():
#     music_dir = "www\\assets\\audio\\start_sound.mp3"
#     playsound(music_dir)

# engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def openCommand(query):
#     # Establish a connection to your database
#     connection = sqlite3.connect('your_database_name.db')  # Update with your database name
#     cursor = connection.cursor()  # Create a cursor object

#     query = query.replace(ASSISTANT_NAME, "")
#     query = query.replace("open", "")
#     query = query.lower()

#     app_name = query.strip()

#     if app_name != "":
#         try:
#             cursor.execute(
#                 'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
#             results = cursor.fetchall()

#             if len(results) != 0:
#                 speak("Opening " + query)
#                 os.startfile(results[0][0])

#             else:
#                 cursor.execute(
#                     'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
#                 results = cursor.fetchall()

#                 if len(results) != 0:
#                     speak("Opening " + query)
#                     webbrowser.open(results[0][0])

#                 else:
#                     speak("Opening " + query)
#                     try:
#                         os.system('start ' + query)
#                     except Exception:
#                         speak("not found")
#         except Exception as e:
#             speak("Something went wrong")
#             print(e)  # Optional: print the error for debugging
#         finally:
#             connection.close()

# def hotword():
#     porcupine=None
#     paud=None
#     audio_stream=None
#     try:
       
#         # pre trained keywords    
#         porcupine=porcupine.create(keywords=["jarvis","alexa"]) 
#         paud=pyaudio.PyAudio()
#         audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
#         # loop for streaming
#         while True:
#             keyword=audio_stream.read(porcupine.frame_length)
#             keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

#             # processing keyword comes from mic 
#             keyword_index=porcupine.process(keyword)

#             # checking first keyword detetcted for not
#             if keyword_index>=0:
#                 print("hotword detected")

#                 # pressing shorcut key win+j
#                 import pyautogui as autogui
#                 autogui.keyDown("win")
#                 autogui.press("j")
#                 time.sleep(2)
#                 autogui.keyUp("win")
                
#     except:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()

# # chat bot 
# # def chatBot(query):
# #     user_input = query.lower()
# #     chatbot = hugchat.ChatBot(cookie_path="engine\cookie.json")
# #     id = chatbot.new_conversation()
# #     chatbot.change_conversation(id)
# #     response =  chatbot.chat(user_input)
# #     print(response)
# #     speak(response)
# #     return response