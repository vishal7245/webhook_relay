from fastapi import FastAPI, Request, HTTPException
import httpx
import asyncio

app = FastAPI()

TARGET_ENDPOINTS = [
   "https://ronasbnb.com/reminders/whook2.php",
   "https://reminder.tripxap.com/api/webhook"
]

async def forward_payload(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=10)
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
        *[forward_payload(url, payload) for url in TARGET_ENDPOINTS]
    )

    return {"status": "forwarded", "results": results}
