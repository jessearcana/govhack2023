# record user speech from microphone, pass to google for speech to text conversion
import speech_recognition as sr

def get_user_story_audio():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # # recognize speech using Google Speech Recognition
    try:
        story =  r.recognize_google(audio)
        # print(story)
        return story
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

get_story()
