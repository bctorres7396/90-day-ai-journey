 # ─────────────────────────────────────────────────────────────
# day02_stretch.py  |  Training Log Parser
# Assignment 4 (Stretch) — Day 2 of the 90-Day AI & Python Masterclass
# ─────────────────────────────────────────────────────────────
import math
import random

random.seed(42)   # fix the seed so results are reproducible

# ═══════════════════════════════════════════════════════════════
# PART 1 — Simulate 30 epochs of training
# ═══════════════════════════════════════════════════════════════
# Each epoch: multiply current loss by a random factor in [0.80, 0.95]
# This mimics a model that is generally converging but with some
# noise — just like real training curves look.

loss    = 5.0
losses  = []

for epoch in range(1, 31):
    factor = random.uniform(0.80, 0.95)
    loss   = loss * factor
    losses.append(round(loss, 6))

# ═══════════════════════════════════════════════════════════════
# PART 2 — Compute statistics (no NumPy)
# ═══════════════════════════════════════════════════════════════

n            = len(losses)
final_loss   = losses[-1]
best_loss    = min(losses)
worst_loss   = max(losses)
mean_loss    = sum(losses) / n
variance     = sum((x - mean_loss) ** 2 for x in losses) / n
std_loss     = math.sqrt(variance)
best_epoch   = losses.index(best_loss) + 1      # +1 because epochs start at 1
improvement  = losses[0] - losses[-1]            # how much loss dropped overall
pct_drop     = (improvement / losses[0]) * 100

print("=" * 55)
print("  TRAINING LOG PARSER — 30 Epoch Simulation")
print("=" * 55)
print()
print("  STATISTICS")
print(f"    Epochs trained  : {n}")
print(f"    Starting loss   : {losses[0]:.6f}")
print(f"    Final loss      : {final_loss:.6f}")
print(f"    Best loss       : {best_loss:.6f}  (epoch {best_epoch})")
print(f"    Worst loss      : {worst_loss:.6f}  (epoch 1 — always the start)")
print(f"    Mean loss       : {mean_loss:.6f}")
print(f"    Std deviation   : {std_loss:.6f}")
print(f"    Total drop      : {improvement:.6f}  ({pct_drop:.1f}% improvement)")
print()

# ═══════════════════════════════════════════════════════════════
# PART 3 — ASCII training curve
# ═══════════════════════════════════════════════════════════════
# Each bar's length = loss normalised to [0, MAX_WIDTH] characters.
# Normalisation formula:
#   bar_len = round( (loss / max_loss) * MAX_WIDTH )
# We use max_loss (worst_loss) as the ceiling so the worst epoch
# always fills the full bar width, and everything else is relative.

MAX_WIDTH = 30   # maximum bar length in characters
BLOCK     = "█"
HALF      = "▌"   # used for the loss value label colour break

print("  TRAINING CURVE  (each █ ≈ {:.4f} loss)".format(worst_loss / MAX_WIDTH))
print("  " + "-" * 55)

for i, ep_loss in enumerate(losses, start=1):
    # Normalise: bar is proportional to loss vs the maximum loss seen
    bar_len   = round((ep_loss / worst_loss) * MAX_WIDTH)
    bar       = BLOCK * bar_len

    # Pad bar to MAX_WIDTH so the loss numbers align on the right
    bar_padded = bar.ljust(MAX_WIDTH)

    # Mark best epoch with an arrow
    marker = " ◄ BEST" if i == best_epoch else ""

    print(f"  Epoch {i:>2d} │{bar_padded}│ {ep_loss:.4f}{marker}")

print("  " + "-" * 55)

# ── Axis labels ───────────────────────────────────────────────
# Print a mini scale under the bars
zero_label  = "0"
mid_label   = f"{worst_loss / 2:.2f}"
max_label   = f"{worst_loss:.2f}"

# Build the axis line: "0" at left, mid in centre, max at right
axis_inner_width = MAX_WIDTH
mid_pos          = axis_inner_width // 2 - len(mid_label) // 2

axis_line = (
    zero_label
    + " " * (mid_pos - len(zero_label))
    + mid_label
    + " " * (axis_inner_width - mid_pos - len(mid_label) - len(max_label))
    + max_label
)
print(f"          │{axis_line}│")
print()

# ── Bonus: highlight the convergence phases ───────────────────
# Find the epoch where loss first dropped below 50% of starting loss
half_start = losses[0] / 2
half_epoch = next((i + 1 for i, l in enumerate(losses) if l < half_start), None)

# Find the epoch where loss first dropped below 10% of starting loss
tenth_start = losses[0] / 10
tenth_epoch = next((i + 1 for i, l in enumerate(losses) if l < tenth_start), None)

print("  CONVERGENCE MILESTONES")
if half_epoch:
    print(f"    < 50% of start ({half_start:.4f})  : epoch {half_epoch}  (loss = {losses[half_epoch-1]:.6f})")
else:
    print(f"    < 50% of start ({half_start:.4f})  : never reached in 30 epochs")

if tenth_epoch:
    print(f"    < 10% of start ({tenth_start:.4f})  : epoch {tenth_epoch}  (loss = {losses[tenth_epoch-1]:.6f})")
else:
    print(f"    < 10% of start ({tenth_start:.4f})  : never reached in 30 epochs")

print()

# ── Bonus: per-epoch delta table (how much did loss change each step) ─
print("  EPOCH-BY-EPOCH DELTAS  (negative = improving)")
print(f"  {'Epoch':>6}  {'Loss':>10}  {'Delta':>10}  {'% Change':>9}  Trend")
print("  " + "-" * 52)

for i in range(n):
    ep    = i + 1
    l     = losses[i]
    if i == 0:
        delta   = 0.0
        pct_chg = 0.0
        trend   = "—  (start)"
    else:
        delta   = l - losses[i - 1]
        pct_chg = (delta / losses[i - 1]) * 100
        # Show a miniature sparkline trend symbol
        if pct_chg < -15:
            trend = "↓↓  big drop"
        elif pct_chg < -10:
            trend = "↓   good drop"
        else:
            trend = "↘   small drop"

    marker = " ◄ BEST" if ep == best_epoch else ""
    print(f"  {ep:>6}  {l:>10.6f}  {delta:>+10.6f}  {pct_chg:>8.2f}%  {trend}{marker}")

print()
print("=" * 55)
print(f"  Run complete. Final loss: {final_loss:.6f}")
print(f"  Model improved by {pct_drop:.1f}% over 30 epochs.")
print("=" * 55)