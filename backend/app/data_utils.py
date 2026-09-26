import os
import uuid
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

# In-memory session data storage
DATA_SETS: Dict[str, pd.DataFrame] = {}

BENCHMARK_DATA_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "Working-Dir-New", "data", "credit_data.csv")
)

def store_dataframe(df: pd.DataFrame, filename: str) -> Tuple[str, Dict[str, Any]]:
    """
    Stores DataFrame in session store and extracts metadata with column suggestions.
    """
    file_id = str(uuid.uuid4())
    
    # Ensure missing values handled safely
    df = df.ffill().bfill()
    DATA_SETS[file_id] = df

    columns = list(df.columns)
    num_rows, num_cols = df.shape
    
    # Heuristics for suggesting columns
    suggested_target = None
    suggested_pred = None
    suggested_prob = None
    suggested_protected = []

    for col in columns:
        col_lower = col.lower()
        if 'default' in col_lower or 'ground' in col_lower or 'actual' in col_lower or 'true' in col_lower or col == 'Default_12M':
            suggested_target = col
        elif 'decision' in col_lower or 'pred' in col_lower or 'approval' in col_lower or col == 'Approval_Decision':
            suggested_pred = col
        elif 'prob' in col_lower or 'score' in col_lower and df[col].dtype in ['float64', 'float32']:
            suggested_prob = col
        
        # Check if categorical/protected attribute candidate
        if col in ['Age', 'Marital_Status', 'Education', 'Employment_Type', 'State', 'City_Tier', 'Gender', 'Ethnicity', 'Race']:
            suggested_protected.append(col)
        elif df[col].nunique() >= 2 and df[col].nunique() <= 10 and col not in [suggested_target, suggested_pred]:
            if col not in suggested_protected:
                suggested_protected.append(col)

    sample_data = df.head(5).to_dict(orient='records')
    
    # Clean NaNs in sample_data for JSON safety
    for row in sample_data:
        for k, v in row.items():
            if pd.isna(v):
                row[k] = ""

    return file_id, {
        "file_id": file_id,
        "filename": filename,
        "num_rows": num_rows,
        "num_cols": num_cols,
        "columns": columns,
        "sample_data": sample_data,
        "suggested_target": suggested_target or (columns[0] if len(columns) > 0 else ""),
        "suggested_pred": suggested_pred or (columns[1] if len(columns) > 1 else ""),
        "suggested_prob": suggested_prob,
        "suggested_protected": suggested_protected
    }

def load_benchmark_dataset() -> Tuple[str, Dict[str, Any]]:
    """Loads default benchmark credit dataset."""
    if os.path.exists(BENCHMARK_DATA_PATH):
        df = pd.read_csv(BENCHMARK_DATA_PATH)
    else:
        # Fallback synthetic credit dataframe if file not found
        np.random.seed(42)
        n = 1000
        df = pd.DataFrame({
            "Applicant_ID": [f"APP{i:04d}" for i in range(n)],
            "Age": np.random.choice(["Young (<30)", "Middle (30-50)", "Senior (>50)"], size=n, p=[0.3, 0.5, 0.2]),
            "Gender": np.random.choice(["Male", "Female"], size=n, p=[0.55, 0.45]),
            "Marital_Status": np.random.choice(["Single", "Married"], size=n, p=[0.4, 0.6]),
            "Employment_Type": np.random.choice(["Salaried", "Self-Employed", "Business Owner"], size=n, p=[0.5, 0.3, 0.2]),
            "Annual_Income": np.random.randint(30000, 150000, size=n),
            "Credit_Score": np.random.randint(580, 820, size=n),
            "Approval_Decision": np.random.choice([1, 0], size=n, p=[0.65, 0.35]),
            "Default_12M": np.random.choice([1, 0], size=n, p=[0.15, 0.85])
        })
    return store_dataframe(df, "credit_data_benchmark.csv")

def get_dataframe(file_id: str) -> pd.DataFrame:
    """Retrieves dataframe by session ID."""
    if file_id not in DATA_SETS:
        raise KeyError(f"File ID {file_id} not found in session memory.")
    return DATA_SETS[file_id]

def auto_bin_series(series: pd.Series, col_name: str) -> Tuple[pd.Series, str]:
    """
    Bins numeric series into discrete categorical labels if continuous.
    Returns (binned_series, reference_group).
    """
    if not pd.api.types.is_numeric_dtype(series) or series.nunique() <= 5:
        ref = str(series.mode()[0]) if len(series.mode()) > 0 else str(series.iloc[0])
        return series.astype(str), ref

    vals = series.dropna()
    if 'age' in col_name.lower():
        bins = [-np.inf, 30, 50, np.inf]
        labels = ['Young (<30)', 'Middle (30-50)', 'Senior (>50)']
        binned = pd.cut(series, bins=bins, labels=labels)
        return binned.astype(str), 'Middle (30-50)'
    
    # Quantile tertiles for continuous metrics
    try:
        q1, q2 = vals.quantile(0.33), vals.quantile(0.67)
        bins = [-np.inf, q1, q2, np.inf]
        labels = [f'Low (<={round(q1, 1)})', f'Med ({round(q1, 1)}-{round(q2, 1)})', f'High (>{round(q2, 1)})']
        binned = pd.cut(series, bins=bins, labels=labels)
        return binned.astype(str), labels[1]
    except Exception:
        bins = [-np.inf, vals.median(), np.inf]
        labels = ['Low', 'High']
        binned = pd.cut(series, bins=bins, labels=labels)
        return binned.astype(str), 'High'
