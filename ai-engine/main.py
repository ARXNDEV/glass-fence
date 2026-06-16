from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import asyncio, time, os, secrets
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

from db import init_db, log_threat, get_threats, get_threat_summary, delete_threat
from models.threat_classifier import ThreatClassifier
import jinja2

app = FastAPI(title="Glass Fence AI Engine", docs_url=None, redoc_url=None)

# 3.8 Prometheus Metrics
threats_total = Counter("gf_threats_total", "Total threats detected", ["category", "blocked"])
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# 3.6 Basic Auth
security = HTTPBasic()

def verify_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv("GF_AI_ADMIN_USER", "admin"))
    correct_password = secrets.compare_digest(credentials.password, os.getenv("GF_AI_ADMIN_PASSWORD", "admin"))
    if not (correct_username and correct_password):
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# State
models_ready = False
startup_time = time.time()
classifier = None

# 3.4 WebSocket Event Bus
class ThreatEventBus:
    def __init__(self):
        self.queues = []

    async def publish(self, event: dict):
        for q in self.queues:
            await q.put(event)

    async def subscribe(self):
        q = asyncio.Queue()
        self.queues.append(q)
        try:
            while True:
                yield await q.get()
        finally:
            self.queues.remove(q)

threat_event_bus = ThreatEventBus()

# 3.1 /health
@app.get("/health")
async def health():
    return {
        "status": "ok" if models_ready else "loading",
        "models_loaded": models_ready,
        "uptime_seconds": round(time.time() - startup_time),
        "version": "1.0.0"
    }

def _load_models_sync():
    global classifier
    classifier = ThreatClassifier()
    return True

@app.on_event("startup")
async def startup_event():
    await init_db()
    global models_ready
    await asyncio.to_thread(_load_models_sync)
    models_ready = True

class ScreenURLRequest(BaseModel):
    url: str
    session_id: str = "unknown"

# 3.3 /screen-url
@app.post("/screen-url")
async def screen_url(payload: ScreenURLRequest):
    if not models_ready:
        return JSONResponse(status_code=503, content={"error": "Models loading"})

    result = await classifier.classify_url(payload.url)
    blocked = result["score"] > 0.75
    
    # 3.8 Update Metrics
    threats_total.labels(category=result["category"], blocked=str(blocked).lower()).inc()
    
    # 3.5 Log threat
    await log_threat(
        session_id=payload.session_id,
        url=payload.url,
        score=result["score"],
        category=result["category"],
        blocked=blocked
    )
    
    # Publish to WS
    await threat_event_bus.publish({
        "url": payload.url,
        "score": result["score"],
        "category": result["category"],
        "blocked": blocked,
        "session_id": payload.session_id,
        "timestamp": __import__('datetime').datetime.now()
    })

    return {
        "url": payload.url,
        "score": result["score"],
        "category": result["category"],
        "blocked": blocked,
        "reason": result["reason"]
    }

# 3.4 /ws/threats
@app.websocket("/ws/threats")
async def threat_feed(websocket: WebSocket):
    await websocket.accept()
    try:
        async for event in threat_event_bus.subscribe():
            await websocket.send_json({
                "url": event["url"],
                "threat_score": round(event["score"], 3),
                "category": event["category"],
                "blocked": event["blocked"],
                "session_id": event["session_id"],
                "ts": event["timestamp"].isoformat()
            })
    except WebSocketDisconnect:
        pass

# 3.5 Threat REST endpoints
@app.get("/threats", dependencies=[Depends(verify_auth)])
async def list_threats():
    return await get_threats()

@app.get("/threats/summary", dependencies=[Depends(verify_auth)])
async def threats_summary():
    return await get_threat_summary()

@app.delete("/threats/{threat_id}", dependencies=[Depends(verify_auth)])
async def remove_threat(threat_id: int):
    await delete_threat(threat_id)
    return {"status": "deleted"}

# 3.7 Admin Dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Glass Fence | AI Admin</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { background: #000; color: #fff; font-family: monospace; padding: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #333; padding: 8px; text-align: left; }
        th { background: #111; }
        .blocked { color: #f00; }
        .safe { color: #0f0; }
        .bar { background: #333; height: 20px; display: inline-block; }
    </style>
</head>
<body>
    <h1>Glass Fence AI Engine | Dashboard</h1>
    <h3>Threat Summary</h3>
    <ul>
        {% for cat, count in summary.items() %}
        <li>{{ cat }}: {{ count }} <div class="bar" style="width: {{ count * 10 }}px;"></div></li>
        {% endfor %}
    </ul>
    <h3>Recent Events</h3>
    <table>
        <tr><th>Time</th><th>URL</th><th>Category</th><th>Score</th><th>Blocked</th></tr>
        {% for t in threats %}
        <tr>
            <td>{{ t.ts }}</td>
            <td>{{ t.url[:60] }}</td>
            <td>{{ t.category }}</td>
            <td>{{ "%.2f"|format(t.score) }}</td>
            <td class="{{ 'blocked' if t.blocked else 'safe' }}">{{ t.blocked }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.get("/dashboard", response_class=HTMLResponse, dependencies=[Depends(verify_auth)])
async def dashboard():
    summary = await get_threat_summary()
    threats = await get_threats(50)
    template = jinja2.Template(DASHBOARD_TEMPLATE)
    return template.render(summary=summary, threats=threats)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
