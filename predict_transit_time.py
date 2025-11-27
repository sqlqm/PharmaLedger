import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

CSV_FILE = "../data/dscsa_transactions_2024_2025.csv"

# Load dataset
df = pd.read_csv(CSV_FILE)
df["timestamp_dt"] = pd.to_datetime(df["timestamp"])
df = df.sort_values(by=["barcode_string", "timestamp_dt"]).reset_index(drop=True)

# Remove invalid serialization
dup_serials = df.groupby("serial")["gtin"].nunique().reset_index()
invalid_serials = dup_serials[dup_serials["gtin"] > 1]["serial"].tolist()
print(f"Invalid reused serials removed: {len(invalid_serials)}")
df = df[~df["serial"].isin(invalid_serials)].copy()

# Keep only continuous routes
def is_continuous_route(location_list):
    visited = set()
    last_loc = None
    for loc in location_list:
        if last_loc is not None and loc != last_loc:
            if loc in visited:
                return False
        visited.add(loc)
        last_loc = loc
    return True

valid_barcodes = []
for barcode, group in df.groupby("barcode_string"):
    if is_continuous_route(list(group["location"])):
        valid_barcodes.append(barcode)

print(f"Barcodes after continuous-route filter: {len(valid_barcodes)}")
df = df[df["barcode_string"].isin(valid_barcodes)].copy()

# Compute transit times (location only and exclude same-location)
transit_records = []

for barcode, group in df.groupby("barcode_string"):
    group = group.reset_index(drop=True)
    prev_location = None
    prev_time = None

    for i, row in group.iterrows():
        loc = row["location"]
        t = row["timestamp_dt"]

        if prev_location is not None and loc != prev_location:
            transit_records.append({
                "barcode": barcode,
                "from_location": prev_location,
                "to_location": loc,
                "from_timestamp": prev_time,
                "to_timestamp": t,
                "transit_time_hours": (t - prev_time).total_seconds() / 3600
            })

        prev_location = loc
        prev_time = t

transit_df = pd.DataFrame(transit_records)
print("\nTransit records generated:", len(transit_df))

if transit_df.empty:
    print("No transit records found after filtering. Try relaxing criteria.")
    raise SystemExit


# Average transit time per route
transit_df["route"] = transit_df["from_location"] + " → " + transit_df["to_location"]
avg_transit = transit_df.groupby("route")["transit_time_hours"].mean()
print("\n=== Average Transit Time per Route (hours) ===")
print(avg_transit)


# Predict transit time for a specific route
FROM_LOC = "Boston, MA"
TO_LOC = "Cincinnati, OH"

route_transits = transit_df[
    (transit_df["from_location"] == FROM_LOC) &
    (transit_df["to_location"] == TO_LOC)
]

num_records = len(route_transits)
print(f"\nNumber of historical reference records from {FROM_LOC} to {TO_LOC}: {num_records}")

if route_transits.empty:
    print(f"\nNo historical transit data from {FROM_LOC} to {TO_LOC}.")
else:
    mean_time = route_transits["transit_time_hours"].mean()
    std_time = route_transits["transit_time_hours"].std()

    print(f"\nHistorical mean transit time: {mean_time:.2f} hours")
    print(f"Standard deviation: {std_time:.2f} hours")

    # Regression by month
    route_transits = route_transits.copy()
    route_transits["month"] = route_transits["from_timestamp"].dt.month

    X = route_transits[["month"]]
    y = route_transits["transit_time_hours"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict for January 2025
    predicted = model.predict(np.array([[1]]))
    print(f"\nPredicted transit time from {FROM_LOC} to {TO_LOC} in January 2025: {predicted[0]:.2f} hours")

transit_df.to_csv("../outputs/per_unit_transit_times_filtered.csv", index=False)
avg_transit.to_csv("../outputs/avg_transit_time_filtered_routes.csv", index=False)

print("\nSaved:")
print(" per_unit_transit_times_filtered.csv")
print(" avg_transit_time_filtered_routes.csv")








