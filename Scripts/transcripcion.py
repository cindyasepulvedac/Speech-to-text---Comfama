import azure.cognitiveservices.speech as speechsdk
from typing import Tuple, List
import time
from datetime import datetime, timedelta

# Credenciales del servicio de Azure
SUBSCRIPTION_KEY, SERVICE_REGION = "a06f7017a99b409c8d76ca31d4fc7dea", "eastus2"

def transcribir_texto(archivo_audio : str, lenguaje : str = "es-CO", mostrar_avance = False) -> List:
    """
    Esta función permite transcribir un audio a texto, utilizando el servicio de speech Azure.

    Parámetros
    ----------
    archivo_audio : str
        Ruta del archivo de audio a transcribir.
    
    Retorna
    -------
    str
        Cadena de texto con la transcripción.
    """
    
    # Se instancia la clase de configuración de Speech con las credenciales para el servicio de Azure
    config_speech = speechsdk.SpeechConfig(subscription=SUBSCRIPTION_KEY, region=SERVICE_REGION)

    # Se selecciona el lenguaje. Es posible que en algunos casos se deba escoger otro tipo de acento, 
    # si es que el entrevistado no es colombiano.
    config_speech.speech_recognition_language = lenguaje

    # Se habilita que la transcripción tenga puntuación y se selecciona el formato de salida.
    config_speech.enable_dictation()
    config_speech.output_format = speechsdk.OutputFormat(1)

    # Configuración del audio de entrada y del reconoce
    config_audio = speechsdk.audio.AudioConfig(filename = archivo_audio)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config = config_speech, audio_config = config_audio)

    # Se genera una variable de control de los eventos de la transcripción
    done = False

    # Se define una función que se ejecutará cuando se detenga la transcripción
    def _terminar_transcripcion(e: speechsdk.SessionEventArgs):
        print(f'Terminando transcripción... {e}')
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    transcripciones_detalles = []
    _agregar_a_transcripcion = lambda e : transcripciones_detalles.append((e.result.text, e.result.offset, e.result.duration))

    # Conectar los eventos de la transcripción a las funciones definidas
    if mostrar_avance: 
        speech_recognizer.recognizing.connect(lambda e: print(f'Reconociendo texto: {e.result.text}'))

    speech_recognizer.recognized.connect(_agregar_a_transcripcion)

    # Detener la transcripción cuando se termine el audio o se acabe manualmente
    speech_recognizer.session_stopped.connect(_terminar_transcripcion)
    speech_recognizer.canceled.connect(_terminar_transcripcion)

    # Comenzar la transcripción continua
    speech_recognizer.start_continuous_recognition_async()
    # Se hace una pausa para que la transcripción se ejecute
    while not done: 
        time.sleep(.5)
    speech_recognizer.stop_continuous_recognition_async()

    return transcripciones_detalles


def guardar_transcripcion(list_transcripcion : List[Tuple], archivo_salida : str, guardar_con_tiempos = False) -> None:
    """
    Esta función permite guardar un texto en un archivo de texto.

    Parámetros
    ----------
    texto : str
        Cadena de texto a guardar.
    
    archivo_salida : str
        Ruta del archivo de texto a generar.
    """
    if guardar_con_tiempos:
        # Se guarda el texto con los tiempos de inicio y duración de cada frase
        for f in list_transcripcion:
            t_comienzo = datetime(1, 1, 1) + timedelta(microseconds=f[1]/10)
            t_final = datetime(1, 1, 1) + timedelta(microseconds=(f[1]+f[2])/10)

            str_final = f"[{t_comienzo} ---> {t_final}] : '{f[0]}' \n "
            with open(archivo_salida, "a") as archivo:
                archivo.write(str_final)
    else:
        # Unir todos los textos que se transcribieron
        str_final = " ".join([r[0] for r in list_transcripcion])
        with open(archivo_salida, "w") as f:
            f.write(str_final)

if __name__ == "__main__":
    from os.path import join 
    audio_str = "SPEAKER_01_24.wav"
    folder_audios = 'Audios'
    folder_transcripciones = "Transcripciones"

    transcripcion = transcribir_texto(join(folder_audios, audio_str), mostrar_avance = True)
    guardar_transcripcion(transcripcion, join(folder_transcripciones, audio_str.replace('.wav', '.txt')), guardar_con_tiempos = True)