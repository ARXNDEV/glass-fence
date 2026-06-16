import re
import math
import tldextract
from urllib.parse import urlparse
from typing import Dict, Any

class URLFeatureExtractor:

    SUSPICIOUS_KEYWORDS = [
        'login', 'signin', 'verify', 'secure', 'account', 'update',
        'confirm', 'banking', 'paypal', 'amazon', 'microsoft', 'google',
        'apple', 'netflix', 'password', 'credential', 'wallet', 'crypto'
    ]
    SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.click']

    def extract(self, url: str) -> Dict[str, Any]:
        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)
        except Exception:
            return self._empty_features()

        hostname = parsed.hostname or ''
        path = parsed.path or ''
        full_url = url.lower()

        return {
            'url_length': len(url),
            'hostname_length': len(hostname),
            'path_length': len(path),
            'num_dots': url.count('.'),
            'num_hyphens': url.count('-'),
            'num_at_signs': url.count('@'),
            'num_question_marks': url.count('?'),
            'num_equals': url.count('='),
            'num_slashes': url.count('/'),
            'num_digits': sum(c.isdigit() for c in url),
            'digit_ratio': sum(c.isdigit() for c in url) / max(len(url), 1),
            'url_entropy': self._entropy(url),
            'hostname_entropy': self._entropy(hostname),
            'has_ip_address': 1 if re.match(r'\d+\.\d+\.\d+\.\d+', hostname) else 0,
            'has_suspicious_keyword': 1 if any(kw in full_url for kw in self.SUSPICIOUS_KEYWORDS) else 0,
            'suspicious_keyword_count': sum(1 for kw in self.SUSPICIOUS_KEYWORDS if kw in full_url),
            'has_suspicious_tld': 1 if any(full_url.endswith(tld) for tld in self.SUSPICIOUS_TLDS) else 0,
            'has_https': 1 if parsed.scheme == 'https' else 0,
            'subdomain_count': len(extracted.subdomain.split('.')) if extracted.subdomain else 0,
            'has_port': 1 if parsed.port and parsed.port not in [80, 443] else 0,
            'has_hex_encoding': 1 if '%' in url else 0,
            'has_at_in_url': 1 if '@' in url else 0,
            'double_slash_redirect': 1 if '//' in path else 0,
            'prefix_suffix_separator': 1 if '-' in hostname else 0,
            'domain_length': len(extracted.domain) if extracted.domain else 0,
            'tld_length': len(extracted.suffix) if extracted.suffix else 0,
        }

    def _entropy(self, text: str) -> float:
        if not text:
            return 0.0
        freq = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1
        total = len(text)
        return -sum((f/total) * math.log2(f/total) for f in freq.values())

    def _empty_features(self) -> Dict[str, Any]:
        return {k: 0 for k in [
            'url_length','hostname_length','path_length','num_dots','num_hyphens',
            'num_at_signs','num_question_marks','num_equals','num_slashes','num_digits',
            'digit_ratio','url_entropy','hostname_entropy','has_ip_address',
            'has_suspicious_keyword','suspicious_keyword_count','has_suspicious_tld',
            'has_https','subdomain_count','has_port','has_hex_encoding','has_at_in_url',
            'double_slash_redirect','prefix_suffix_separator','domain_length','tld_length'
        ]}

    def to_vector(self, features: Dict[str, Any]) -> list:
        return [features[k] for k in sorted(features.keys())]
