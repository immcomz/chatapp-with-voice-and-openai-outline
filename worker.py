from openai import OpenAI
import requests

openai_client = OpenAI()


# -------------------------
# Speech to Text (Watson)
# -------------------------
def speech_to_text(audio_binary):
    try:
        base_url = "https://sn-watson-stt.labs.skills.network"
        api_url = base_url + "/speech-to-text/api/v1/recognize"

        params = {
            "model": "en-US_Multimedia",
        }

        response = requests.post(
            api_url,
            params=params,
            data=audio_binary
        ).json()

        print("STT response:", response)

        text = ""

        if response.get("results"):
            text = response["results"][0]["alternatives"][0]["transcript"]

        print("recognized text:", text)
        return text

    except Exception as e:
        print("STT ERROR:", str(e))
        return ""


# -------------------------
# Text to Speech (Watson)
# -------------------------
def text_to_speech(text, voice=""):
    try:
        base_url = "https://sn-watson-tts.labs.skills.network"
        api_url = base_url + "/text-to-speech/api/v1/synthesize?output=output_text.wav"

        if voice and voice != "default":
            api_url += "&voice=" + voice

        headers = {
            "Accept": "audio/wav",
            "Content-Type": "application/json",
        }

        json_data = {
            "text": text,
        }

        response = requests.post(api_url, headers=headers, json=json_data)

        print("TTS response:", response.status_code)

        return response.content

    except Exception as e:
        print("TTS ERROR:", str(e))
        return b""


# -------------------------
# OpenAI Processing
# -------------------------
def openai_process_message(user_message):
    try:
        prompt = (
            "Act like a personal assistant. "
            "Answer questions, summarize, translate. "
            "Keep responses short (2–3 sentences)."
        )

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300
        )

        print("OpenAI response received")

        return response.choices[0].message.content

    except Exception as e:
        print("OPENAI ERROR:", str(e))
        return "Sorry, I couldn't process your request."