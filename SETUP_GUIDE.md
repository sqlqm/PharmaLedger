# 🚀 GitHub Repository Setup Guide

## Quick Start - Repository Structure

Follow these steps to organize your code for GitHub:

### Step 1: Create Directory Structure

```bash
# Create main project folder
mkdir dscsa-blockchain
cd dscsa-blockchain

# Create subdirectories
mkdir data
mkdir blockchain
mkdir analysis
mkdir outputs
mkdir docs
```

### Step 2: Move Files to Correct Locations

#### Your Data File:
```bash
# Move the CSV to data folder
# From: wherever it currently is
# To: data/dscsa_transactions_2024_2025.csv
```

#### Polls' Code:
```bash
# Move to blockchain folder:
# - chain.py → blockchain/chain.py
# - project.py → blockchain/project.py
```

#### Cherie's Code:
```bash
# Move to analysis folder:
# - transit_time.py → analysis/transit_time.py
# - tamper_measure.py → analysis/tamper_measure.py
# - predict_transit_time.py → analysis/predict_transit_time.py
```

#### Root Files:
```bash
# Add to root directory:
# - README.md
# - requirements.txt
# - .gitignore
```

### Step 3: Update File Paths

You'll need to update the CSV file path in some scripts:

#### In `blockchain/project.py`:
**Change line 11 from:**
```python
CSV_FILE = "dscsa_transactions_2024_2025.csv"
```
**To:**
```python
CSV_FILE = "../data/dscsa_transactions_2024_2025.csv"
```

**Or update line 41:**
```python
parser.add_argument("--path", "-p", default="../data/dscsa_transactions_2024_2025.csv", ...)
```

#### In `analysis/transit_time.py`:
**Change line 4 from:**
```python
CSV_FILE = "dscsa_transactions_2024_2025.csv"
```
**To:**
```python
CSV_FILE = "../data/dscsa_transactions_2024_2025.csv"
```

#### In `analysis/predict_transit_time.py`:
**Change line 5 from:**
```python
CSV_FILE = "dscsa_transactions_2024_2025.csv"
```
**To:**
```python
CSV_FILE = "../data/dscsa_transactions_2024_2025.csv"
```

#### In `analysis/tamper_measure.py`:
**Change line 29 from:**
```python
ORIGINAL = "json1.json"
```
**To:**
```python
ORIGINAL = "../outputs/json1.json"
```

### Step 4: Create outputs/.gitkeep

```bash
# Create empty file to track the outputs folder
touch outputs/.gitkeep
```

### Final Directory Structure

```
dscsa-blockchain/
├── README.md
├── requirements.txt
├── .gitignore
├── SETUP_GUIDE.md (this file)
│
├── data/
│   └── dscsa_transactions_2024_2025.csv
│
├── blockchain/
│   ├── chain.py
│   └── project.py
│
├── analysis/
│   ├── transit_time.py
│   ├── tamper_measure.py
│   └── predict_transit_time.py
│
├── outputs/
│   └── .gitkeep
│
└── docs/
    └── (optional documentation)
```

---

## 🔧 Alternative: Keep Original Paths

If you don't want to change any code, you can use this simpler structure:

```
dscsa-blockchain/
├── README.md
├── requirements.txt
├── .gitignore
├── dscsa_transactions_2024_2025.csv
├── chain.py
├── project.py
├── transit_time.py
├── tamper_measure.py
└── predict_transit_time.py
```

**No code changes needed!** Just put everything in the root folder.

**Pros:**
- No path changes required
- Works immediately
- Simple structure

**Cons:**
- Less organized
- Harder to navigate
- Not as professional

---

## 📦 Initialize Git Repository

```bash
# Navigate to project folder
cd dscsa-blockchain

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: DSCSA Blockchain Project"

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/dscsa-blockchain.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## ⚠️ Important Notes

### Large Data File
The CSV file is 22 MB. GitHub allows files up to 100 MB, so it's fine to commit.

If you want to use Git LFS (Large File Storage):
```bash
# Install Git LFS
git lfs install

# Track the CSV file
git lfs track "data/*.csv"

# Add .gitattributes
git add .gitattributes

# Commit
git add data/dscsa_transactions_2024_2025.csv
git commit -m "Add dataset via Git LFS"
```

### Output Files
The `.gitignore` file excludes generated outputs (PNG, CSV, JSON) from version control.

To keep outputs tracked, remove these lines from `.gitignore`:
```
outputs/*.png
outputs/*.csv
outputs/*.json
```

---

## ✅ Verification Checklist

Before pushing to GitHub:

- [ ] All files in correct folders
- [ ] Paths updated in Python scripts (if using organized structure)
- [ ] requirements.txt present
- [ ] .gitignore present
- [ ] README.md present
- [ ] Git initialized
- [ ] Files added and committed
- [ ] Remote added
- [ ] Test: Run each script to ensure paths work

---

## 🧪 Test Commands

After setup, test that everything works:

```bash
# Test Polls' blockchain
cd blockchain
python project.py

# Test Cherie's transit analysis
cd ../analysis
python transit_time.py

# Test tampering detection (after generating blockchain)
cd ../blockchain
python project.py --build-chain --chain-output ../outputs/json1.json
cd ../analysis
python tamper_measure.py

# Test predictions
python predict_transit_time.py
```

All should run without errors!

---

## 📝 Recommended Approach

**For professional presentation:** Use the organized structure (data/, blockchain/, analysis/)
**For quick setup:** Use flat structure (all files in root)

Choose based on:
- How much time you have
- Whether you want to impress with organization
- Your comfort level with path adjustments

---

## 🆘 Troubleshooting

**"File not found" errors:**
- Check your current directory: `pwd` (Mac/Linux) or `cd` (Windows)
- Verify file paths in Python scripts match your structure
- Use absolute paths if relative paths cause issues

**Git push issues:**
- Make sure you created the GitHub repository first
- Check remote URL: `git remote -v`
- Use personal access token if password doesn't work

**CSV too large:**
- Verify size: `ls -lh data/dscsa_transactions_2024_2025.csv`
- Should be ~22 MB (within GitHub's 100 MB limit)
- If needed, use Git LFS (instructions above)

---

**Good luck with your GitHub repository!** 🎉
