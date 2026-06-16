from pydantic import BaseModel
from typing import Optional, Literal, List
from datetime import datetime

class URLAnalysisRequest(BaseModel):
    url: str
    session_id: str
    timestamp: Optional[datetime] = None

class URLAnalysisResponse(BaseModel):
    url: str
    session_id: str
    action: Literal["ALLOW", "WARN", "BLOCK"]
    threat_level: Literal["CLEAR", "CAUTION", "CRITICAL"]
    confidence: float
    risk_score: float
    reasons: List[str]
    timestamp: datetime

class PixelAnalysisRequest(BaseModel):
    session_id: str
    image_base64: str
    timestamp: Optional[datetime] = None

class PixelAnalysisResponse(BaseModel):
    session_id: str
    phishing_detected: bool
    confidence: float
    visual_threat_indicators: List[str]
    timestamp: datetime

class SessionEvent(BaseModel):
    session_id: str
    event_type: str
    data: dict
    timestamp: Optional[datetime] = None
