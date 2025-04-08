from fastapi import FastAPI, Request, HTTPException
import httpx
import asyncio

app = FastAPI()

POST_TARGET_ENDPOINTS = [
   "https://ronasbnb.com/reminders/whook2.php",
   "https://reminder.tripxap.com/api/webhook",
]

GET_TARGET_ENDPOINTS = [
    "https://n8n.tripxap.com/webhook-test/f72c7da2-e62c-4789-a339-16bc8961d4e9",
    "https://n8n.tripxap.com/webhook/f72c7da2-e62c-4789-a339-16bc8961d4e9"
]

async def forward_post_payload(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=10)
            return {"url": url, "status": response.status_code}
        except Exception as e:
            return {"url": url, "error": str(e)}

async def forward_get_payload(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=payload, timeout=10)
            return {"url": url, "status": response.status_code}
        except Exception as e:
            return {"url": url, "error": str(e)}

@app.post("/webhook")
async def webhook_receiver(request: Request):
    try:
        payload = await request.json()
        print(payload)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Forward the payload to all target endpoints
    results = await asyncio.gather(
        *[forward_post_payload(url, payload) for url in POST_TARGET_ENDPOINTS],
        *[forward_get_payload(url, payload) for url in GET_TARGET_ENDPOINTS]
    )

    return {"status": "forwarded", "results": results}
