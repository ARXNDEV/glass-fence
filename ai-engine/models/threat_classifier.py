import os
from typing import Dict, Any, TypedDict
from transformers import pipeline
from langgraph.graph import StateGraph, END
from models.url_classifier import URLThreatClassifier

# State definition for LangGraph
class ThreatState(TypedDict):
    url: str
    score: float
    category: str
    blocked: bool
    reason: str
    features: Dict[str, Any]

class ThreatClassifier:
    def __init__(self):
        self.xgb_classifier = URLThreatClassifier()
        # Initialize BERT pipeline (lazy loading can be used, but we'll do it here)
        print("[GF-AI] Loading BERT model: distilbert-base-uncased-finetuned-sst-2-english")
        self.bert_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(ThreatState)

        # Define nodes
        workflow.add_node("extract_features", self.node_extract_features)
        workflow.add_node("xgb_classify", self.node_xgb_classify)
        workflow.add_node("bert_classify", self.node_bert_classify)

        # Define edges
        workflow.set_entry_point("extract_features")
        workflow.add_edge("extract_features", "xgb_classify")

        # Conditional edge: if XGBoost confidence is low or it's suspicious, use BERT
        workflow.add_conditional_edges(
            "xgb_classify",
            self.should_run_bert,
            {
                True: "bert_classify",
                False: END
            }
        )
        workflow.add_edge("bert_classify", END)

        return workflow.compile()

    def node_extract_features(self, state: ThreatState) -> ThreatState:
        features = self.xgb_classifier.extractor.extract(state["url"])
        state["features"] = features
        return state

    def node_xgb_classify(self, state: ThreatState) -> ThreatState:
        # We reuse the predict method from url_classifier
        risk_score, threat_level, reasons, _ = self.xgb_classifier.predict(state["url"])
        state["score"] = risk_score
        
        if risk_score >= 0.7:
            state["category"] = "phishing"
            state["blocked"] = True
        elif risk_score >= 0.4:
            state["category"] = "suspicious"
            state["blocked"] = False
        else:
            state["category"] = "safe"
            state["blocked"] = False
            
        state["reason"] = "; ".join(reasons) if reasons else "No threats detected"
        return state

    def should_run_bert(self, state: ThreatState) -> bool:
        # Run BERT if it's suspicious (needs further analysis)
        return state["category"] == "suspicious"

    def node_bert_classify(self, state: ThreatState) -> ThreatState:
        # In a real scenario, we'd fetch the URL content and classify.
        # Here we simulate by classifying the URL string itself.
        try:
            result = self.bert_classifier(state["url"])[0]
            if result['label'] == 'NEGATIVE':
                # Increase score slightly if text content is considered negative/suspicious
                state["score"] = min(1.0, state["score"] + 0.2)
                state["reason"] += "; BERT detected negative sentiment/suspicious content"
                if state["score"] >= 0.7:
                    state["category"] = "malware"
                    state["blocked"] = True
        except Exception as e:
            print(f"[GF-AI] BERT error: {e}")
        return state

    async def classify_url(self, url: str) -> dict:
        initial_state = ThreatState(
            url=url,
            score=0.0,
            category="safe",
            blocked=False,
            reason="",
            features={}
        )
        # We use asyncio.to_thread because graph execution might be blocking depending on implementations
        import asyncio
        final_state = await asyncio.to_thread(self.graph.invoke, initial_state)
        
        return {
            "score": final_state["score"],
            "category": final_state["category"],
            "blocked": final_state["blocked"],
            "reason": final_state["reason"]
        }
