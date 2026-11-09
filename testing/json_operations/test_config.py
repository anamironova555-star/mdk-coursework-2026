from storage import read

c = read("config.json")
assert {"server", "database", "logging"} <= c.keys()
assert type(c["server"]["port"]) is int and 1 <= c["server"]["port"] <= 65535
assert c["logging"]["level"] in ["DEBUG", "INFO", "WARNING", "ERROR"]
assert c["database"]["name"].strip()
print("PASS: config")
