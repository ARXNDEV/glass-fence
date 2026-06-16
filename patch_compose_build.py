import yaml

with open("docker-compose.prod.yaml", "r") as f:
    compose = yaml.safe_load(f)

if "ai-engine" in compose.get("services", {}):
    compose["services"]["ai-engine"]["build"] = "./ai-engine"

# Also glass-fence needs build context if it's there
if "glass-fence" in compose.get("services", {}):
    compose["services"]["glass-fence"]["build"] = "."

with open("docker-compose.prod.yaml", "w") as f:
    yaml.dump(compose, f, sort_keys=False)

print("Added build context to compose")
