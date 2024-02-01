# uvicorn main:app
# uvicorn main:app --reload
# python -m venv venv
# .\venv\Scripts\activate


#Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai 


# Custom Functions import
from functions.database import store_messages, reset_messages
from functions.openai_request import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech


# init app
app = FastAPI()

# CORS - Origins

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5000",
]

# CORS - Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Check Health 
@app.get("/health")
async def check_health():
    return {"message": "healthy"}   


# Reset Messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}
   


# Get Audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    # Get saved audio
    # audio_input = open("voice.mp3", "rb")

    # Save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
        audio_input = open(file.filename, "rb")
        print("File saved and ready for processing")

    # Decode Audio
    message_decoded = convert_audio_to_text(audio_input)
    print(f"Decoded message: {message_decoded}")

    # Guard: Esnure message decoded 
    if not message_decoded:

        return HTTPException(status_code=400, detail="Failed to decode audio")


    # Get ChatGpt Response
    chat_response = get_chat_response(message_decoded)
    print(f"ChatGPT response: {chat_response}")

    # Guard: Ensure chat response
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Store Messages
    store_messages(message_decoded, chat_response)


    # Convert Chat Response to audio
    audio_output = convert_text_to_speech(chat_response)

    # Guard: Ensure audio response
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to convert chat response to audio")
    
    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

        # Return audio file

    return StreamingResponse(iterfile(), media_type="application/octet-stream")

    
    

# Post bot response 
# Note: Not playing in browser when using post request

# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):

#     print("hello")
    