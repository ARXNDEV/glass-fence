import yaml

with open("docker-compose.prod.yaml", "r") as f:
    compose = yaml.safe_load(f)

grafana_volumes = compose["services"]["grafana"]["volumes"]
if "./grafana/datasources:/etc/grafana/provisioning/datasources:ro" not in grafana_volumes:
    grafana_volumes.append("./grafana/datasources:/etc/grafana/provisioning/datasources:ro")

with open("docker-compose.prod.yaml", "w") as f:
    yaml.dump(compose, f, sort_keys=False)

print("Added datasources volume to compose")
