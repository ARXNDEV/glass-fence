import asyncio
import json
from datetime import datetime
from typing import Dict, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from schemas.types import (
    URLAnalysisRequest, URLAnalysisResponse,
    PixelAnalysisRequest, PixelAnalysisResponse,
    SessionEvent
)
from models.url_classifier import URLThreatClassifier
from utils.pixel_boost import PixelBoostAnalyzer
from graph.knowledge_graph import graph

classifier = URLThreatClassifier()
pixel = PixelBoostAnalyzer()

class WSManager:
    def __init__(self):
        self.connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, sid: str, ws: WebSocket):
        await ws.accept()
        self.connections.setdefault(sid, set()).add(ws)

    def disconnect(self, sid: str, ws: WebSocket):
        if sid in self.connections:
            self.connections[sid].discard(ws)

    async def send(self, sid: str, msg: dict):
        dead = set()
        for ws in self.connections.get(sid, set()):
            try:
                await ws.send_json(msg)
            except Exception:
                dead.add(ws)
        self.connections.get(sid, set()).difference_update(dead)

    async def broadcast(self, msg: dict):
        for sid in list(self.connections.keys()):
            await self.send(sid, msg)

ws_manager = WSManager()

app = FastAPI(
    title="Glass Fence AI Engine",
    description="AI threat detection for Remote Browser Isolation",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "glass-fence-ai", "timestamp": datetime.now().isoformat()}

@app.post("/analyze/url", response_model=URLAnalysisResponse)
async def analyze_url(req: URLAnalysisRequest):
    risk_score, threat_level, reasons, features = classifier.predict(req.url)

    # Check knowledge graph for prior history
    history = graph.get_domain_info(req.url)
    if history.get('known') and history.get('risk_score', 0) > risk_score:
        risk_score = history['risk_score']
        reasons.insert(0, "Domain has known threat history")
        threat_level = "CRITICAL" if risk_score >= 0.7 else "CAUTION"

    graph.add_result(req.url, req.session_id, risk_score, threat_level)

    action = "BLOCK" if risk_score >= 0.7 else ("WARN" if risk_score >= 0.4 else "ALLOW")

    # Push live update to frontend WebSocket
    await ws_manager.send(req.session_id, {
        "type": "threat_update",
        "threat_level": threat_level,
        "url": req.url,
        "risk_score": round(risk_score, 3),
        "action": action,
        "reasons": reasons,
        "timestamp": datetime.now().isoformat(),
    })

    return URLAnalysisResponse(
        url=req.url,
        session_id=req.session_id,
        action=action,
        threat_level=threat_level,
        confidence=round(max(risk_score, 1 - risk_score), 3),
        risk_score=round(risk_score, 3),
        reasons=reasons,
        timestamp=datetime.now()
    )

@app.post("/analyze/pixel", response_model=PixelAnalysisResponse)
async def analyze_pixel(req: PixelAnalysisRequest):
    result = pixel.analyze(req.image_base64)
    score = result.get('phishing_score', 0)
    indicators = pixel.get_indicators(result)
    detected = score >= 0.5

    if detected:
        await ws_manager.send(req.session_id, {
            "type": "pixel_threat",
            "phishing_detected": True,
            "confidence": round(score, 3),
            "indicators": indicators,
            "timestamp": datetime.now().isoformat(),
        })

    return PixelAnalysisResponse(
        session_id=req.session_id,
        phishing_detected=detected,
        confidence=round(score, 3),
        visual_threat_indicators=indicators,
        timestamp=datetime.now()
    )

@app.get("/session/{session_id}/profile")
async def session_profile(session_id: str):
    return graph.get_session_profile(session_id)

@app.get("/graph")
async def get_graph():
    return graph.export_json()

@app.post("/event")
async def session_event(event: SessionEvent):
    await ws_manager.send(event.session_id, {"type": "session_event", **event.dict()})
    return {"status": "ok"}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(ws: WebSocket, session_id: str):
    await ws_manager.connect(session_id, ws)
    try:
        await ws.send_json({
            "type": "connected",
            "session_id": session_id,
            "message": "Glass Fence AI Engine ready",
            "timestamp": datetime.now().isoformat()
        })
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "ping":
                await ws.send_json({"type": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id, ws)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
