"""
Script to generate modular Jupyter Notebooks:
01_Data_Cleaning_and_Audit.ipynb
02_Feature_Engineering_and_EDA.ipynb
03_RFM_vs_KMeans_Clustering.ipynb
04_Segment_Profiling_and_Stability.ipynb
"""

import os
import nbformat as nbf

os.makedirs('notebooks', exist_ok=True)

def create_nb(filename, cells):
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    }
    nb.cells = cells
    path = os.path.join('notebooks', filename)
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Generated {path}")

# Notebook 01
cells_01 = [
    nbf.v4.new_markdown_cell("# 01. Data Cleaning & Healthcare Data Quality Audit\nHyderabad Community Clinic Network - 500,000+ Records Across 4 Hospitals"),
    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import re
from datetime import datetime

df_opd = pd.read_csv('../data/raw/hyderabad_opd_visits.csv')
df_adm = pd.read_csv('../data/raw/hyderabad_admissions.csv')
df_lab = pd.read_csv('../data/raw/hyderabad_lab_tests.csv')
df_bill = pd.read_csv('../data/raw/hyderabad_billing.csv')

print(f"Total rows: {len(df_opd) + len(df_adm) + len(df_lab) + len(df_bill):,d}")"""),
    nbf.v4.new_markdown_cell("## 1. Age Standardisation (Parsing Date-of-Birth Entries)"),
    nbf.v4.new_code_cell("""def parse_age(val, ref_year=2023):
    if pd.isna(val): return np.nan
    s = str(val).strip()
    iso = re.match(r'^(\\d{4})[-/](\\d{1,2})[-/](\\d{1,2})$', s)
    if iso: return max(0, ref_year - int(iso.group(1)))
    dmy = re.match(r'^(\\d{1,2})[-/](\\d{1,2})[-/](\\d{4})$', s)
    if dmy: return max(0, ref_year - int(dmy.group(3)))
    str_m = re.match(r'^(\\d+)\\s*(?:yrs|years|y)?$', s, re.IGNORECASE)
    if str_m: return int(str_m.group(1))
    try:
        f = float(s)
        return ref_year - int(f) if f > 1900 and f <= ref_year else int(f)
    except: return np.nan

df_opd['age_cleaned'] = df_opd['raw_age'].apply(parse_age)
df_opd['age_cleaned'] = df_opd['age_cleaned'].fillna(df_opd['age_cleaned'].median()).astype(int)
print("Age summary:", df_opd['age_cleaned'].describe())"""),
    nbf.v4.new_markdown_cell("## 2. Standardising Free-Text Diagnoses"),
    nbf.v4.new_code_cell("""def categorize_diagnosis(text):
    if pd.isna(text): return 'General / Unspecified'
    t = str(text).lower()
    if any(k in t for k in ['diabet', 't2dm', 'dm-ii', 'dm2', 'sugar', 'neuropathy']): return 'Cardiometabolic (Diabetes)'
    elif any(k in t for k in ['hypertens', 'htn', 'cad', 'coronary', 'cardio', 'stent', 'dyslipid', 'cholesterol', 'fatty liver']): return 'Cardiovascular & Metabolic'
    elif any(k in t for k in ['asthma', 'astma', 'copd', 'bronch', 'urti', 'respirat', 'rhinitis']): return 'Respiratory'
    elif any(k in t for k in ['gastro', 'age ', 'vomit', 'diarrhea', 'pyrexia', 'fever', 'dengue', 'typhoid', 'malaria', 'uti']): return 'Acute Infectious / GI'
    elif any(k in t for k in ['osteoarth', 'oa ', 'knee', 'spondyl', 'backache', 'disc', 'sprain']): return 'Orthopedic & Musculoskeletal'
    elif any(k in t for k in ['antenatal', 'anc ', 'pregnan', 'pcod', 'pcos', 'pediatric', 'baby']): return 'Maternal & Child Health'
    elif any(k in t for k in ['executive', 'master health', 'screening', 'checkup', 'malaise']): return 'Preventive & Wellness'
    return 'General Medicine / Other'

df_opd['diagnosis_category'] = df_opd['diagnosis_raw'].apply(categorize_diagnosis)
print(df_opd['diagnosis_category'].value_counts())"""),
    nbf.v4.new_markdown_cell("## 3. Rectifying Double-Counted GST Billing Glitch"),
    nbf.v4.new_code_cell("""ratio = df_bill['total_billed_amount'] / (df_bill['base_charge'] * 1.18)
double_gst_mask = ratio > 1.10
df_bill['net_billing_amount'] = np.where(double_gst_mask, np.round(df_bill['total_billed_amount'] / 1.18, 2), df_bill['total_billed_amount'])
print(f"Corrected invoices: {double_gst_mask.sum():,d} of {len(df_bill):,d}")""")
]
create_nb('01_Data_Cleaning_and_Audit.ipynb', cells_01)

# Notebook 02
cells_02 = [
    nbf.v4.new_markdown_cell("# 02. Feature Engineering & Exploratory Data Analysis\nPatient Entity Feature Store with Behavioral, Clinical, and Seasonal Dimensions"),
    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pt_master = pd.read_csv('../data/processed/patient_features.csv')
print("Shape of Patient Feature Store:", pt_master.shape)
pt_master.head()"""),
    nbf.v4.new_markdown_cell("## Feature Distributions & Skewness Handling"),
    nbf.v4.new_code_cell("""features = ['recency_days', 'frequency', 'monetary', 'growth_rate', 'seasonality_index', 'avg_los', 'clinical_acuity']
print("Feature Skewness:")
print(pt_master[features].skew().round(2))

# Log transformations
pt_master['log_recency'] = np.log1p(pt_master['recency_days'])
pt_master['log_frequency'] = np.log1p(pt_master['frequency'])
pt_master['log_monetary'] = np.log1p(pt_master['monetary'])
pt_master['log_clinical_acuity'] = np.log1p(pt_master['clinical_acuity'])""")
]
create_nb('02_Feature_Engineering_and_EDA.ipynb', cells_02)

