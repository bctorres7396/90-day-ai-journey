 # ─────────────────────────────────────────────────────────────
# day03.py  |  Dataset Manager
# Uses all four collection types in a realistic ML utility
# ─────────────────────────────────────────────────────────────

# ── Raw dataset: list of dicts ───────────────────────────────
# Each sample is a dict. The full dataset is a list of those dicts.
# This is the standard format for ML datasets before you load NumPy.
dataset = [
    {"id":1,  "label":"cat",  "split":"train", "score":0.92, "size":(224,224)},
    {"id":2,  "label":"dog",  "split":"train", "score":0.87, "size":(224,224)},
    {"id":3,  "label":"bird", "split":"train", "score":0.94, "size":(224,224)},
    {"id":4,  "label":"cat",  "split":"train", "score":0.78, "size":(256,256)},
    {"id":5,  "label":"dog",  "split":"val",   "score":0.91, "size":(224,224)},
    {"id":6,  "label":"cat",  "split":"val",   "score":0.85, "size":(224,224)},
    {"id":7,  "label":"fish", "split":"val",   "score":0.76, "size":(256,256)},
    {"id":8,  "label":"bird", "split":"test",  "score":0.95, "size":(224,224)},
    {"id":9,  "label":"dog",  "split":"test",  "score":0.88, "size":(224,224)},
    {"id":10, "label":"cat",  "split":"test",  "score":0.82, "size":(224,224)},
]

# ── Build derived structures ─────────────────────────────────

# 1. Label map: str → int index (dict comprehension)
all_labels   = sorted(set(s["label"] for s in dataset))  # unique + sorted
label_to_idx = {label: i for i, label in enumerate(all_labels)}
idx_to_label = {v: k for k, v in label_to_idx.items()}

# 2. Split buckets: group sample IDs by split (dict of sets)
splits = {"train": set(), "val": set(), "test": set()}
for s in dataset:
    splits[s["split"]].add(s["id"])

# 3. Scores per label: dict of lists
scores_by_label = {label: [] for label in all_labels}
for s in dataset:
    scores_by_label[s["label"]].append(s["score"])

# 4. All image sizes seen: a set of tuples
unique_sizes = {s["size"] for s in dataset}   # set comprehension

# ── Report ───────────────────────────────────────────────────
print("=" * 50)
print("  DATASET MANAGER REPORT")
print("=" * 50)

print(f"\n  Total samples : {len(dataset)}")
print(f"  Classes       : {len(all_labels)} — {all_labels}")
print(f"  Image sizes   : {unique_sizes}")

print("\n  SPLIT BREAKDOWN")
for split_name, ids in splits.items():
    pct = len(ids) / len(dataset) * 100
    print(f"    {split_name:<6s}: {len(ids)} samples ({pct:.0f}%)")

print("\n  LABEL MAP")
for label, idx in label_to_idx.items():
    avg = sum(scores_by_label[label]) / len(scores_by_label[label])
    print(f"    [{idx}] {label:<8s} — {len(scores_by_label[label])} samples, avg score: {avg:.3f}")

print("\n  DATA LEAKAGE CHECK")
train_val_overlap  = splits["train"] & splits["val"]
train_test_overlap = splits["train"] & splits["test"]
val_test_overlap   = splits["val"]   & splits["test"]
leakage = train_val_overlap | train_test_overlap | val_test_overlap
if leakage:
    print(f"    WARNING: Leaking sample IDs: {leakage}")
else:
    print(f"    PASS: No overlap between splits.")

print("\n  QUALITY FLAGS")
low_score = [s for s in dataset if s["score"] < 0.80]
non_std   = [s for s in dataset if s["size"] != (224, 224)]
print(f"    Low confidence samples (<0.80) : {len(low_score)}")
for s in low_score:
    print(f"      id={s['id']} label={s['label']} score={s['score']:.2f}")
print(f"    Non-standard size samples     : {len(non_std)}")
for s in non_std:
    print(f"      id={s['id']} label={s['label']} size={s['size']}")
print("\n" + "=" * 50)
