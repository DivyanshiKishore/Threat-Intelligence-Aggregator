from normalizer.schema import IOC

ioc = IOC(
    type="ipv4",
    value="8.8.8.8",
    source="AleinVault",
    confidence=90,
    tags=["malware", "botnet"]
)

print(ioc)
