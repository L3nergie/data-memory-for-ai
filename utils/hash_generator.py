import hashlib

def generate_hash(word: str) -> str:
    key = str(len(word))
    return hashlib.sha256((word + key).encode()).hexdigest()
