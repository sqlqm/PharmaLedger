# DSCSA Blockchain Supply Chain Project

A production-scale blockchain implementation for pharmaceutical supply chain traceability, compliant with the Drug Supply Chain Security Act (DSCSA).

## 🎯 Project Overview

This project demonstrates a complete blockchain-based solution for tracking pharmaceutical products through the supply chain from manufacturer to patient. It includes:

- **Synthetic Dataset**: 142,268 realistic pharmaceutical supply chain transactions
- **Blockchain Infrastructure**: SHA-256 hash-based immutable ledger
- **Data Analysis**: Transit time analysis, tampering detection, and ML predictions

## 👥 Team Members

- **Jadallah Salam**: Synthetic Dataset Creation
- **Polls**: Blockchain Infrastructure (Block & Chain Classes)
- **Cherie Qiu**: Data Analysis & Validation

## 📊 Dataset

### Overview
- **Total Transactions**: 142,268
- **Unique Products**: 24,501
- **Supply Chain Participants**: 45
  - 15 Manufacturers (Pfizer, J&J, Merck, etc.)
  - 10 Distributors (McKesson, Cardinal Health, etc.)
  - 20 Pharmacies (CVS, Walgreens, etc.)
  - 10 Hospitals (Mayo Clinic, Johns Hopkins, etc.)
- **Time Period**: 15 months (January 2024 - April 2025)
- **File**: `dscsa_transactions_2024_2025.csv` (22 MB)

### Data Structure
Each transaction includes:
- `barcode_string`: GS1 2D barcode format
- `gtin`: Global Trade Item Number
- `serial`: Unique product serial number
- `exp`: Expiration date
- `lot`: Lot number
- `event_type`: Commissioned, Shipped, Received, Dispensed, Recalled, Expired, Returned
- `actor`: Organization performing the action
- `location`: Physical location
- `timestamp`: ISO 8601 timestamp
- `status`: Current product status

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CSV Dataset                          │
│              (142,268 Transactions)                     │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ↓                       ↓
┌─────────────────┐    ┌──────────────────┐
│  Blockchain     │    │  Data Analysis   │
│  (Polls)        │    │  (Cherie)        │
│                 │    │                  │
│  • Block Class  │    │  • Transit Time  │
│  • Chain Class  │    │  • Tampering     │
│  • Validation   │    │  • Predictions   │
│  • JSON Export  │    │  • Visualization │
└─────────────────┘    └──────────────────┘
```

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Required packages
pip install pandas matplotlib scikit-learn
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dscsa-blockchain.git
cd dscsa-blockchain

# Install dependencies
pip install -r requirements.txt
```

## 📁 Project Structure

```
dscsa-blockchain/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── dscsa_transactions_2024_2025.csv
│
├── blockchain/
│   ├── chain.py              # Block and Chain classes
│   └── project.py            # CLI application
│
├── analysis/
│   ├── transit_time.py       # Transit time analysis
│   ├── tamper_measure.py     # Tampering detection
│   └── predict_transit_time.py  # ML predictions
│
├── outputs/
│   └── (generated files)
│
└── docs/
    ├── DATASET.md            # Dataset documentation
    ├── BLOCKCHAIN.md         # Blockchain documentation
    └── ANALYSIS.md           # Analysis documentation
```

## 💻 Usage

### 1. Blockchain Operations

#### View Dataset
```bash
python blockchain/project.py
```

#### Build Blockchain
```bash
python blockchain/project.py --build-chain
```

#### Export Blockchain to JSON
```bash
python blockchain/project.py --build-chain --chain-output outputs/blockchain.json
```

### 2. Transit Time Analysis

```bash
python analysis/transit_time.py
```

**Outputs:**
- `outputs/top10_transit_time_avg_variability.png` - Visualization
- `outputs/per_unit_transit_times_filtered.csv` - All transit records
- `outputs/avg_transit_time_filtered_routes.csv` - Route averages

### 3. Tampering Detection Test

```bash
# First, generate blockchain JSON
python blockchain/project.py --build-chain --chain-output outputs/json1.json

# Run tampering detection experiments
python analysis/tamper_measure.py
```

