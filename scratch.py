 # Part 1 start
# Single quotes
s1 = 'Hello, world!'

# Double quotes
s2 = "Hello, world!"

# Triple quotes 
s3 = """This is a  
multi-line string.
It preserves every newline."""

# Escape characters
s4 = 'She said \'hello\' to me'
s5 = "Line one\nLine two"
s6 = "Column1\tColumn2"
s7 = "C:\\Users\\name"

print(s5)
print(s6)

#String indexing: starts at 0, negative indexes count from the end
s = "DeepLearning"
#    0123456789...    positive indexes left to right
#   -12-11-10...      negative indexes right to left

print(s[0])      # "D"       - first character
print(s[4])      # "L"       - fifth character (0-indexed!)
print(s[-1])     # "g"       - last character
print(s[-8])     # "L"       - 8th from the end

# Slicing: string[start : stop : step]
# start is inclusive, stop is EXCLUSIVE
print(s[0:4])   # "Deep"     - chars at index 0, 1, 2, 3 (not 4)
print(s[4:12])  # "Learning" - index 4 through 11
print(s[4:])    # "Learning" - from index 4 to the end
print(s[:4])     # "Deep"     - from start to index 3
print(s[::2])   # "DeLann"   _ every second character
print(s[::-1])  # "gninraeLepeD" - reversed! Step of -1 = go backwards

# Real AI use case: extracting file extentions from dataset paths
filepath = "dataset/images/cat_001.jpg"
filename = filepath.split("/")[-1]   # "cat_001.jpg"
extention = filename[-4:]            # ".jpg"
label = filename.split("_")[0]       # "cat"
print(f"File: {filename}, Ext: {extention}, Label: {label}")

text = " Machine Learning is Absolutely Fascinating "

# CLEANING
print(text.strip())         # remove leading AND trailing whitespace
print(text.lstrip())        # remove only leading (left) whitespace
print(text.rstrip())        # remove only trailing (right) whitespace

# CASE CONVERSION
print(text.lower())         # all lowercase - use before comparing strings
print(text.upper())         # all uppercase
print(text.swapcase())      # Title Case Every Word
print(text.swapcase())      # flip every letter's case

# SEARCHING
clean = text.strip()
print("Learning" in clean)   # True - membership test
print(clean.startswith("Machine"))  # True
print(clean.endswith("ing"))        # True
print(clean.find("Learning"))       # 8 -index of first occurrence
print(clean.count("a"))             # 4 - count occurrences of "a"

# REPLACING & SPLITTING
print(clean.replace("Fascinating", "Essential"))  # swap a word
print(clean.replace(" ", "_"))                    # replace spaces with underscores
words = clean.split()          # split on whitespace → list of words
print(words)                   # ["Machine", "Learning", "Is", ...]
print(clean.split("a"))        # split on the letter "a"

# ── JOINING — the reverse of split ──────────────────────────
words = ["deep", "learning", "is", "powerful"]
print(" ".join(words))         # "deep learning is powerful"
print("_".join(words))         # "deep_learning_is_powerful"
print(", ".join(words))        # "deep, learning, is, powerful"

# ── CHECKING TYPE OF CONTENT ─────────────────────────────────
print("12345".isdigit())       # True  — only digits
print("hello".isalpha())       # True  — only letters
print("hello123".isalnum())    # True  — letters and/or digits
print("   ".isspace())         # True  — only whitespace

name = "Ada"
score = 0.9234
epoch = 42

# ── METHOD 1: % formatting — OLD, do not write this ─────────
print("Student: %s, Score: %.2f" % (name, score))

# ── METHOD 2: .format() — less old, still avoid ─────────────
print("Student: {}, Score: {:.2f}".format(name, score))

# ── METHOD 3: f-strings — ALWAYS USE THIS ───────────────────
print(f"Student: {name}, Score: {score:.2f}")

