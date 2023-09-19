LANG_TO_VOICE_ID = {"RU" : 0, "EN" : 1}
SELECTED_VOICE_ID = "EN"
REPEATE_MESSAGE_ON_STANDART_OUTPUT = False
ANY_FILE_PLAYING_AT_SECOND = False
ON_HELP_INVOKE_TEXT = """\n============= HELP =============
COMMANDS STRUCTURE: 
    -COMMAND_NAME ARGS

COMMANDS:
    1)  NAME: sao | select_audio_output
        ARGS: None
        Select new audio output
       
    2)  NAME: t | translate
        ARGS: TEXT TO TRANSLATE
        Translate text (by Google Translate)
        
    3)  NAME: l | lang | language
        ARGS: SELECTED LANG ABBREVIATION
        Select new language
    
    4)  NAME: rm | repeat_messages
        ARGS: None
        Repeat (or not) next messages on the standard output
    
    4)  NAME: h | help
        ARGS: None
        Print help message
        
    5)  NAME: e | exit
        ARGS: None
        Exit program
"""

import pyttsx3
import sys
import play_at_micro
from threading import Thread
from googletrans import Translator
from tkinter.filedialog import askopenfilename


#=========================SETUP========================
translator = Translator()
player = play_at_micro.SoundPlayer();
second_player = play_at_micro.SoundPlayer();

player.select_audio_output()
second_player.set_output_device(player.get_output_device())

engine = pyttsx3.init()
SELECTED_VOICE_ID = input("Select lang (RU/EN): ")
engine.setProperty("voice", engine.getProperty('voices')[LANG_TO_VOICE_ID[SELECTED_VOICE_ID]].id)

newVoiceRate = 130
engine.setProperty('rate',newVoiceRate)

print(ON_HELP_INVOKE_TEXT)

#=========================CHECK ARGS========================
def check_args(input_str):
    global SELECTED_VOICE_ID, LANG_TO_VOICE_ID, REPEATE_MESSAGE_ON_STANDART_OUTPUT, ANY_FILE_PLAYING_AT_SECOND, engine, translator
    
    input_str += " "
    
    _input = input_str[1:input_str.find(" ")].lower().replace(" ", "")
    _content = input_str[input_str.find(" ") + 1:]
    
    if (_input == 'sao' or _input == 'select_audio_output'):
        player.select_audio_output()
        
        return 'c'
    
    elif (_input == 't' or _input == 'translate'):
        accepted = False
        
        text = _content
        
        while not accepted:
            translated = translator.translate(text, dest=SELECTED_VOICE_ID.lower());
            
            result = input("Result: " + translated.text + " | Accept? (y/n/e): ")
            if (result == 'e'): 
                return 'c'
            elif (result != 'n'):
                accepted = True
            else:
                text = input("Text: ")
        
        return translated.text
    
    elif (_input == 'l' or _input == 'lang' or _input == 'language'):
        SELECTED_VOICE_ID = _content.replace(" ", "").upper()
        engine.setProperty("voice", engine.getProperty('voices')[LANG_TO_VOICE_ID[SELECTED_VOICE_ID]].id)

        return 'c'
    
    elif (_input == 'rm' or _input == 'repeat_messages'):
        REPEATE_MESSAGE_ON_STANDART_OUTPUT = not REPEATE_MESSAGE_ON_STANDART_OUTPUT
        
        print("Repeat message: " + REPEATE_MESSAGE_ON_STANDART_OUTPUT*"Yes"\
                                 + (not REPEATE_MESSAGE_ON_STANDART_OUTPUT)*"No")
        
        return 'c'
    
    elif (_input == 'pf' or _input == 'play_file'):
        if (_content == 'stop'):
            pass
        
        if (ANY_FILE_PLAYING_AT_SECOND):
            print("File already playing")
            return 'c'
        
        _content = _content.replace(" ", "");
        
        if (_content == ""):
            _content = askopenfilename()
        
        ANY_FILE_PLAYING_AT_SECOND = True
        
        async_file_playing_thread = Thread(target=async_file_playing, args=(second_player, _content,))
        async_file_playing_thread.start()
        
    
    elif (_input == 'h' or _input == 'help'):
        print(ON_HELP_INVOKE_TEXT)
        
        return 'c'
    
    elif (_input == 'exit' or _input == 'e'): exit(0)
    
    return 'c'


#=========================ASYNC================
def async_repeat(_input):
    repeatEngine = pyttsx3.init()
    repeatEngine.setProperty("voice", engine.getProperty('voices')[LANG_TO_VOICE_ID[SELECTED_VOICE_ID]].id)
    
    repeatEngine.say(_input) 
    repeatEngine.runAndWait()

def async_file_playing(player, file_path):
    
    
    player.stream_filename(file_path)
    

#=========================MAIN========================
while True:
    if engine._inLoop:
        engine.endLoop()
    
    input_str = input("ToSpeech: ");
    
    if (input_str.replace(" ", "")[0] == '-'):
        result = check_args(input_str)
        
        if (result == 'c'): continue
        else:               input_str = result
    
    engine.save_to_file(input_str, sys.path[0]+"\\speech.wav")
    engine.runAndWait()
    
    if (REPEATE_MESSAGE_ON_STANDART_OUTPUT):
        t = Thread(target=async_repeat, args=(input_str,))
        t.start()
    
    player.stream_filename('speech.wav') 