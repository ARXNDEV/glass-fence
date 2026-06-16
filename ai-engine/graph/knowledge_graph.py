import networkx as nx
from datetime import datetime
from typing import Dict, List, Any
from urllib.parse import urlparse

class ThreatKnowledgeGraph:

    def __init__(self):
        self.G = nx.DiGraph()
        self._seed_known_threats()

    def _seed_known_threats(self):
        known = [
            ('paypal-secure-login.tk', 0.97),
            ('secure-banking-verify.xyz', 0.93),
            ('microsoft-account-update.ga', 0.91),
        ]
        for domain, risk in known:
            self.G.add_node(domain, node_type='domain', risk_score=risk,
                            threat_level='CRITICAL', seeded=True,
                            added=datetime.now().isoformat())

    def add_result(self, url: str, session_id: str, risk_score: float, threat_level: str):
        domain = urlparse(url).hostname or url

        if not self.G.has_node(domain):
            self.G.add_node(domain, node_type='domain', first_seen=datetime.now().isoformat())

        self.G.nodes[domain].update({
            'risk_score': risk_score,
            'threat_level': threat_level,
            'last_seen': datetime.now().isoformat(),
        })

        if not self.G.has_node(session_id):
            self.G.add_node(session_id, node_type='session',
                            created=datetime.now().isoformat())

        self.G.add_edge(session_id, domain,
                        relation='visited',
                        timestamp=datetime.now().isoformat(),
                        risk_score=risk_score)

    def get_domain_info(self, url: str) -> Dict[str, Any]:
        domain = urlparse(url).hostname or url
        if not self.G.has_node(domain):
            return {'known': False, 'risk_score': 0.0}
        return {'known': True, **dict(self.G.nodes[domain])}

    def get_session_profile(self, session_id: str) -> Dict[str, Any]:
        if not self.G.has_node(session_id):
            return {'total_urls': 0, 'avg_risk': 0.0, 'max_risk': 0.0, 'threats_found': 0}
        edges = list(self.G.out_edges(session_id, data=True))
        if not edges:
            return {'total_urls': 0, 'avg_risk': 0.0, 'max_risk': 0.0, 'threats_found': 0}
        risks = [e[2].get('risk_score', 0) for e in edges]
        return {
            'total_urls': len(edges),
            'avg_risk': round(sum(risks) / len(risks), 3),
            'max_risk': round(max(risks), 3),
            'threats_found': sum(1 for r in risks if r > 0.5),
        }

    def export_json(self) -> Dict:
        nodes = [{'id': n, **self.G.nodes[n]} for n in self.G.nodes()]
        edges = [{'source': u, 'target': v, **d} for u, v, d in self.G.edges(data=True)]
        return {'nodes': nodes, 'edges': edges}

graph = ThreatKnowledgeGraph()
