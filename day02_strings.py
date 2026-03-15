 # ─────────────────────────────────────────────────────────────
# day02_strings.py  |  String Manipulation Drills
# Assignment 2 — Day 2 of the 90-Day AI & Python Masterclass
# ─────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════
# FUNCTION 1 — clean_label(text)
# ═══════════════════════════════════════════════════════════════
# Purpose: normalize messy human-typed class labels into the
# clean, consistent format used inside ML datasets and code.
# Real use: dataset builders, annotation pipelines, label maps.
#
# Steps (in order):
#   1. strip()        — remove leading/trailing whitespace
#   2. lower()        — normalize case so "Cat" == "cat"
#   3. replace spaces — spaces become underscores
#   4. filter chars   — keep only [a-z], [0-9], and [_]
# ─────────────────────────────────────────────────────────────

def clean_label(text):
    """
    Normalize a raw class label into a clean ML-safe identifier.

    Args:
        text (str): Raw label string, possibly messy.

    Returns:
        str: Cleaned label — lowercase, underscored, alphanumeric only.

    Examples:
        "  Cat  "           -> "cat"
        "  Golden Retriever " -> "golden_retriever"
        "  HOT-DOG!!  "     -> "hot_dog"
    """
    # Step 1: strip leading/trailing whitespace
    text = text.strip()

    # Step 2: lowercase everything
    text = text.lower()

    # Step 3: replace spaces with underscores
    text = text.replace(" ", "_")

    # Step 4: keep only alphanumeric characters and underscores
    # We build a new string character by character using a comprehension,
    # keeping a char only if it is a letter, digit, or underscore.
    text = "".join(ch for ch in text if ch.isalnum() or ch == "_")

    return text


# ── Tests for clean_label ─────────────────────────────────────
print("=" * 55)
print("  FUNCTION 1: clean_label()")
print("=" * 55)

test_labels = [
    "  Cat  ",
    "  Golden Retriever  ",
    "  HOT-DOG!!  ",
    "   great_white SHARK   ",
    "!!##@@",           # edge: nothing alphanumeric left
    "",                 # edge: empty string
    "  123 Data Points  ",
    "BERT_large-uncased (v2)  ",
]

for raw in test_labels:
    result = clean_label(raw)
    print(f"  input : {repr(raw)}")
    print(f"  output: {repr(result)}")
    print()


# ═══════════════════════════════════════════════════════════════
# FUNCTION 2 — parse_filename(filepath)
# ═══════════════════════════════════════════════════════════════
# Purpose: extract structured metadata from a dataset filepath.
# Real use: the first step of almost every computer vision
# pipeline — reading a folder of images and extracting labels
# and split info from the path and filename automatically.
#
# Expected input:  "datasets/images/train/cat_042.jpg"
# Expected output: {
#     "directory": "datasets/images/train",
#     "filename":  "cat_042.jpg",
#     "label":     "cat",
#     "index":     42,
#     "extension": ".jpg"
# }
#
# Assumptions (standard dataset naming convention):
#   - Filename format: <label>_<index>.<extension>
#   - Directory is everything before the last "/"
#   - Index is always numeric (after the underscore, before dot)
# ─────────────────────────────────────────────────────────────

def parse_filename(filepath):
    """
    Parse a dataset filepath into its structural components.

    Args:
        filepath (str): Full path string, e.g. "datasets/images/train/cat_042.jpg"

    Returns:
        dict with keys: directory, filename, label, index (int), extension

    Raises:
        ValueError: If the filename does not match expected <label>_<index>.<ext> format.
    """
    # ── Step 1: split directory from filename ─────────────────
    # rsplit splits from the RIGHT, limit of 1 split = safe even
    # if the directory path itself contains slashes (it always does)
    parts = filepath.rsplit("/", 1)

    if len(parts) == 2:
        directory = parts[0]
        filename  = parts[1]
    else:
        # No slash at all — filepath IS the filename, no directory
        directory = ""
        filename  = parts[0]

    # ── Step 2: split extension from the rest of the filename ─
    # rsplit on "." from the right, limit 1 — handles names like
    # "my.model.v2.pt" correctly (extension = ".pt")
    name_parts = filename.rsplit(".", 1)

    if len(name_parts) != 2:
        raise ValueError(f"Cannot find extension in filename: {repr(filename)}")

    name_stem = name_parts[0]   # "cat_042"
    extension = "." + name_parts[1]  # ".jpg"

    # ── Step 3: split label and index on the LAST underscore ──
    # rsplit from the right — handles multi-word labels like
    # "golden_retriever_007" correctly (label="golden_retriever", index=7)
    stem_parts = name_stem.rsplit("_", 1)

    if len(stem_parts) != 2 or not stem_parts[1].isdigit():
        raise ValueError(
            f"Filename stem {repr(name_stem)} does not match expected "
            f"<label>_<index> format (e.g. 'cat_042')."
        )

    label = stem_parts[0]           # "cat"
    index = int(stem_parts[1])      # 42  (string "042" → int 42)

    return {
        "directory": directory,
        "filename":  filename,
        "label":     label,
        "index":     index,
        "extension": extension,
    }


# ── Tests for parse_filename ──────────────────────────────────
print("=" * 55)
print("  FUNCTION 2: parse_filename()")
print("=" * 55)

