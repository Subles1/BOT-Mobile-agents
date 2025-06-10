from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from sqlalchemy.orm import Session
from datetime import datetime

from .database import SessionLocal, init_db, Click

app = FastAPI()

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/click")
def click(target_url: str, user_id: str, db: Session = Depends(get_db)):
    if not target_url:
        raise HTTPException(status_code=400, detail="target_url required")
    click = Click(user_id=user_id, target_url=target_url, timestamp=datetime.utcnow())
    db.add(click)
    db.commit()
    return RedirectResponse(url=target_url)

@app.get("/report")
def report(db: Session = Depends(get_db)):
    result = db.query(Click.target_url, Click.user_id).all()
    stats = {}
    for url, user in result:
        stats.setdefault(url, {})
        stats[url][user] = stats[url].get(user, 0) + 1
    return stats


async def _get_json(client: httpx.AsyncClient, method: str, url: str, **kwargs):
    response = await client.request(method, url, timeout=10, **kwargs)
    response.raise_for_status()
    return response.json()


async def fetch_binance_offers(ref: str) -> list[dict]:
    """Fetch 5 latest P2P offers from Binance."""
    payload = {
        "page": 1,
        "rows": 5,
        "payTypes": [],
        "tradeType": "BUY",
        "asset": "USDT",
        "fiat": "RUB",
    }
    async with httpx.AsyncClient() as client:
        data = await _get_json(
            client,
            "POST",
            "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",
            json=payload,
        )

    offers = []
    for item in data.get("data", [])[:5]:
        adv = item.get("adv", {})
        adv_no = adv.get("advNo")
        url = f"https://p2p.binance.com/en/advertiserDetail?advertiserNo={adv_no}"
        if ref:
            url = f"{url}?ref={ref}"
        offers.append({
            "adv_no": adv_no,
            "price": adv.get("price"),
            "asset": adv.get("asset"),
            "fiat": adv.get("fiatUnit"),
            "trade_type": adv.get("tradeType"),
            "url": url,
        })
    return offers


async def fetch_bybit_offers(ref: str) -> list[dict]:
    """Fetch 5 latest P2P offers from Bybit."""
    params = {
        "userId": 0,
        "tokenId": "USDT",
        "currencyId": "RUB",
        "payment": "all",
        "side": 1,
        "size": 5,
        "page": 1,
    }
    async with httpx.AsyncClient() as client:
        data = await _get_json(
            client,
            "GET",
            "https://api2.bybit.com/fiat/otc/v2/public/ad/list",
            params=params,
        )

    offers = []
    for item in data.get("result", {}).get("items", [])[:5]:
        adv_id = item.get("id")
        url = f"https://www.bybit.com/fiat/trade/otc/detail?id={adv_id}"
        if ref:
            url = f"{url}?ref={ref}"
        offers.append({
            "adv_id": adv_id,
            "price": item.get("price"),
            "asset": item.get("tokenId"),
            "fiat": item.get("currencyId"),
            "trade_type": "BUY" if item.get("side") == 1 else "SELL",
            "url": url,
        })
    return offers


@app.get("/offers/binance")
async def binance_offers(ref: str = ""):
    return await fetch_binance_offers(ref)


@app.get("/offers/bybit")
async def bybit_offers(ref: str = ""):
    return await fetch_bybit_offers(ref)
