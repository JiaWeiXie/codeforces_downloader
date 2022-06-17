def normalization_text(txt: str) -> str:
    contexts = []
    for line in txt.splitlines():
        s = line.strip()
        if s:
            contexts.append(s)
    return "\n".join(contexts)