test_paths = [
    "datasets/images/train/cat_042.jpg",
    "datasets/images/val/dog_007.png",
    "data/golden_retriever_128.jpeg",   # multi-word label
    "hot_dog_001.jpg",                  # no directory
    "raw/scans/chest_xray_003.dcm",     # medical imaging extension
]

for path in test_paths:
    print(f"  input : {repr(path)}")
    try:
        result = parse_filename(path)
        for key, val in result.items():
            print(f"    {key:<12}: {repr(val)}")
    except ValueError as e:
        print(f"    ERROR: {e}")
    print()

# Edge case: bad format
print("  Edge case — bad filename format:")
try:
    parse_filename("datasets/images/nolabel.jpg")
except ValueError as e:
    print(f"    Caught expected error: {e}")
print()


# ═══════════════════════════════════════════════════════════════
# FUNCTION 3 — truncate(text, max_chars, suffix="...")
# ═══════════════════════════════════════════════════════════════
# Purpose: shorten a string to a maximum total length while
# appending a suffix so the reader knows it was cut.
#
# Real use: LLM context window management — when you feed text
# into a model with a token limit, you must truncate cleanly
# rather than hard-cutting mid-word. This also appears in UI
# work (preview text in cards, notification bodies, etc.).
#
# Rules:
#   - If len(text) <= max_chars: return text unchanged
#   - Otherwise: return text[:max_chars - len(suffix)] + suffix
#   - If max_chars < len(suffix): raise ValueError — impossible
#   - Truncate at a word boundary if possible (no mid-word cuts)
# ─────────────────────────────────────────────────────────────

def truncate(text, max_chars, suffix="..."):
    """
    Shorten text to max_chars total length, appending suffix if cut.

    Truncates at a word boundary where possible — never cuts mid-word.
    Total length of the result is always <= max_chars.

    Args:
        text      (str): The input string to potentially shorten.
        max_chars (int): Maximum total character count of the result.
        suffix    (str): String appended when truncation occurs. Default "..."

    Returns:
        str: Original text if short enough, otherwise truncated + suffix.

    Raises:
        ValueError: If max_chars is shorter than the suffix itself.
    """
    if max_chars < len(suffix):
        raise ValueError(
            f"max_chars ({max_chars}) must be >= len(suffix) ({len(suffix)}). "
            f"Cannot fit suffix {repr(suffix)} in {max_chars} characters."
        )

    # Already fits — return unchanged
    if len(text) <= max_chars:
        return text

    # How many characters of the original text we can keep
    budget = max_chars - len(suffix)

    # Truncate at word boundary: find the last space within budget
    # so we never cut a word in half (e.g. "transf..." not "transformer...")
    cut_point = text.rfind(" ", 0, budget)

    if cut_point == -1:
        # No space found within budget — single long word, hard cut it
        cut_point = budget

    return text[:cut_point] + suffix


# ── Tests for truncate ────────────────────────────────────────
print("=" * 55)
print("  FUNCTION 3: truncate()")
print("=" * 55)

long_text = (
    "The transformer architecture introduced in 'Attention Is All You Need' "
    "revolutionized natural language processing by replacing recurrent networks "
    "with self-attention mechanisms, enabling parallelization and capturing "
    "long-range dependencies more effectively."
)

print(f"  Original ({len(long_text)} chars):")
print(f"  {repr(long_text)}")
print()

test_cases = [
    (100, "..."),       # standard truncation
    (50,  "..."),       # shorter limit
    (20,  "..."),       # tight limit
    (10,  "..."),       # very tight — may hard-cut
    (5,   "…"),         # unicode ellipsis, single char suffix
    (3,   "…"),         # absolute minimum
    (len(long_text), "..."),   # exactly fits — should NOT truncate
    (len(long_text) + 1, "..."),  # longer than text — should NOT truncate
]

for max_c, suf in test_cases:
    result = truncate(long_text, max_c, suf)
    truncated = len(result) < len(long_text)
    print(f"  max={max_c:<4d} suffix={repr(suf)}  ->  ({len(result)} chars, truncated={truncated})")
    print(f"    {repr(result)}")

print()

# Edge: suffix longer than max_chars
print("  Edge case — suffix longer than max_chars:")
try:
    truncate("hello world", max_chars=2, suffix="...")
except ValueError as e:
    print(f"    Caught expected error: {e}")

print()

# ── Real LLM use case demonstration ──────────────────────────
print("=" * 55)
print("  REAL-WORLD USE CASE: LLM prompt fitting")
print("=" * 55)

context_window   = 4096   # tokens (approximated here as chars for demo)
system_prompt    = "You are a helpful AI assistant. Answer concisely.\n\n"
user_prefix      = "User question: "
article          = long_text * 5    # simulate a long article

available_chars  = context_window - len(system_prompt) - len(user_prefix) - 200
fitted_article   = truncate(article, available_chars, suffix=" [truncated]")

print(f"  Context window:   {context_window} chars")
print(f"  System prompt:    {len(system_prompt)} chars")
print(f"  Budget for text:  {available_chars} chars")
print(f"  Raw article:      {len(article)} chars")
print(f"  Fitted article:   {len(fitted_article)} chars")
print(f"  Fits in window:   {len(system_prompt) + len(user_prefix) + len(fitted_article) <= context_window}")