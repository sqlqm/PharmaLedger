# PharmaLedger — DSCSA Blockchain Supply Chain Simulator

PharmaLedger is a full blockchain-based pharmaceutical traceability system built around a **142,268-transaction synthetic DSCSA dataset**.  
It models real-world drug package movement through a supply chain, enables tamper detection, performs statistical transit-time analysis, and includes machine-learning predictions for route timing.

This project was originally developed as a team assignment and later consolidated, refactored, and maintained into this standalone version.

## 📌 Features

### Blockchain Simulation
- Full block and chain implementation (`chain.py`, `project.py`)  
- Automatic validation, hashing, and event linking  
- DSCSA-style fields (GTIN, serial, lot, exp, events, actors)

### Data Analytics
- Transit time variability analysis  
- Route performance metrics  
- Tamper detection experiments  
- Predictive transit-time ML model (scikit-learn)

### GUI Application
- Desktop GUI for browsing supply chain data  
- Inspect block history and event logs  
- Run analyses from a visual interface

### Outputs
- Multiple CSV reports  
- Visualizations (PNG charts)  
- Tampered chain experiment files  
- Exported blockchain JSON

## 📁 Project Structure

```
PharmaLedger/
├── README.md
├── QUICK_REFERENCE.md
├── SETUP_GUIDE.md
├── requirements.txt
├── .gitignore
│
├── dscsa_transactions_2024_2025.csv        # 142k synthetic DSCSA transactions
│
├── chain.py                                # Block + Chain classes
├── project.py                              # Blockchain builder / CLI entry
├── transit_time.py                         # Transit time analytics
├── tamper_measure.py                       # Tampering detection experiments
├── predict_transit_time.py                 # Transit-time ML prediction
├── pharmaledger_gui.py                     # Desktop GUI application
│
└── outputs/                                # Generated charts + CSVs
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/sqlqm/PharmaLedger.git
cd PharmaLedger
```

### 2. (Recommended) Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 📦 Usage

### 1. Build the Blockchain

```bash
python project.py --build-chain --chain-output outputs/blockchain.json
```

### 2. Run Transit-Time Analysis

```bash
python transit_time.py
```

### 3. Run Tamper Detection Experiments

```bash
python project.py --build-chain --chain-output outputs/json1.json
python tamper_measure.py
```

### 4. Predict Transit Times (ML)

```bash
python predict_transit_time.py
```

### 5. Launch the GUI

```bash
python pharmaledger_gui.py
```

## 📊 Dataset Overview

The dataset simulates DSCSA-compliant serialized pharmaceutical events.

## 🔐 Blockchain Logic Summary

PharmaLedger’s chain implements:

- SHA256 hashing  
- Previous-hash linking  
- Tamper detection  
- Event reconstruction  
- Exportable JSON  
- Multi-run tampering experiments

## 📘 Team & Roles

- **Jadallah, Salam** — Synthetic dataset design, integration, GUI.
- **Duong, Polls** — Blockchain infrastructure.
- **Qiu, Cherie** — Data analysis + validation.

## 🎯 Educational Value

Useful for learning:

- Distributed ledgers  
- Serialization (DSCSA)  
- Supply-chain analytics  
- ML for logistics  
- Tamper detection

## 📄 License

MIT License.

## 🕒 Last Updated

December 2025
