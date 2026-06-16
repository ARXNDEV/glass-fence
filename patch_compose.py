import yaml

with open("docker-compose.prod.yaml", "r") as f:
    compose = yaml.safe_load(f)

if "services" not in compose:
    compose["services"] = {}

compose["services"]["prometheus"] = {
    "image": "prom/prometheus:v2.50.0",
    "volumes": [
        "./prometheus.yml:/etc/prometheus/prometheus.yml:ro",
        "prometheus-data:/prometheus"
    ],
    "networks": ["web"],
    "labels": [
        "traefik.enable=true",
        "traefik.http.routers.prometheus.rule=Host(`metrics.${DOMAIN}`)",
        "traefik.http.routers.prometheus.middlewares=traefik-auth"
    ]
}

compose["services"]["grafana"] = {
    "image": "grafana/grafana:10.3.0",
    "environment": {
        "GF_SECURITY_ADMIN_PASSWORD": "${GRAFANA_PASSWORD:-changeme}"
    },
    "volumes": [
        "grafana-data:/var/lib/grafana",
        "./grafana/dashboards:/etc/grafana/provisioning/dashboards:ro"
    ],
    "networks": ["web"]
}

if "volumes" not in compose:
    compose["volumes"] = {}
compose["volumes"]["prometheus-data"] = None
compose["volumes"]["grafana-data"] = None

with open("docker-compose.prod.yaml", "w") as f:
    yaml.dump(compose, f, sort_keys=False)

print("Updated docker-compose.prod.yaml")
