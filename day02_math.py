 # ─────────────────────────────────────────────────────────────
# day02_math.py  |  Math & Activation Functions
# Assignment 3 — Day 2 of the 90-Day AI & Python Masterclass
# ─────────────────────────────────────────────────────────────
import math


# ═══════════════════════════════════════════════════════════════
# PART 1 — ACTIVATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════
# Activation functions are applied to a neuron's weighted sum (z)
# before passing the result to the next layer. They introduce
# non-linearity — without them, stacking layers is mathematically
# identical to a single linear transformation, and the network
# cannot learn complex patterns.
#
# Every function below takes a single float (one neuron's output)
# and returns a single float (its activated value).
# Only math.exp and basic operators allowed — no libraries.
# ─────────────────────────────────────────────────────────────

def relu(x):
    """
    Rectified Linear Unit.

    Returns x if positive, 0 otherwise. Dead simple, but the most
    widely used activation in hidden layers. Fast to compute,
    sparse (many neurons output 0), and avoids vanishing gradients
    in the positive region.

    Range: [0, +inf)
    Problem: "Dying ReLU" — neurons with z < 0 always output 0
             and receive zero gradient. They stop learning forever.
    """
    return x if x > 0 else 0.0


def sigmoid(x):
    """
    Logistic sigmoid function.

    Squishes any real number into (0, 1) — interpretable as a
    probability. Used in output layers for binary classification.
    Fell out of favour for hidden layers because it saturates
    (gradients vanish) at large positive or negative values.

    Range: (0, 1)
    Formula: 1 / (1 + e^(-x))
    """
    return 1.0 / (1.0 + math.exp(-x))


def tanh(x):
    """
    Hyperbolic tangent.

    Like sigmoid but centred at 0 — outputs range (-1, 1).
    Zero-centred means gradients are naturally balanced during
    backprop. Still suffers from saturation at extremes but
    outperforms sigmoid in hidden layers.

    Range: (-1, 1)
    Formula: (e^x - e^(-x)) / (e^x + e^(-x))
    """
    e_pos = math.exp(x)
    e_neg = math.exp(-x)
    return (e_pos - e_neg) / (e_pos + e_neg)


def leaky_relu(x, alpha=0.01):
    """
    Leaky ReLU — fixes the Dying ReLU problem.

    Instead of outputting exactly 0 for negative inputs, it allows
    a small gradient to flow (alpha * x). This keeps all neurons
    alive and learning, even when z is consistently negative.

    Range: (-inf, +inf)
    alpha: the slope for negative inputs. Typical values: 0.01–0.2.
           If alpha is learned during training, it becomes PReLU.
    """
    return x if x > 0 else alpha * x


# ── Comparison table ─────────────────────────────────────────
print("=" * 65)
print("  PART 1: Activation Function Comparison")
print("=" * 65)

# Header row
header = f"  {'x':>6}  {'relu':>10}  {'sigmoid':>10}  {'tanh':>10}  {'leaky_relu':>10}"
print(header)
print("  " + "-" * 61)

test_inputs = [-2, -1, 0, 1, 2]

for x in test_inputs:
    r  = relu(x)
    s  = sigmoid(x)
    t  = tanh(x)
    lr = leaky_relu(x)
    print(f"  {x:>6}  {r:>10.6f}  {s:>10.6f}  {t:>10.6f}  {lr:>10.6f}")

print()

# Observations worth knowing
print("  KEY OBSERVATIONS:")
print("  - relu(-2) = 0.0 exactly   — dead zone for negative inputs")
print("  - sigmoid(0) = 0.5         — always, by symmetry")
print("  - tanh(0) = 0.0            — zero-centred, unlike sigmoid")
print("  - leaky_relu(-2) = -0.02   — tiny gradient keeps neuron alive")
print("  - sigmoid and tanh both saturate near +/-2 (gradients shrink)")
print()


# ═══════════════════════════════════════════════════════════════
# PART 2 — compute_loss_stats(losses)
# ═══════════════════════════════════════════════════════════════
# Tracks summary statistics for a list of training losses.
# In a real training loop you call this after each epoch to
# monitor whether your model is converging, stalling, or diverging.
#
# Convergence check: True if ALL of the last 5 losses are
# individually lower than ALL of the first 5 losses — i.e. the
# tail of training is strictly better than the head.
# ─────────────────────────────────────────────────────────────

def compute_loss_stats(losses):
    """
    Compute summary statistics for a training loss history.

    Args:
        losses (list of float): Loss value recorded after each epoch.
                                Must contain at least 1 value.

    Returns:
        dict with keys:
            mean       (float) — average loss across all epochs
            std        (float) — standard deviation (population std)
            min        (float) — best (lowest) loss seen
            max        (float) — worst (highest) loss seen
            range      (float) — max - min
            converging (bool)  — True if last 5 are ALL below first 5

    Raises:
        ValueError: If losses is empty.
    """
    if not losses:
        raise ValueError("losses list cannot be empty.")

    n = len(losses)

    # ── Mean ──────────────────────────────────────────────────
    mean = sum(losses) / n

    # ── Population standard deviation ─────────────────────────
    # std = sqrt( mean of squared deviations from the mean )
    variance = sum((x - mean) ** 2 for x in losses) / n
    std = math.sqrt(variance)

    # ── Min / Max / Range ─────────────────────────────────────
    lo = min(losses)
    hi = max(losses)
    rng = hi - lo

    # ── Convergence check ─────────────────────────────────────
    # Requires at least 10 values to have a meaningful head and tail.
    # If fewer than 10 values: compare what we have, split evenly.
    if n >= 10:
        head = losses[:5]
        tail = losses[-5:]
    elif n >= 2:
        mid  = n // 2
        head = losses[:mid]
        tail = losses[mid:]
    else:
        # Only 1 value — cannot determine convergence
        head = losses
        tail = losses

    # Converging = every value in tail is below every value in head
    # max(tail) < min(head) guarantees ALL tail values beat ALL head values
    converging = max(tail) < min(head)

    return {
        "mean":       round(mean, 6),
        "std":        round(std,  6),
        "min":        round(lo,   6),
        "max":        round(hi,   6),
        "range":      round(rng,  6),
        "converging": converging,
    }