# Notebook 03
cells_03 = [
    nbf.v4.new_markdown_cell("# 03. Patient Segmentation: RFM vs K-Means Clustering\nMethodology Comparison, Elbow Curve, and Silhouette Analysis"),
    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from IPython.display import Image

pt_master = pd.read_csv('../data/processed/final_patient_segments.csv')
print("Final Cluster Segments:")
print(pt_master['segment_name'].value_counts(normalize=True).round(3) * 100)"""),
    nbf.v4.new_markdown_cell("## Elbow Curve & Silhouette Validation"),
    nbf.v4.new_code_cell("""Image('../outputs/charts/elbow_and_silhouette_analysis.png')"""),
    nbf.v4.new_markdown_cell("## Frequency vs Monetary Spend by Cluster"),
    nbf.v4.new_code_cell("""Image('../outputs/charts/rfm_vs_kmeans_scatter.png')""")
]
create_nb('03_RFM_vs_KMeans_Clustering.ipynb', cells_03)

# Notebook 04
cells_04 = [
    nbf.v4.new_markdown_cell("# 04. Segment Profiling, Concrete Actions & Stability Analysis\nClinical Benchmarks, Operational Recommendations, and 2-Year Entity Migration Matrix"),
    nbf.v4.new_code_cell("""import pandas as pd
from IPython.display import Image

df_profile = pd.read_csv('../outputs/tables/segment_profile_summary.csv')
df_actions = pd.read_csv('../outputs/tables/segment_actionable_recommendations.csv')
df_migration = pd.read_csv('../outputs/tables/segment_stability_migration_matrix.csv', index_col=0)"""),
    nbf.v4.new_markdown_cell("## 1. Segment Profile Table"),
    nbf.v4.new_code_cell("""df_profile"""),
    nbf.v4.new_markdown_cell("## 2. Clinical Benchmarks (ALOS, Readmission, Bed Occupancy)"),
    nbf.v4.new_code_cell("""Image('../outputs/charts/clinical_kpi_profile_bars.png')"""),
    nbf.v4.new_markdown_cell("## 3. Concrete Action Recommendations & ROI"),
    nbf.v4.new_code_cell("""df_actions[['Segment Name', 'Concrete Action', 'Estimated Cost (INR)', 'Expected Benefit (INR)', 'Net ROI (%)', 'Measurable KPI Target']]"""),
    nbf.v4.new_markdown_cell("## 4. 2-Year Segment Migration Matrix & Heatmap"),
    nbf.v4.new_code_cell("""Image('../outputs/charts/segment_migration_matrix_heatmap.png')""")
]
create_nb('04_Segment_Profiling_and_Stability.ipynb', cells_04)