# Why f-strings win: readable, fast, supports any expression
print(f"Score: {score:.2f}")          # 2 decimal places: 0.92
print(f"Score: {score:.1%}")          # as percentage: 92.3%
print(f"Epoch: {epoch:03d}")          # zero-padded integer: 042
print(f"Name:  {name:>10s}")          # right-aligned in 10 chars
print(f"Name:  {name:<10s}")          # left-aligned in 10 chars
print(f"Name:  {name:^10s}")          # center-aligned in 10 chars
print(f"Big:   {1234567:,}")          # thousands separator: 1,234,567

# Expressions and method calls work inside {}
print(f"Upper: {name.upper()}")
print(f"Calc:  {score * 100:.1f}%")
print(f"Days left: {90 - 2}")

# Integers in Python are UNBOUNDED — they can be arbitrarily large
# No overflow error like in C or Java
big = 2 ** 1000    # Python handles this fine. Try it.
print(f"2^1000 has {len(str(big))} digits")

# Integer methods
x = -42
print(abs(x))          # 42  — absolute value
print(bin(255))        # "0b11111111" — binary representation
print(hex(255))        # "0xff"        — hexadecimal
print(oct(255))        # "0o377"       — octal
print((255).bit_length())  # 8         — bits needed to represent 255

# Integer division always returns int, true division always returns float
print(type(10 // 3))   # <class int>
print(type(10 / 3))    # <class float> — even if result is whole
print(type(10 / 2))    # <class float> — 5.0, not 5!

# Modulo — extremely useful in training loops
for step in range(1, 201):
    if step % 50 == 0:         # every 50 steps
        print(f"  Step {step}: save checkpoint")

# Floats have a precision limit — 15-17 significant digits
print(0.1 + 0.2)           # 0.30000000000000004 — NOT 0.3!
print(0.1 + 0.2 == 0.3)    # False  — this is infamous

# Why? Floating point is stored in binary. 0.1 cannot be
# represented exactly in binary, just like 1/3 has no finite decimal.

# The fix: never use == to compare floats. Use a tolerance.
tolerance = 1e-9
print(abs(0.1 + 0.2 - 0.3) < tolerance)   # True — correct comparison

# Or use the math module's isclose()
import math
print(math.isclose(0.1 + 0.2, 0.3))        # True

# Special float values
inf      = float("inf")    # positive infinity
neg_inf  = float("-inf")   # negative infinity
nan      = float("nan")    # Not a Number — result of invalid operations

print(inf > 1_000_000)     # True
print(nan == nan)          # False — NaN is never equal to anything, even itself
print(math.isnan(nan))     # True  — correct way to check for NaN

# In ML: loss becomes nan when training explodes. This is your warning signal.
loss = float("nan")
if math.isnan(loss):
    print("WARNING: Loss is NaN — training has diverged. Reduce learning rate!")

import math

# Constants
print(math.pi)         # 3.141592653589793
print(math.e)          # 2.718281828459045 — Euler's number (base of natural log)
print(math.tau)        # 6.283... = 2*pi
print(math.inf)        # infinity

# Functions you will use constantly in AI
print(math.sqrt(144))       # 12.0   — square root
print(math.log(math.e))     # 1.0    — natural log (ln)
print(math.log2(1024))      # 10.0   — log base 2
print(math.log10(1000))     # 3.0    — log base 10
print(math.exp(1))          # 2.718  — e^x (inverse of log)
print(math.floor(3.7))      # 3      — round DOWN
print(math.ceil(3.2))       # 4      — round UP
print(round(3.14159, 2))    # 3.14   — round to N decimal places
print(math.factorial(5))    # 120    — 5! = 5×4×3×2×1
print(math.pow(2, 10))      # 1024.0 — 2^10 (returns float)
print(abs(-7.3))            # 7.3    — absolute value

# Sigmoid function using math.exp — you will implement this in Week 6
def sigmoid(x):
    """Squishes any number into the range (0, 1)."""
    return 1 / (1 + math.exp(-x))

print(f"sigmoid(-10) = {sigmoid(-10):.6f}")   # very close to 0
print(f"sigmoid(0)   = {sigmoid(0):.6f}")     # exactly 0.5
print(f"sigmoid(10)  = {sigmoid(10):.6f}")    # very close to 1

# Instead of:  x = x + 5
# Write:       x += 5

loss = 2.4
loss -= 0.3       # loss = loss - 0.3  → 2.1
loss *= 0.9       # loss = loss * 0.9  → 1.89
loss /= 2         # loss = loss / 2    → 0.945
loss **= 0.5      # loss = loss ** 0.5 → square root

count = 100
count //= 3       # count = count // 3 → 33
count %= 10       # count = count % 10 → 3
print(loss, count)

# These appear constantly in if-statements and while-loop conditions
accuracy = 0.923
threshold = 0.90

print(accuracy == threshold)   # False  — equality: are they identical?
print(accuracy != threshold)   # True   — inequality: are they different?
print(accuracy > threshold)    # True   — greater than
print(accuracy < threshold)    # False  — less than
print(accuracy >= 0.923)       # True   — greater than or equal
print(accuracy <= 1.0)         # True   — less than or equal

# Chained comparisons — very Pythonic, very readable
print(0.80 <= accuracy < 0.95)  # True — is accuracy in [0.80, 0.95)?
# This is equivalent to: (accuracy >= 0.80) and (accuracy < 0.95)

# Comparing strings — compares alphabetically by Unicode value
print("apple" < "banana")      # True
print("Z" < "a")               # True — uppercase letters come before lowercase in Unicode
print("cat" == "cat")          # True
print("Cat" == "cat")          # False — case sensitive!
print("Cat".lower() == "cat")  # True  — correct way to compare case-insensitively

# and — BOTH conditions must be True
model_ready = True
data_loaded = True
gpu_free    = False

print(model_ready and data_loaded)     # True  — both True
print(model_ready and gpu_free)        # False — one is False

# or — AT LEAST ONE condition must be True
print(gpu_free or model_ready)         # True  — model_ready is True
print(gpu_free or not model_ready)     # False — both effectively False

# not — flips True to False and False to True
print(not gpu_free)                    # True
print(not model_ready)                 # False

# Combining all three — real training gate logic
loss = 0.05
epochs_done = 50
min_epochs = 20

should_stop = (loss < 0.1) and (epochs_done >= min_epochs) and not gpu_free
print(f"Should stop training: {should_stop}")

# Short-circuit evaluation — Python stops early when result is known
# In "A and B": if A is False, B is never evaluated
# In "A or B":  if A is True,  B is never evaluated

# This matters for performance and avoiding errors:
data = []
# Safe: checks len first, only divides if len > 0
if len(data) > 0 and sum(data) / len(data) > 0.5:
    print("Mean above 0.5")
else:
    print("No data or mean not above 0.5")

# "is" — checks if two variables point to the SAME object in memory
# "==" — checks if two variables have the SAME VALUE

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)    # True  — same values
print(a is b)    # False — different objects in memory
print(a is c)    # True  — c points to the same object as a

# The correct way to check for None — always use "is", never "=="
result = None
if result is None:
    print("No result yet")

# "in" — membership: is this value inside this container?
classes = ["cat", "dog", "bird", "fish"]
print("dog" in classes)         # True
print("snake" not in classes)   # True  — "not in" is the complement

# Works on strings too: is this substring in this string?
sentence = "Deep learning is transforming the world"
print("learning" in sentence)   # True
print("math" in sentence)       # False

# scratch.py — Part 4

# ── int() ────────────────────────────────────────────────────
print(int("42"))         # 42    — string digit to int
print(int("  17  "))     # 17    — strips whitespace first
print(int(3.9))          # 3     — truncates, does NOT round
print(int(True))         # 1     — True is 1
print(int(False))        # 0     — False is 0
# print(int("3.14"))     # ValueError! int() cannot parse a float string
print(int(float("3.14")))  # 3   — convert to float first, then int

# ── float() ──────────────────────────────────────────────────
print(float("3.14"))     # 3.14   — string to float
print(float("1e-5"))     # 0.00001 — scientific notation works too
print(float(42))         # 42.0   — int to float
print(float(True))       # 1.0
print(float("inf"))      # inf    — infinity

# ── str() ────────────────────────────────────────────────────
print(str(42))           # "42"    — int to string
print(str(3.14))         # "3.14"  — float to string
print(str(True))         # "True"  — bool to string
print(str([1,2,3]))      # "[1, 2, 3]" — list to string

# ── bool() ───────────────────────────────────────────────────
# Falsy values — convert to False
print(bool(0))           # False   — zero
print(bool(0.0))         # False   — zero float
print(bool(""))          # False   — empty string
print(bool([]))          # False   — empty list
print(bool(None))        # False   — None
# ALL other values convert to True
print(bool(1))           # True
print(bool(-1))          # True    — any non-zero number
print(bool("hello"))     # True    — any non-empty string
print(bool([0]))         # True    — list with content (even if content is 0)

# Python automatically promotes types in arithmetic
# int + float → float (always)
result = 5 + 2.0      # 7.0 — int silently becomes float
print(type(result))   # <class float>

# bool + int → int (True = 1, False = 0)
print(True + True)    # 2
print(True + 5)       # 6
print(False * 100)    # 0

# Practical use: count True values in a list of booleans
predictions = [True, False, True, True, False, True]
correct_count = sum(predictions)   # sum treats True as 1, False as 0
print(f"Correct: {correct_count}/{len(predictions)}")   # 4/6

# Type conversion in real data pipelines
raw_data = ["1.2", "3.4", "0.9", "2.1", "1.7"]   # strings from a CSV
numbers  = [float(x) for x in raw_data]           # convert all to float
average  = sum(numbers) / len(numbers)
print(f"Average: {average:.4f}")

# What happens when conversion fails?
# int("hello") raises ValueError — your program crashes
# The solution: try/except (covered fully on Day 7, preview here)

def safe_int(value, default=0):
    """Convert to int safely. Return default if conversion fails."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(safe_int("42"))        # 42
print(safe_int("hello"))     # 0  — default
print(safe_int("hello", -1)) # -1 — custom default
print(safe_int(None))        # 0  — handles None too

# Real use: reading a messy CSV where some cells are empty or corrupted
raw_scores = ["95", "87", "", "91", "bad_data", "88"]
cleaned    = [safe_int(s, default=0) for s in raw_scores]
print(cleaned)   # [95, 87, 0, 91, 0, 88]

# scratch.py — Part 5

# Booleans ARE integers in Python — True == 1, False == 0
print(True == 1)       # True
print(False == 0)      # True
print(True + True)     # 2

# This lets you count True values elegantly
results = [True, False, True, True, False, True, False, True]
print(f"Correct: {sum(results)}")          # 5
print(f"Accuracy: {sum(results)/len(results):.1%}")  # 62.5%

# Comparison operators return booleans
scores = [0.92, 0.45, 0.88, 0.31, 0.95, 0.67]
passed = [s > 0.5 for s in scores]   # [True, False, True, False, True, True]
print(passed)
print(f"Pass rate: {sum(passed)}/{len(passed)}")

# Real-world model evaluation logic
def should_deploy(val_accuracy, val_loss, test_accuracy, latency_ms):
    """
    Decide if a model is ready for production deployment.
    Returns (bool, str) — decision and reason.
    """
    # All criteria must pass
    acc_ok      = val_accuracy >= 0.90 and test_accuracy >= 0.88
    loss_ok     = val_loss < 0.15
    speed_ok    = latency_ms < 100
    gap_ok      = abs(val_accuracy - test_accuracy) < 0.05  # no overfitting
    
    if acc_ok and loss_ok and speed_ok and gap_ok:
        return True, "All criteria met — deploy!"
    
    # Find what failed
    issues = []
    if not acc_ok:   issues.append(f"accuracy too low ({val_accuracy:.2%})")
    if not loss_ok:  issues.append(f"loss too high ({val_loss:.3f})")
    if not speed_ok: issues.append(f"too slow ({latency_ms}ms)")
    if not gap_ok:   issues.append("overfitting detected")
    return False, "Issues: " + ", ".join(issues)


ok, reason = should_deploy(0.93, 0.12, 0.91, 45)
print(f"Deploy: {ok} — {reason}")

ok, reason = should_deploy(0.85, 0.22, 0.84, 120)
print(f"Deploy: {ok} — {reason}")

