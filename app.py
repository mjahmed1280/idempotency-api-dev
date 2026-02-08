from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# This simulates a persistent store (like Redis)
# In production, you'd store the response body and status code
idempotency_store = {}

class Order(BaseModel):
    item: str
    amount: float

@app.post("/orders")
async def create_order(order: Order, idempotency_key: Optional[str] = Header(None)):
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is missing")

    # 1. Check if the key exists
    if idempotency_key in idempotency_store:
        print(f"Duplicate request detected for key: {idempotency_key}")
        return idempotency_store[idempotency_key]

    # 2. Simulate "Database Update"
    new_order_id = 1001
    result = {
        "order_id": new_order_id,
        "status": "Success",
        "message": f"Order for {order.item} processed."
    }

    # 3. Save the result to the store
    idempotency_store[idempotency_key] = result

    return result