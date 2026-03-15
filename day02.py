 # ─────────────────────────────────────────────────────────────
# day02.py  |  AI Model Performance Analyzer
# Covers: strings, numbers, operators, type conversion, booleans
# ─────────────────────────────────────────────────────────────
import math

# ── SECTION 1: Collect model information from the user ────────
print("=" * 55)
print("   AI MODEL PERFORMANCE ANALYZER")
print("=" * 55)

model_name   = input("Model name: ").strip()
architecture = input("Architecture (e.g. CNN, Transformer): ").strip().title()

# Safe float conversion — handles bad input gracefully
def get_float(prompt, low=0.0, high=1.0):
    """Ask for a float in [low, high], retry until valid."""
    while True:
        try:
            val = float(input(prompt))
            if low <= val <= high:
                return val
            print(f"  Please enter a value between {low} and {high}.")
        except ValueError:
            print("  Invalid input — please enter a number.")

train_acc = get_float("Training accuracy   (0.0-1.0): ")
val_acc   = get_float("Validation accuracy (0.0-1.0): ")
test_acc  = get_float("Test accuracy       (0.0-1.0): ")
val_loss  = get_float("Validation loss     (0.0-10.0): ", low=0.0, high=10.0)

epochs    = int(get_float("Epochs trained (1-10000): ", low=1, high=10000))
params_m  = float(input("Parameters (millions, e.g. 7.0 for 7M): "))
latency   = float(input("Inference latency (milliseconds): "))

# ── SECTION 2: Compute derived metrics ────────────────────────
overfit_gap   = train_acc - val_acc
train_val_gap = abs(train_acc - val_acc)
val_test_gap  = abs(val_acc - test_acc)
params_b      = params_m * 1_000_000

# ── SECTION 3: Boolean flags for each quality criterion ───────
acc_strong    = val_acc >= 0.90
loss_low      = val_loss < 0.15
no_overfit    = train_val_gap < 0.05
generalizes   = val_test_gap < 0.03
fast_enough   = latency < 100
well_trained  = epochs >= 20
params_ok     = params_m < 100                          # CRITERION 7: under 100M params

deploy_ready  = all([acc_strong, loss_low, no_overfit, generalizes, fast_enough, well_trained, params_ok])
criteria_met  = sum([acc_strong, loss_low, no_overfit, generalizes, fast_enough, well_trained, params_ok])

# ── SECTION 4: Grade the model ────────────────────────────────
if val_acc >= 0.97:   grade = "S   — Elite. Ship it yesterday."
elif val_acc >= 0.93: grade = "A   — Excellent. Production ready."
elif val_acc >= 0.88: grade = "B   — Strong. Minor tuning needed."
elif val_acc >= 0.80: grade = "C   — Decent. Investigate errors."
elif val_acc >= 0.70: grade = "D   — Weak. Rethink architecture."
else:                 grade = "F   — Start over."

# ── SECTION 5: Overfit diagnosis ──────────────────────────────
if overfit_gap >= 0.10:   overfit_status = "SEVERE overfitting — add dropout/regularization"
elif overfit_gap >= 0.05: overfit_status = "Mild overfitting — monitor closely"
elif overfit_gap < 0:     overfit_status = "Underfitting — model needs more capacity or epochs"
else:                     overfit_status = "Healthy — train/val gap is acceptable"

# ── SECTION 6: Print the full report ──────────────────────────
print()
print("=" * 55)
print(f"  REPORT: {model_name.upper()}")
print(f"  Architecture: {architecture}")
print("=" * 55)
print()
print("  ACCURACY")
print(f"    Train:      {train_acc:.1%}")
print(f"    Validation: {val_acc:.1%}")
print(f"    Test:       {test_acc:.1%}")
print(f"    Grade:      {grade}")
print()
print("  LOSS & EFFICIENCY")
print(f"    Val Loss:   {val_loss:.4f}")
print(f"    Latency:    {latency:.1f} ms")
print(f"    Parameters: {params_m:.1f}M ({params_b:,.0f})")
print(f"    Epochs:     {epochs:,}")
print()
print("  DIAGNOSTICS")
print(f"    Overfit gap:     {overfit_gap:+.3f}  ({overfit_status})")
print(f"    Val/Test gap:    {val_test_gap:.3f}")
print(f"    Criteria met:    {criteria_met}/7")
print()
print("  CHECKLIST")
print(f"    [{'✓' if acc_strong   else '✗'}] Validation accuracy >= 90%")
print(f"    [{'✓' if loss_low     else '✗'}] Validation loss < 0.15")
print(f"    [{'✓' if no_overfit   else '✗'}] Overfit gap < 5%")
print(f"    [{'✓' if generalizes  else '✗'}] Val/Test gap < 3%")
print(f"    [{'✓' if fast_enough  else '✗'}] Latency < 100ms")
print(f"    [{'✓' if well_trained else '✗'}] Trained for >= 20 epochs")
print(f"    [{'✓' if params_ok    else '✗'}] Parameters < 100M")
print()

# ── SECTION 7: Recommendations ────────────────────────────────
recommendations = []

if not acc_strong:
    gap = 0.90 - val_acc
    recommendations.append(
        f"ACCURACY ({val_acc:.1%} — need 90%): You are {gap:.1%} short. Try a deeper "
        f"architecture, more training data, or longer training with a lower learning rate."
    )

if not loss_low:
    recommendations.append(
        f"LOSS ({val_loss:.4f} — need < 0.15): Loss is too high. Apply label smoothing, "
        f"tune your learning rate schedule, or add weight decay (L2 regularization)."
    )

if not no_overfit:
    recommendations.append(
        f"OVERFITTING (gap = {train_val_gap:.1%} — need < 5%): Model memorized training data. "
        f"Add dropout (start at 0.2-0.5), increase L2 weight decay, or collect more training data."
    )

if not generalizes:
    recommendations.append(
        f"GENERALIZATION (val/test gap = {val_test_gap:.1%} — need < 3%): Model does not transfer "
        f"well to unseen data. Check for data leakage, or apply stronger augmentation during training."
    )

if not fast_enough:
    recommendations.append(
        f"LATENCY ({latency:.0f}ms — need < 100ms): Too slow for production. Try quantization "
        f"(INT8), pruning, knowledge distillation into a smaller model, or switch to ONNX runtime."
    )

if not well_trained:
    recommendations.append(
        f"TRAINING (only {epochs} epochs — need >= 20): Model is undertrained. Run more epochs "
        f"with a learning rate scheduler (cosine annealing or ReduceLROnPlateau)."
    )

if not params_ok:
    recommendations.append(
        f"MODEL SIZE ({params_m:.1f}M params — need < 100M): Model is too large for most "
        f"deployments. Use a smaller backbone, apply structured pruning, or try knowledge distillation."
    )

if recommendations:
    print("  RECOMMENDATIONS")
    for i, rec in enumerate(recommendations, 1):
        # Word-wrap each recommendation at ~50 chars for clean terminal output
        words = rec.split()
        line, lines = "", []
        for word in words:
            if len(line) + len(word) + 1 > 50:
                lines.append(line)
                line = word
            else:
                line = word if not line else line + " " + word
        if line:
            lines.append(line)
        print(f"    {i}. {lines[0]}")
        for l in lines[1:]:
            print(f"       {l}")
        print()
else:
    print("  RECOMMENDATIONS")
    print("    All criteria passed — no changes needed.")
    print()

status_line = "DEPLOY READY" if deploy_ready else "NOT READY — see checklist above"
print(f"  VERDICT: {status_line}")
print("=" * 55)