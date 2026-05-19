import base64
import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS

from worker import speech_to_text, text_to_speech, openai_process_message

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/speech-to-text", methods=["POST"])
def speech_to_text_route():
    try:
        print("processing speech-to-text")

        audio_binary = request.data
        text = speech_to_text(audio_binary)

        return app.response_class(
            response=json.dumps({"text": text}),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        print("ERROR speech_to_text_route:", str(e))
        return app.response_class(
            response=json.dumps({"error": str(e)}),
            status=500,
            mimetype="application/json"
        )


@app.route("/process-message", methods=["POST"])
def process_message_route():
    try:
        user_message = request.json["userMessage"]
        voice = request.json["voice"]

        print("user_message:", user_message)
        print("voice:", voice)

        # OpenAI response
        openai_response_text = openai_process_message(user_message)

        # clean response
        openai_response_text = os.linesep.join(
            [s for s in openai_response_text.splitlines() if s]
        )

        # text to speech
        openai_response_speech = text_to_speech(openai_response_text, voice)
        openai_response_speech = base64.b64encode(openai_response_speech).decode("utf-8")

        return app.response_class(
            response=json.dumps({
                "openaiResponseText": openai_response_text,
                "openaiResponseSpeech": openai_response_speech
            }),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        print("ERROR process_message_route:", str(e))
        return app.response_class(
            response=json.dumps({"error": str(e)}),
            status=500,
            mimetype="application/json"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)