# ── Tests for compute_loss_stats ──────────────────────────────
print("=" * 65)
print("  PART 2: compute_loss_stats()")
print("=" * 65)

# Scenario A: healthy converging training run
losses_converging = [2.41, 1.87, 1.52, 1.23, 0.98, 0.76, 0.61, 0.49, 0.38, 0.29]

# Scenario B: stalled / oscillating — not converging
losses_stalled    = [0.82, 0.79, 0.81, 0.80, 0.83, 0.79, 0.82, 0.80, 0.81, 0.79]

# Scenario C: diverging — getting worse
losses_diverging  = [0.30, 0.35, 0.50, 0.78, 1.20, 1.85, 2.60, 3.40, 4.50, 5.80]

# Scenario D: very short list (edge case)
losses_short      = [1.5, 0.9]

scenarios = [
    ("Converging run  ", losses_converging),
    ("Stalled run     ", losses_stalled),
    ("Diverging run   ", losses_diverging),
    ("Short list (n=2)", losses_short),
]

for label, losses in scenarios:
    stats = compute_loss_stats(losses)
    conv  = "YES — loss is dropping" if stats["converging"] else "NO  — stalled or diverging"
    print(f"  {label}")
    print(f"    losses     : {losses}")
    print(f"    mean       : {stats['mean']:.4f}")
    print(f"    std        : {stats['std']:.4f}")
    print(f"    min / max  : {stats['min']:.4f} / {stats['max']:.4f}")
    print(f"    range      : {stats['range']:.4f}")
    print(f"    converging : {conv}")
    print()


# ═══════════════════════════════════════════════════════════════
# PART 3 — scaled_prob(logit, temperature)
# ═══════════════════════════════════════════════════════════════
# Temperature scaling controls the "confidence" of a model's
# output distribution.
#
# For a SINGLE logit (binary case), dividing by temperature before
# sigmoid achieves the same effect as temperature-scaled softmax:
#
#   temperature > 1  →  logit/T is smaller  →  sigmoid closer to 0.5
#                        output is more uniform (less confident)
#
#   temperature < 1  →  logit/T is larger   →  sigmoid closer to 0 or 1
#                        output is more peaked (more confident)
#
#   temperature = 1  →  standard sigmoid, no change
#
# Real use: calibration, creative vs. deterministic LLM sampling,
# knowledge distillation (soft labels use high temperature).
# ─────────────────────────────────────────────────────────────

def scaled_prob(logit, temperature):
    """
    Temperature-scaled probability for a single logit.

    Applies sigmoid to (logit / temperature). Temperature controls
    how peaked or uniform the output probability is.

    Args:
        logit       (float): Raw model output (pre-activation score).
        temperature (float): Scaling factor. Must be > 0.
                             T > 1 → more uniform.
                             T < 1 → more peaked.
                             T = 1 → standard sigmoid.

    Returns:
        float: Probability in (0, 1).

    Raises:
        ValueError: If temperature <= 0.
    """
    if temperature <= 0:
        raise ValueError(f"temperature must be > 0, got {temperature}.")

    return sigmoid(logit / temperature)


# ── Tests for scaled_prob ─────────────────────────────────────
print("=" * 65)
print("  PART 3: scaled_prob() — Temperature Scaling")
print("=" * 65)

logit = 2.0   # a moderately confident positive prediction

temperatures = [0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]

print(f"  logit = {logit}  (unscaled sigmoid = {sigmoid(logit):.6f})")
print()
print(f"  {'temperature':>12}  {'scaled logit':>14}  {'probability':>12}  interpretation")
print("  " + "-" * 63)

for T in temperatures:
    prob         = scaled_prob(logit, T)
    scaled_logit = logit / T

    if T < 1.0:
        interp = "more peaked   (higher confidence)"
    elif T > 1.0:
        interp = "more uniform  (lower confidence)"
    else:
        interp = "standard sigmoid — no change"

    print(f"  {T:>12.2f}  {scaled_logit:>14.4f}  {prob:>12.6f}  {interp}")

print()

# Sweep across logits at different temperatures to show the full picture
print("  PROBABILITY TABLE: logit vs temperature")
print(f"  {'logit':>7}", end="")
for T in [0.5, 1.0, 2.0, 5.0]:
    print(f"  {'T='+str(T):>10}", end="")
print()
print("  " + "-" * 50)

for x in [-3, -2, -1, 0, 1, 2, 3]:
    print(f"  {x:>7}", end="")
    for T in [0.5, 1.0, 2.0, 5.0]:
        print(f"  {scaled_prob(x, T):>10.4f}", end="")
    print()

print()
print("  READ THE TABLE:")
print("  - Column T=0.5: probs cluster near 0 or 1 — very confident")
print("  - Column T=1.0: standard sigmoid — baseline")
print("  - Column T=2.0: probs drift toward 0.5 — less confident")
print("  - Column T=5.0: probs very close to 0.5 — nearly random")
print()

# Error case
print("  Edge case — temperature <= 0:")
try:
    scaled_prob(1.0, 0)
except ValueError as e:
    print(f"    Caught expected error: {e}")