**Outputs:**
- `outputs/detection_rate_chart.png` - Detection effectiveness
- `outputs/tampered_run1.json` through `tampered_run10.json` - Tampered chains
- Console output with detection statistics

### 4. Transit Time Prediction

```bash
python analysis/predict_transit_time.py
```

**Outputs:**
- Console predictions for specific routes
- `outputs/per_unit_transit_times_filtered.csv`
- `outputs/avg_transit_time_filtered_routes.csv`

## 🔬 Technical Details

### Blockchain Implementation

**Block Structure:**
```python
@dataclass
class Block:
    index: int              # Position in chain
    timestamp: float        # Unix timestamp
    data: Any              # Transaction payload
    previous_hash: str     # Link to previous block
    nonce: int             # For proof-of-work
    hash: str              # SHA-256 hash
```

**Hash Computation:**
- SHA-256 cryptographic hashing
- JSON serialization with sorted keys
- Ensures deterministic hash generation

**Validation:**
- Verifies each block's hash integrity
- Validates chain linkage (previous_hash matching)
- Detects any tampering attempts

### Data Analysis Features

**Transit Time Analysis:**
- Calculates time between location changes
- Identifies bottlenecks in supply chain
- Statistical analysis (mean, std dev, quartiles)
- Visualization with dual-axis charts

**Tampering Detection:**
- Simulates random tampering (0.01% - 80% rates)
- Validates blockchain integrity
- Measures detection effectiveness
- Experimental methodology with 10 trials

**Machine Learning Predictions:**
- Linear regression on historical data
- Seasonal trend analysis
- Route-specific forecasting
- Predictive analytics for logistics optimization

## 📊 Results

### Transit Time Metrics
- Average transit times per route calculated
- Top 10 most frequent routes identified
- Variability analysis showing outliers and quartiles

### Tampering Detection
- **Detection Rate**: ~100% across all experiments
- **Tamper Rates Tested**: 0.01% to 80%
- **Conclusion**: Blockchain successfully detects all tampering attempts

### Predictions
- Historical mean transit times by route
- Seasonal predictions using linear regression
- Statistical validation of forecasts

## 🎓 Educational Value

This project demonstrates:

**Blockchain Concepts:**
- Cryptographic hashing (SHA-256)
- Chain data structures
- Immutability through hash linking
- Validation algorithms

**Data Science:**
- Large-scale data processing (142K records)
- Time series analysis
- Statistical aggregation
- Data quality filtering

**Machine Learning:**
- Supervised learning (Linear Regression)
- Feature engineering
- Model training and prediction
- Validation techniques

**Software Engineering:**
- Modular architecture
- Object-oriented design
- Command-line interfaces
- Error handling
- Documentation

## 🔒 Security Features

- **Cryptographic Hashing**: SHA-256 for tamper detection
- **Chain Linking**: Blocks cryptographically linked via previous_hash
- **Validation**: Comprehensive integrity checking
- **Immutability**: Any modification breaks the chain

## 📈 Performance

**With 142,268 transactions:**
- CSV Loading: 2-5 seconds
- Blockchain Building: 30-60 seconds
- Validation: 10-20 seconds
- JSON Export: 10-15 seconds
- Analysis: 15-30 seconds per script

**Memory Usage:**
- CSV: ~150 MB
- Blockchain: ~200 MB
- Total: ~500 MB recommended RAM

## 🤝 Contributing

This is an academic project. For questions or suggestions:
1. Open an issue
2. Submit a pull request
3. Contact team members

## 📝 License

This project is created for educational purposes as part of CSE 532 coursework.

## 🙏 Acknowledgments

- **DSCSA Standards**: FDA Drug Supply Chain Security Act
- **GS1 Barcodes**: Global standards for product identification
- **Industry Partners**: Pharmaceutical companies referenced in dataset

## 📧 Contact

- **Jadallah Salam**: Dataset & Integration
- **Polls**: Blockchain Infrastructure
- **Cherie Qiu**: Data Analysis

## 🔗 References

- [FDA DSCSA](https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa)
- [GS1 Standards](https://www.gs1.org/)
- [Blockchain Technology](https://en.wikipedia.org/wiki/Blockchain)

---

**Built with Python 3 • pandas • matplotlib • scikit-learn**

*Last Updated: November 2024*
