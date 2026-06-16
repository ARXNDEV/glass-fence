import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os
from typing import Tuple, List, Dict, Any
from utils.feature_extractor import URLFeatureExtractor

MODEL_PATH = "/tmp/gf_xgb_model.pkl"

class URLThreatClassifier:

    def __init__(self):
        self.extractor = URLFeatureExtractor()
        self.model = None
        self._load_or_train()

    def _load_or_train(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            print("[GF-AI] XGBoost model loaded from cache")
        else:
            print("[GF-AI] Training XGBoost model on synthetic data...")
            self._train()

    def _train(self):
        benign = [
            "https://google.com/search?q=python",
            "https://github.com/microsoft/vscode",
            "https://docs.python.org/3/library/",
            "https://stackoverflow.com/questions/",
            "https://en.wikipedia.org/wiki/Machine_learning",
            "https://www.youtube.com/watch?v=abc123",
            "https://aws.amazon.com/ec2/pricing/",
            "https://developer.mozilla.org/en-US/docs/",
            "https://www.npmjs.com/package/react",
            "https://pypi.org/project/fastapi/",
        ] * 60

        phishing = [
            "http://secure-paypal-login.tk/account/verify",
            "http://192.168.1.1/microsoft/signin/password",
            "https://amazon-security-alert.xyz/login?ref=update",
            "http://google-accounts.ga/verify-identity",
            "http://faceb00k-login.ml/signin.php",
            "https://netf1ix-billing-update.top/payment/confirm",
            "http://apple-id-locked-1234.cf/unlock?token=abc",
            "https://secure-banking-login.click/verify.asp?id=xyz",
            "http://login-paypal-secure-verify.xyz/login.php",
            "https://microsoft-account-alert-update.ga/signin",
        ] * 60

        all_urls = benign + phishing
        labels = [0] * len(benign) + [1] * len(phishing)

        X = np.array([self.extractor.to_vector(self.extractor.extract(u)) for u in all_urls])
        y = np.array(labels)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = xgb.XGBClassifier(
            n_estimators=100, max_depth=6, learning_rate=0.1,
            eval_metric='logloss', random_state=42
        )
        self.model.fit(X_train, y_train)
        acc = accuracy_score(y_test, self.model.predict(X_test))
        print(f"[GF-AI] Training complete. Accuracy: {acc:.2%}")

        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(self.model, f)

    def predict(self, url: str) -> Tuple[float, str, List[str], Dict]:
        features = self.extractor.extract(url)
        vector = np.array(self.extractor.to_vector(features)).reshape(1, -1)
        proba = self.model.predict_proba(vector)[0]
        risk_score = float(proba[1])

        reasons = []
        if features.get('has_ip_address'):
            reasons.append("URL uses raw IP address instead of domain")
        if features.get('has_suspicious_keyword'):
            reasons.append("Contains known phishing keywords")
        if features.get('has_suspicious_tld'):
            reasons.append("Uses high-risk top-level domain (.tk, .xyz, etc.)")
        if features.get('url_entropy', 0) > 4.5:
            reasons.append("High URL entropy — possible obfuscation")
        if features.get('subdomain_count', 0) > 3:
            reasons.append("Excessive subdomains — common in phishing")
        if not features.get('has_https'):
            reasons.append("Connection is not encrypted (HTTP)")

        if risk_score >= 0.7:
            threat_level = "CRITICAL"
        elif risk_score >= 0.4:
            threat_level = "CAUTION"
        else:
            threat_level = "CLEAR"

        return risk_score, threat_level, reasons, features
