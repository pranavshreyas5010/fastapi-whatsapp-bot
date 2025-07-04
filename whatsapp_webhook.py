from fastapi import FastAPI, Request
import requests

app = FastAPI()

VERIFY_TOKEN = "12345"
ACCESS_TOKEN = "EAARZAswajqEkBPMZCpSfouYOIUCZCdCpNnm8VIawRMBJCWo1eizBUvqBhf07RUgZAGhsQx3Xs1GFjPCEy6F74XfXUIfhylJBuQHnZAOocggIkJGlHsT3ZAwEVCVZCuLfJy7CXsQCDWe91mCH9agNuvSFGJCKeeCWgZBOhJKyMSHsZC5uNsh5Nvs0KToRP7hRkJI1DUHmtAcXwcRZCZBD2V67f4jNLRhUVTiYpKxkDBLjtVpHgOzeQgZD"
PHONE_NUMBER_ID = "624292667445289"   # ✅ Correct phone number ID

# ✅ Webhook verification
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

# ✅ Handle incoming messages and reply
@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    body = await request.json()
    print("Incoming Message:", body)

    # Extract message details
    try:
        phone_number = body['entry'][0]['changes'][0]['value']['messages'][0]['from']
        message_text = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    except Exception as e:
        print("Error parsing message:", e)
        return {"status": "ok"}

    # ✅ Send a reply using WhatsApp Cloud API
    reply_message = f"You said: {message_text}"

    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {
            "body": reply_message
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("WhatsApp API Response:", response.json())

    return {"status": "success"}

