import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "dscsa_transactions_2024_2025.csv" 

df = pd.read_csv(CSV_FILE)
df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by=['barcode_string', 'timestamp_dt']).reset_index(drop=True)


# Remove invalid serialization
dup_serials = (
    df.groupby("serial")["gtin"]
      .nunique()
      .reset_index()
)
invalid_serials = dup_serials[dup_serials["gtin"] > 1]["serial"].tolist()
print(f"Invalid reused serials removed: {len(invalid_serials)}")
df = df[~df["serial"].isin(invalid_serials)].copy()

# Keep only continuous routes
def is_continuous_route(location_list):
    """ Return False if route jumps BACK to a previous location """
    visited = set()
    last_loc = None
    
    for loc in location_list:
        if last_loc is not None and loc != last_loc:
            if loc in visited:
                # This means the route returned to a past location → invalid
                return False
        visited.add(loc)
        last_loc = loc
    return True

valid_barcodes = []

for barcode, group in df.groupby("barcode_string"):
    loc_seq = list(group["location"])
    if is_continuous_route(loc_seq):
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


# Compute average per route
transit_df["route"] = transit_df["from_location"] + " → " + transit_df["to_location"]

avg_transit = (
    transit_df.groupby("route")["transit_time_hours"]
    .mean()
    .sort_values()
)


# Visualization: Top 10 most frequent routes with avg transit time and variability
top_routes = transit_df['route'].value_counts().head(10).index.tolist()
top_transit_df = transit_df[transit_df['route'].isin(top_routes)]
route_order = transit_df['route'].value_counts().head(10).index
avg_transit_top = top_transit_df.groupby('route')['transit_time_hours'].mean().reindex(route_order)
box_data = [top_transit_df[top_transit_df['route'] == route]['transit_time_hours'].values for route in route_order]

fig, ax1 = plt.subplots(figsize=(12,6))
# Bar chart for average transit time
bars = ax1.bar(avg_transit_top.index, avg_transit_top.values, color='skyblue', alpha=0.7, label='Average Time')
ax1.set_ylabel('Average Transit Time (hours)')
ax1.set_xlabel('Route')
ax1.set_xticklabels(avg_transit_top.index, rotation=45, ha='right')
margin = 0.02 * (avg_transit_top.max() - avg_transit_top.min())
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height + margin, f'{height:.1f}', ha='center', va='bottom')

# Box plot for variability
ax2 = ax1.twinx()
ax2.boxplot(box_data, positions=range(len(route_order)), widths=0.5,
            patch_artist=True,
            boxprops=dict(facecolor='lightgreen', alpha=0.5),
            medianprops=dict(color='red'),
            showfliers=False)
ax2.set_ylabel('Transit Time Variability (hours)')

plt.title("Top 10 Most Frequent Routes: Average Transit Time & Variability")
plt.tight_layout()
plt.savefig("top10_transit_time_avg_variability.png", dpi=200)
plt.show()


transit_df.to_csv("per_unit_transit_times_filtered.csv", index=False)
avg_transit.to_csv("avg_transit_time_filtered_routes.csv")
print("\nSaved:")
print(" per_unit_transit_times_filtered.csv")
print(" avg_transit_time_filtered_routes.csv")
print(" transit_time_filtered_routes.png")
