import json
import random
import hashlib
import copy
import matplotlib.pyplot as plt

# Helper: compute block hash - Recreate the correct hash of a block
def compute_hash(block):
    block_string = (
        str(block["index"])
        + str(block["timestamp"])
        + json.dumps(block["data"], sort_keys=True)
        + str(block["previous_hash"])
        + str(block["nonce"])
    )
    return hashlib.sha256(block_string.encode()).hexdigest()

# Validate chain: to detect errors
def validate_chain(chain):
    errors = []
    for i, block in enumerate(chain):
        recalculated_hash = compute_hash(block)
        if recalculated_hash != block["hash"]:
            errors.append({"index": block["index"], "error": "block_hash_mismatch"})
    return errors

# simulation
def run_experiments(runs=10):
    ORIGINAL = "json1.json"

    # Load original chain
    with open(ORIGINAL, "r") as f:
        original_chain = json.load(f)

    total_blocks = len(original_chain)
    print(f"Total blocks in chain: {total_blocks}")

    # Store summary results for line chart
    summary_results = []

    for run in range(1, runs + 1):
        # Randomize tamper rate 0.01% to 80%
        tamper_rate = random.uniform(0.0001, 0.8)
        num_to_tamper = max(1, int(total_blocks * tamper_rate))

        # Deep copy chain: create a fresh copy for tampering
        tampered_chain = copy.deepcopy(original_chain)

        # Randomly choose blocks to tamper
        tampered_indexes = random.sample(range(1, total_blocks), num_to_tamper)

        # Tamper blocks
        for idx in tampered_indexes:
            block = tampered_chain[idx]
            if "serial" in block["data"]:
                block["data"]["serial"] = "FAKE_" + block["data"]["serial"]
            # Recompute hash incorrectly to simulate tampering
            block["hash"] = compute_hash(block) + "_BAD"

        # Validate chain to detect tampering
        errors = validate_chain(tampered_chain)

        detected_tampered = {
            e["index"] for e in errors if e["error"] == "block_hash_mismatch" and e["index"] in tampered_indexes
        }

        detection_rate = len(detected_tampered) / len(tampered_indexes) * 100

        print(f"\n=== Running tamper rate {tamper_rate*100:.2f}% ===")
        print(f"Tampered blocks: {len(tampered_indexes)}")
        print(f"Detected tampered: {len(detected_tampered)}")
        print(f"Detection rate: {detection_rate:.2f}%")

        # Save tampered chain JSON
        out_name = f"tampered_run{run}.json"
        with open(out_name, "w") as f_out:
            json.dump(tampered_chain, f_out, indent=2)
        print(f"Saved: {out_name}")

        # Store summary for line chart
        summary_results.append({
            "tamper_fraction": tamper_rate,
            "detection_rate": detection_rate
        })

    # Visualize
    rates = [r["tamper_fraction"]*100 for r in summary_results]
    detection = [r["detection_rate"] for r in summary_results]

    plt.figure(figsize=(8,5))
    plt.plot(rates, detection, marker="o", linewidth=2)
    plt.xlabel("Tamper Rate (%)")
    plt.ylabel("Detection Rate (%)")
    plt.title("Detection Rate vs Tamper Rate (10 Random Experiments)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("detection_rate_chart.png", dpi=200)
    plt.show()
    print("Saved: detection_rate_chart.png")

# --------------------------
if __name__ == "__main__":
    run_experiments()





