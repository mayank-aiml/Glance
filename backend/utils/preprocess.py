import re
import unicodedata

try:  # accurate token counts if tiktoken is installed, else a conservative estimate
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
except Exception:
    _ENC = None


# Negations, modals, comparisons, connectors and direction words (not, no, never,
# can, may, but, because, if, than, from, to, by, ...) are deliberately NOT here:
# removing them changes meaning.
_STOPWORDS = frozenset("""
a an the and or of in on at for with as into onto about so too very
just really also then there here this that these those is are was were be been
being am do does did have has had i me my we our us you your he him his she her
it its they them their what which who whom whose when where how why some any
each other such own same both few many much i'm i'll i've i'd you're you'll
you've we're we'll we've they're they'll they've it's that's there's here's
what's let's he's she's
""".split())

_FILLER = re.compile(
    r"\b(?:um+|uh+|er+|erm|ah+|hmm+|mm+|uh-huh|you know|i mean|basically|"
    r"actually|literally|obviously|honestly|anyway|okay|ok|yeah|yep|alright|"
    r"so yeah)\b",
    re.I,
)
_URL = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
_HTML = re.compile(r"<[^>]+>")
_TIMESTAMP = re.compile(r"[\[(]?\b\d{1,2}:\d{2}(?::\d{2})?\b[\])]?")
_CUE = re.compile(
    r"[\[(](?:music|applause|laughter|laughs|inaudible|silence|crosstalk|"
    r"singing|cheering)[^\])]*[\])]",
    re.I,
)
_CITE = re.compile(r"\[\d+\]")
_BOILER = re.compile(
    r"cookie|privacy policy|terms of (?:service|use)|all rights reserved|"
    r"subscribe|sign up|sign in|log in|newsletter|follow us|share (?:this|on)|"
    r"advertisement|skip to (?:main )?content|read more|click here|copyright|"
    r"©|related (?:posts|articles)|leave a comment",
    re.I,
)
_JUNK = re.compile(r"[^\w\s.,;:?!%$'\-/+&]")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_EDGE = ".,;:?!'\"-"


def preprocess_text(text: str, token_limit: int = 3000):
    """
    Shrink text (YouTube transcripts, web pages, articles) before LLM summarization.

    Removes HTML, URLs, timestamps, [Music]-style cues, boilerplate lines,
    stray symbols, filler words, stopwords, repeated words and duplicate
    sentences. Negations, numbers, names and casing are preserved.

    Returns:
        str        -> cleaned text, if it fits within `token_limit`
        list[str]  -> cleaned text split into chunks of <= `token_limit` tokens
                      (on sentence boundaries where possible), otherwise
    """
    if token_limit <= 0:
        raise ValueError("token_limit must be a positive integer")
    if not text or not text.strip():
        return ""

    def count(s: str) -> int:
        if _ENC:
            return len(_ENC.encode(s, disallowed_special=()))
        return int(len(s) / 3.5) + 1

    # ---- 1. strip noise -------------------------------------------------
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("_", " ")
    for pat in (_HTML, _URL, _CUE, _TIMESTAMP, _CITE):
        text = pat.sub(" ", text)

    # ---- 2. drop short boilerplate lines (menus, cookie banners, ...) ---
    lines = [
        ln for ln in text.splitlines()
        if ln.strip() and not (_BOILER.search(ln) and len(ln.split()) <= 25)
    ]

    # ---- 3. clean sentence by sentence ----------------------------------
    seen, sentences = set(), []
    for line in lines:
        line = _JUNK.sub(" ", line)
        for sent in _SENT_SPLIT.split(line):
            sent = _FILLER.sub(" ", sent).strip()
            if not sent:
                continue
            end = sent[-1] if sent[-1] in ".!?" else ""

            words, prev = [], None
            for w in sent.split():
                core = w.strip(_EDGE).lower()
                if (
                    not re.search(r"\w", w)      # lone punctuation
                    or core in _STOPWORDS
                    or core == prev              # "the the", "I I I"
                ):
                    continue
                words.append(w)
                prev = core

            if not words or (len(words) < 2 and not re.search(r"\d", words[0])):
                continue
            if end and words[-1][-1] not in ".!?":
                words[-1] = words[-1].rstrip(",;:") + end

            cleaned = " ".join(words)
            key = re.sub(r"\W+", " ", cleaned.lower()).strip()
            if key in seen:                      # repeated sentence
                continue
            seen.add(key)
            sentences.append(cleaned)

    cleaned_text = " ".join(sentences)

    # ---- 4. return as-is, or chunk if over the limit --------------------
    if count(cleaned_text) <= token_limit:
        return cleaned_text

    chunks, cur, cur_tok = [], [], 0
    for sent in sentences:
        tok = count(sent) + 1
        if tok > token_limit:                    # one huge "sentence" (e.g. unpunctuated transcript)
            if cur:
                chunks.append(" ".join(cur))
                cur, cur_tok = [], 0
            words = sent.split()
            per_word = tok / len(words)
            step = max(1, int(token_limit / per_word * 0.95))
            chunks.extend(" ".join(words[i:i + step]) for i in range(0, len(words), step))
        elif cur_tok + tok > token_limit:
            chunks.append(" ".join(cur))
            cur, cur_tok = [sent], tok
        else:
            cur.append(sent)
            cur_tok += tok
    if cur:
        chunks.append(" ".join(cur))
    return chunks
