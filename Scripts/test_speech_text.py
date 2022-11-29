import azure.cognitiveservices.speech as speechsdk
import time
import pickle
from typing import List

# Credenciales para el servicio
SUBSCRIPTION_KEY = "[SUBSCRIPTION_KEY]"
SERVICE_REGION = "[SERVICE_REGION]"

def speech_recognize_continuous_from_file(filename : str):
    """
    Todo este código proviene de este repositorio, aunque he modificado un par de cosas:
    https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/python/console

    Debe necesariamente utilizarse el método start_continuous_recognition, pues en caso contrario solamente
    reconoce los primeros 15 segundos de audio.
    """
    speech_config = speechsdk.SpeechConfig(subscription=SUBSCRIPTION_KEY, region=SERVICE_REGION, )
    speech_config.speech_recognition_language="es-CO"
    speech_config.enable_dictation()
    speech_config.output_format = speechsdk.OutputFormat(1)

    audio_config = speechsdk.audio.AudioConfig(filename=filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    transcripcion = []
    agregar_a_transcripcion = lambda f : print(f.result.text) #transcripcion.append(f.result.text)

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(agregar_a_transcripcion)

    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    return transcripcion


def separar_conversacion(transcripcion : List) -> List:
    frase, max_palabras = transcripcion[0], len(transcripcion[0].split())
    frases_completas = []

    for elemento in transcripcion[1:]:
        if len(elemento) > max_palabras:
            frase, max_palabras = elemento, len(elemento.split())
        else:
            frases_completas.append(frase)
            frase, max_palabras = elemento, len(elemento.split())
        
    return frases_completas


if __name__ == "__main__":
    filename = 'SPEAKER_01_24.wav'
    texto_transcripcion = speech_recognize_continuous_from_file(filename)
    for frase in texto_transcripcion:
        print(frase)

    # with open('transcripcion_v2.pickle', 'wb') as f:
    #    pickle.dump(texto_transcripcion, f)

    # print("Terminada la transcripción!")

    # with open('transcripcion_v2.pickle', 'rb') as f:
    #     texto_transcripcion = pickle.load(f)

    # transcripcion_limpia = separar_conversacion(texto_transcripcion)
    # str_transcripcion = ' '.join(transcripcion_limpia)
    # print(str_transcripcion)
