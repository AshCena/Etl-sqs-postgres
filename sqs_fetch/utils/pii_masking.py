import hashlib


def mask(value: str) -> str:
    if value is not None:
        return hashlib.sha256(value.encode()).hexdigest()
    else:
        return "0"
