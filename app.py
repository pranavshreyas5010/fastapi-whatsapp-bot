from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Replace with your actual Meta WhatsApp values:
VERIFY_TOKEN = "12345"
ACCESS_TOKEN = "EAARZAswajqEkBPCskDRFvYhm7PoCb7DW7qlfpyZAGWApjkc7UXQ8G79iPJ6R9w3NSN9Mq3bcB357HfT0he95vEb6zjeTWPUfJAGZBqQ3QlK9e79Y6Myh9570JVlTRK16sHs5dhRjlYmRUT3sBBbqybaxAT8jZA0al6GjTH88WdLWZCNmakawNJdWb25wESXbCFsdcJJycSu6aNOJKFZBToKBcDvj3s0BX3ZBwMuZBJB7ij6cDQZDZD"
PHONE_NUMBER_ID = "624292667445289"

# Replace with your ngrok URL for the Kabaddi bot
KABADDI_BOT_URL = "https://8b82-14-142-185-230.ngrok-free.app/ask"

# ✅ WhatsApp Webhook Verification (GET)
@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    else:
        return {"status": "error", "message": "Verification failed"}

# ✅ WhatsApp Webhook Handler (POST)
@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    print("Incoming Message:", body)

    try:
        phone_number = body['entry'][0]['changes'][0]['value']['messages'][0]['from']
        message_text = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    except Exception as e:
        print("Error parsing message:", e)
        return {"status": "ok"}

    # Ask the Kabaddi bot
    answer = ask_kabaddi_bot(message_text)

    # Send the answer back to WhatsApp
    send_whatsapp_reply(phone_number, answer)

    return {"status": "success"}

# 🔗 Function to call Kabaddi bot's /ask API
def ask_kabaddi_bot(question):
    try:
        response = requests.post(KABADDI_BOT_URL, json={"question": question})
        return response.json().get("answer", "Sorry, no answer found.")
    except Exception as e:
        return f"Error talking to Kabaddi bot: {e}"

# 🔁 Function to send reply to WhatsApp user
def send_whatsapp_reply(phone_number, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=payload)
    print("WhatsApp API Response:", response.json())
