# 🚀 Quick Reference Guide

## File Structure

```
dscsa-blockchain/
├── README.md                          # Main documentation
├── SETUP_GUIDE.md                    # Setup instructions
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── data/
│   └── dscsa_transactions_2024_2025.csv    # Your dataset (22 MB)
│
├── blockchain/                       # Polls' blockchain code
│   ├── chain.py                      # Block and Chain classes
│   └── project.py                    # CLI application
│
├── analysis/                         # Cherie's analysis code
│   ├── transit_time.py               # Transit time analysis
│   ├── tamper_measure.py             # Tampering detection
│   └── predict_transit_time.py       # ML predictions
│
└── outputs/                          # Generated files
    └── .gitkeep
```

## Running the Code

### From blockchain/ directory:
```bash
cd blockchain

# View dataset
python project.py

# Build blockchain
python project.py --build-chain

# Export blockchain to JSON
python project.py --build-chain --chain-output ../outputs/blockchain.json
```

### From analysis/ directory:
```bash
cd analysis

# Transit time analysis
python transit_time.py

# Tampering detection (requires blockchain JSON first)
python tamper_measure.py

# Transit predictions
python predict_transit_time.py
```

## What Was Changed

**Minimal changes - only file paths updated:**

1. **blockchain/project.py**: CSV path updated to `../data/`
2. **analysis/transit_time.py**: CSV path and output paths updated
3. **analysis/predict_transit_time.py**: CSV path and output paths updated
4. **analysis/tamper_measure.py**: JSON input and output paths updated

**No logic or functionality changes!**

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Test blockchain
cd blockchain && python project.py

# Test analysis
cd analysis && python transit_time.py

# Generate blockchain JSON for tampering test
cd blockchain
python project.py --build-chain --chain-output ../outputs/json1.json
cd ../analysis
python tamper_measure.py
```

## Expected Outputs

### Transit Time Analysis:
- `outputs/top10_transit_time_avg_variability.png`
- `outputs/per_unit_transit_times_filtered.csv`
- `outputs/avg_transit_time_filtered_routes.csv`

### Tampering Detection:
- `outputs/detection_rate_chart.png`
- `outputs/tampered_run1.json` through `tampered_run10.json`

### Predictions:
- Console output with predictions
- `outputs/per_unit_transit_times_filtered.csv`
- `outputs/avg_transit_time_filtered_routes.csv`

## Troubleshooting

**Import errors?**
```bash
pip install pandas matplotlib scikit-learn
```

**File not found?**
- Make sure you're in the correct directory
- Check that CSV is in `data/` folder
- Run commands from `blockchain/` or `analysis/` directories

**Still having issues?**
- Read SETUP_GUIDE.md for detailed instructions
- Check README.md for comprehensive documentation
