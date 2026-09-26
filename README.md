# Automated Bias & Fairness Evaluation Pipeline for Credit Decision Models

An enterprise-grade, deployment-ready automated fairness audit system for credit decisioning models built for **Lloyds Banking Group**.

## Features & Navigation

- **Setup & Upload**: Type in Model Name, upload predictions dataset (CSV/Excel) or click *Load Benchmark Credit Data*, map ground truth (`y_true`), predictions (`y_pred`), continuous probabilities (`y_prob`), select protected attributes (`Age`, `Gender`, `Marital_Status`, `Employment_Type`, etc.), and set risk tier thresholds (*Strict Regulatory*, *Moderate Banking*, *Lenient*).
- **Dashboard**: Standard model performance metrics (Accuracy, Precision, Recall, F1, ROC-AUC, Specificity), 2x2 visual Confusion Matrix, and the **Fairness vs. Accuracy Trade-Off Evaluator** chart across decision probability thresholds.
- **Fairness Metrics**: Multi-metric **Fair-Compass Radar Chart** and single feature protected variable bias analysis (e.g. Male vs Female, Age brackets) with Disparate Impact Ratio (80% rule), Demographic Parity, Equalized Odds, Equal Opportunity, and compliance status tags (**PASS**, **FLAG**, **HIGH BIAS**).
- **Subgroup Analysis**: Subgroup level fairness metrics across single attributes and combined intersectional groups (e.g., `Gender: Female & Age: <30`) with population percentage, selection rates, disparity ratios, and risk badges.
- **Report**: Downloadable executive governance audit report in **PDF**, **HTML**, and **JSON** formats with Pass/Fail indicators.

---

## Deployment & Execution Options

### Option A: Direct Python & Node Local Launch
```bash
# 1. Install backend requirements
cd backend
pip install -r requirements.txt

# 2. Install frontend packages
cd ../frontend
npm install

# 3. Launch both services
cd ..
python run_app.py
```
- Frontend UI: `http://localhost:3000`
- Backend API Docs: `http://localhost:8000/docs`

### Option B: Docker & Docker Compose
```bash
docker-compose up --build
```
- Web Application: `http://localhost:3000`
