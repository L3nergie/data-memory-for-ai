import re

def tokenize_phrase(phrase: str) -> List[str]:
    # Découpage en tokens en respectant les points de fin de phrase
    tokens = re.split(r'[ !?.;"\']+', phrase)
    tokens = [token for token in tokens if token]
    return tokens
