import base64
import io
import numpy as np
from PIL import Image, ImageFilter
from typing import Dict, Any, List

class PixelBoostAnalyzer:
    """
    Pixel Boost: Analyzes browser screenshots for visual phishing.
    Detects fake login forms, brand impersonation, suspicious layouts.
    No GPU needed — pure classical CV for hackathon demo.
    """

    def analyze(self, image_base64: str) -> Dict[str, Any]:
        try:
            image = self._decode(image_base64)
            login = self._detect_login_form(image)
            brand = self._detect_brand_impersonation(image)
            color = self._suspicious_color_score(image)
            density = self._text_density(image)
            score = self._compute_score(login, brand, color, density)
            return {
                'login_form_detected': login,
                'fake_brand_logo': brand,
                'suspicious_color_scheme': color,
                'text_density_score': density,
                'phishing_score': score,
            }
        except Exception as e:
            return {'error': str(e), 'phishing_score': 0.0}

    def _decode(self, b64: str) -> Image.Image:
        return Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGB')

    def _detect_login_form(self, img: Image.Image) -> bool:
        arr = np.array(img.resize((200, 200)))
        gray = np.mean(arr, axis=2)
        center = np.mean(gray[60:140, 60:140])
        border = np.mean(np.concatenate([gray[:20,:], gray[-20:,:], gray[:,:20], gray[:,-20:]], axis=None))
        return bool(center > border + 40)

    def _detect_brand_impersonation(self, img: Image.Image) -> bool:
        arr = np.array(img.resize((50, 50))).reshape(-1, 3)
        dominant = arr.mean(axis=0)
        is_paypal_blue = dominant[2] > 150 and dominant[0] < 50
        is_google_red = dominant[0] > 200 and dominant[1] < 50
        return bool(is_paypal_blue or is_google_red)

    def _suspicious_color_score(self, img: Image.Image) -> float:
        arr = np.array(img.resize((100, 100))).reshape(-1, 3)
        return float(max(0, 1 - np.var(arr, axis=0).mean() / 5000))

    def _text_density(self, img: Image.Image) -> float:
        edges = img.convert('L').resize((200, 200)).filter(ImageFilter.FIND_EDGES)
        return float(np.mean(np.array(edges)) / 255)

    def _compute_score(self, login, brand, color, density) -> float:
        score = 0.0
        if login:  score += 0.40
        if brand:  score += 0.30
        score += color * 0.20
        score += density * 0.10
        return min(score, 1.0)

    def get_indicators(self, result: Dict) -> List[str]:
        out = []
        if result.get('login_form_detected'):
            out.append("Login form detected — possible credential harvesting")
        if result.get('fake_brand_logo'):
            out.append("Brand impersonation pattern detected")
        if result.get('suspicious_color_scheme', 0) > 0.6:
            out.append("Suspicious uniform color scheme")
        return out
