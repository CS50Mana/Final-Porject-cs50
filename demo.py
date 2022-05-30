from cgitb import text
import os 
from google.cloud import texttospeech
from google.cloud import texttospeech_v1
from convert import convert_doc, convert_pdf

#----Setting a virtual inv----#
###############################

#I had first to set a virtual environment for this project:
#py -m venv "pyvenv"
# I then installed different packages related to the project

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='massive-hexagon-351107-d6940f0d83db.json'

# I will use client library

#instantiates a client
client=texttospeech_v1.TextToSpeechClient()

#----doc file---#
question= input("If your text is a doc text type 1 ")
if question=="1":
    text_docx="Direct_aid_demande.docx"
    text=convert_doc(text_docx)

    #Set the text input to be sythesized
    synthesis_input= texttospeech_v1.SynthesisInput(text=text)

    #Build the voice request, select the language code fr-FR and ssml
    # voice gender FEMALE 
    voice=texttospeech_v1.VoiceSelectionParams(
        language_code='fr-fr',
        ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio you want returned 
    audio_config=texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    #Perform the text-to-speech request on the input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary
    with open ('audio file_doc.mp3','wb') as output:
        #write the response to the output file.
        output.write(response.audio_content)
        print("Audio content written to file 'output.mp3'")
                

else:
    text_pdf="Master_thesis.pdf"
    text=convert_pdf(text_pdf)
    print(text)
    #Set the text input to be sythesized
    synthesis_input= texttospeech_v1.SynthesisInput(text=text)

    #Build the voice request, select the language code fr-FR and ssml
    # voice gender FEMALE 
    voice=texttospeech_v1.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio you want returned 
    audio_config=texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
        speakingRate=texttospeech_v1.AudioEncoding.1
    )

    #Perform the text-to-speech request on the input with the selected
    # voice parameters and audio file type
    response=client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary
    with open ('audio file_pdf.mp3','wb') as output:
        #write the response to the output file.
        output.write(response.audio_content)
        print("Audio content written to file 'output.mp3'")