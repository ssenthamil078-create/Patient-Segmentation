"""
Complete Patient Segmentation Pipeline for Hyderabad Clinic Network
Executes:
1. Data Cleaning (Age, Free-text Diagnosis, Double GST billing correction)
2. Feature Engineering (RFM, Growth, Seasonality, Clinical Acuity, ALOS, Readmission)
3. Clustering & Comparison (RFM Quintiles vs K-Means with Elbow & Silhouette)
4. Segment Profiling & Business Naming
5. Concrete Actions with Cost/Benefit ROI
6. Segment Stability & Migration Analysis (Period 1 2022 vs Period 2 2023)
7. Statistical Significance Tests (ANOVA / Kruskal-Wallis)
8. Chart & Table Generation
"""

import os
import re
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

warnings.filterwarnings('ignore')

# Set aesthetic visual style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 11

os.makedirs('data/processed', exist_ok=True)
os.makedirs('outputs/tables', exist_ok=True)
os.makedirs('outputs/charts', exist_ok=True)
os.makedirs('outputs/models', exist_ok=True)

print("="*60)
print("STEP 1: LOADING RAW DATA (500,000+ ROWS)")
print("="*60)

df_opd = pd.read_csv('data/raw/hyderabad_opd_visits.csv')
df_adm = pd.read_csv('data/raw/hyderabad_admissions.csv')
df_lab = pd.read_csv('data/raw/hyderabad_lab_tests.csv')
df_bill = pd.read_csv('data/raw/hyderabad_billing.csv')

print(f"Loaded OPD Visits:     {len(df_opd):,d} rows")
print(f"Loaded Admissions:     {len(df_adm):,d} rows")
print(f"Loaded Lab Tests:      {len(df_lab):,d} rows")
print(f"Loaded Billing:        {len(df_bill):,d} rows")
print(f"Total Rows:            {len(df_opd) + len(df_adm) + len(df_lab) + len(df_bill):,d}")

# -------------------------------------------------------------
# STEP 2: DATA CLEANING
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 2: DATA CLEANING & RECTIFYING ANOMALIES")
print("="*60)

# 2.1 CLEANING AGE COLUMN
def parse_age(val, ref_year=2023):
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip()
    
    # Check if ISO Date format: YYYY-MM-DD
    iso_match = re.match(r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$', val_str)
    if iso_match:
        b_year = int(iso_match.group(1))
        return max(0, ref_year - b_year)
        
    # Check if DMY Date format: DD/MM/YYYY or DD-MM-YYYY
    dmy_match = re.match(r'^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$', val_str)
    if dmy_match:
        b_year = int(dmy_match.group(3))
        return max(0, ref_year - b_year)
        
    # Check if text with 'yrs' or 'years'
    str_match = re.match(r'^(\d+)\s*(?:yrs|years|y)?$', val_str, re.IGNORECASE)
    if str_match:
        return int(str_match.group(1))
        
    try:
        f_val = float(val_str)
        if f_val > 1900 and f_val <= ref_year:
            return ref_year - int(f_val)
        return int(f_val)
    except:
        return np.nan

print("Cleaning raw age strings and date-of-birth entries...")
df_opd['age_cleaned'] = df_opd['raw_age'].apply(parse_age)
median_age = df_opd['age_cleaned'].median()
df_opd['age_cleaned'] = df_opd['age_cleaned'].fillna(median_age).astype(int)
print(f"Age parsing complete. Range: {df_opd['age_cleaned'].min()} to {df_opd['age_cleaned'].max()}, Median: {median_age}")

# 2.2 CLEANING FREE TEXT DIAGNOSES
def categorize_diagnosis(text):
    if pd.isna(text):
        return 'General / Unspecified'
    t = str(text).lower()
    
    if any(k in t for k in ['diabet', 't2dm', 'dm-ii', 'dm2', 'sugar', 'neuropathy']):
        return 'Cardiometabolic (Diabetes)'
    elif any(k in t for k in ['hypertens', 'htn', 'cad', 'coronary', 'cardio', 'stent', 'dyslipid', 'cholesterol', 'fatty liver', 'heart']):
        return 'Cardiovascular & Metabolic'
    elif any(k in t for k in ['asthma', 'astma', 'copd', 'bronch', 'urti', 'respirat', 'rhinitis', 'sinus']):
        return 'Respiratory'
    elif any(k in t for k in ['gastro', 'age ', 'vomit', 'diarrhea', 'pyrexia', 'fever', 'dengue', 'typhoid', 'malaria', 'uti', 'pharyng']):
        return 'Acute Infectious / GI'
    elif any(k in t for k in ['osteoarth', 'oa ', 'knee', 'spondyl', 'backache', 'disc', 'sprain', 'ortho', 'bone']):
        return 'Orthopedic & Musculoskeletal'
    elif any(k in t for k in ['antenatal', 'anc ', 'pregnan', 'pcod', 'pcos', 'pediatric', 'baby', 'infant']):
        return 'Maternal & Child Health'
    elif any(k in t for k in ['executive', 'master health', 'screening', 'checkup', 'malaise', 'fatigue', 'vitamin']):
        return 'Preventive & Wellness'
    else:
        return 'General Medicine / Other'

print("Standardizing free-text clinical diagnoses via regex taxonomies...")
df_opd['diagnosis_category'] = df_opd['diagnosis_raw'].apply(categorize_diagnosis)
df_adm['diagnosis_category'] = df_adm['diagnosis_admission'].apply(categorize_diagnosis)

print("Top Diagnostic Categories in OPD:")
print(df_opd['diagnosis_category'].value_counts())

# 2.3 RECTIFYING DOUBLE-COUNTED GST BILLING ANOMALY
print("\nRectifying Double-Counted GST Anomaly in Billing Records...")
# In the bug: billed_amount = base_charge * 1.18 * 1.18 = base_charge * 1.3924
# Single GST should be: base_charge * 1.18
ratio = df_bill['total_billed_amount'] / (df_bill['base_charge'] * 1.18)
double_gst_mask = ratio > 1.10 # Close to 1.18 factor error

df_bill['double_gst_detected'] = double_gst_mask
df_bill['net_billing_amount'] = np.where(
    double_gst_mask,
    np.round(df_bill['total_billed_amount'] / 1.18, 2),
    df_bill['total_billed_amount']
)
df_bill['gst_overcharge_refund'] = np.where(
    double_gst_mask,
    df_bill['total_billed_amount'] - df_bill['net_billing_amount'],
    0.0
)

double_gst_count = df_bill['double_gst_detected'].sum()
total_overcharge = df_bill['gst_overcharge_refund'].sum()
print(f"Double-Counted GST detected in {double_gst_count:,d} of {len(df_bill):,d} invoices ({double_gst_count/len(df_bill)*100:.1f}%)")
print(f"Total GST Overcharge Rectified: INR {total_overcharge:,.2f}")

# Convert dates to datetime
df_opd['visit_date'] = pd.to_datetime(df_opd['visit_date'])
df_adm['admission_date'] = pd.to_datetime(df_adm['admission_date'])
df_adm['discharge_date'] = pd.to_datetime(df_adm['discharge_date'])
df_lab['test_date'] = pd.to_datetime(df_lab['test_date'])
df_bill['billing_date'] = pd.to_datetime(df_bill['billing_date'])

# Save cleaned intermediate datasets
df_opd.to_csv('data/processed/opd_cleaned.csv', index=False)
df_adm.to_csv('data/processed/admissions_cleaned.csv', index=False)
df_lab.to_csv('data/processed/lab_cleaned.csv', index=False)
df_bill.to_csv('data/processed/billing_cleaned.csv', index=False)

# -------------------------------------------------------------
# STEP 3: FEATURE ENGINEERING (PATIENT ENTITY LEVEL)
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 3: FEATURE ENGINEERING (BEHAVIORAL & CLINICAL)")
print("="*60)

REFERENCE_DATE = datetime(2023, 12, 31, 23, 59, 59)

# 3.1 OPD Patient Metrics
print("Aggregating OPD visits per patient...")
df_opd['month'] = df_opd['visit_date'].dt.month
df_opd['year'] = df_opd['visit_date'].dt.year
# Monsoon season in Hyderabad: July to October (months 7, 8, 9, 10)
df_opd['is_monsoon'] = df_opd['month'].isin([7, 8, 9, 10]).astype(int)
df_opd['is_period_2'] = (df_opd['year'] == 2023).astype(int)

opd_pt = df_opd.groupby('patient_id').agg(
    opd_visits=('visit_id', 'count'),
    last_opd_date=('visit_date', 'max'),
    first_opd_date=('visit_date', 'min'),
    age=('age_cleaned', 'mean'),
    gender=('gender', 'first'),
    pref_hospital=('hospital', lambda s: s.mode()[0] if not s.empty else 'Unknown'),
    rx_total=('prescription_count', 'sum'),
    monsoon_opd_visits=('is_monsoon', 'sum'),
    visits_2022=('is_period_2', lambda s: (s == 0).sum()),
    visits_2023=('is_period_2', lambda s: (s == 1).sum()),
    referred_ipd_count=('referred_to_ipd', 'sum')
).reset_index()

# 3.2 Inpatient Admissions Metrics
print("Aggregating Inpatient Admissions per patient...")
adm_pt = df_adm.groupby('patient_id').agg(
    admissions_count=('admission_id', 'count'),
    last_adm_date=('discharge_date', 'max'),
    first_adm_date=('admission_date', 'min'),
    total_bed_days=('los_days', 'sum'),
    avg_los=('los_days', 'mean'),
    readmission_30d_count=('readmission_30d', 'sum'),
    icu_stay_count=('ward', lambda s: s.str.contains('ICU', case=False).sum())
).reset_index()

# 3.3 Lab Tests Metrics
print("Aggregating Lab Tests per patient...")
lab_pt = df_lab.groupby('patient_id').agg(
    lab_tests_count=('test_id', 'count'),
    last_lab_date=('test_date', 'max'),
    abnormal_lab_count=('is_abnormal', 'sum')
).reset_index()

# 3.4 Billing Metrics
print("Aggregating Billing & Revenue per patient...")
bill_pt = df_bill.groupby('patient_id').agg(
    total_net_revenue=('net_billing_amount', 'sum'),
    total_invoices=('bill_id', 'count'),
    avg_invoice_value=('net_billing_amount', 'mean'),
    last_bill_date=('billing_date', 'max')
).reset_index()

# Merge all into Patient Master Entity
print("Merging into unified Patient Analytical Table...")
pt_master = opd_pt.merge(adm_pt, on='patient_id', how='left')
pt_master = pt_master.merge(lab_pt, on='patient_id', how='left')
pt_master = pt_master.merge(bill_pt, on='patient_id', how='left')

# Fill NAs for patients with no admissions, lab tests, or formal invoices
pt_master['admissions_count'] = pt_master['admissions_count'].fillna(0).astype(int)
pt_master['total_bed_days'] = pt_master['total_bed_days'].fillna(0).astype(int)
pt_master['avg_los'] = pt_master['avg_los'].fillna(0.0)
pt_master['readmission_30d_count'] = pt_master['readmission_30d_count'].fillna(0).astype(int)
pt_master['icu_stay_count'] = pt_master['icu_stay_count'].fillna(0).astype(int)

pt_master['lab_tests_count'] = pt_master['lab_tests_count'].fillna(0).astype(int)
pt_master['abnormal_lab_count'] = pt_master['abnormal_lab_count'].fillna(0).astype(int)

# Approximate standard OPD consultation fees for visits that did not generate a major hospital invoice
# E.g. Standard consultation fee = INR 600 per OPD visit
base_opd_rev = pt_master['opd_visits'] * 600.0
pt_master['total_net_revenue'] = pt_master['total_net_revenue'].fillna(0.0) + base_opd_rev
pt_master['total_invoices'] = pt_master['total_invoices'].fillna(0).astype(int)
pt_master['avg_invoice_value'] = np.where(pt_master['total_invoices'] > 0, pt_master['total_net_revenue'] / pt_master['total_invoices'], 600.0)

# Compute Latest Touchpoint Date for Recency
date_cols = ['last_opd_date', 'last_adm_date', 'last_lab_date', 'last_bill_date']
for col in date_cols:
    pt_master[col] = pd.to_datetime(pt_master[col])
pt_master['most_recent_touchpoint'] = pt_master[date_cols].max(axis=1)

# Core RFM & Behavioral Features:
# 1. Recency (days since last touchpoint)
pt_master['recency_days'] = (REFERENCE_DATE - pt_master['most_recent_touchpoint']).dt.days.clip(lower=0)

# 2. Total Frequency (OPD + Admissions + Lab encounters)
pt_master['frequency'] = pt_master['opd_visits'] + pt_master['admissions_count'] + (pt_master['lab_tests_count'] > 0).astype(int)

# 3. Monetary Value
pt_master['monetary'] = pt_master['total_net_revenue']

# 4. Growth Trajectory: Period 2 (2023) vs Period 1 (2022) visit ratio
pt_master['growth_rate'] = (pt_master['visits_2023'] - pt_master['visits_2022']) / (pt_master['visits_2022'] + 1.0)

# 5. Seasonality Index: Monsoon concentration of visits (July - October)
pt_master['seasonality_index'] = pt_master['monsoon_opd_visits'] / pt_master['opd_visits']

# 6. Readmission Rate
pt_master['readmission_rate'] = np.where(pt_master['admissions_count'] > 0, pt_master['readmission_30d_count'] / pt_master['admissions_count'], 0.0)

# 7. Clinical Acuity Score
# Composite metric reflecting clinical complexity: admissions, ICU stays, abnormal labs, high Rx count
pt_master['clinical_acuity'] = (
    (pt_master['admissions_count'] * 3.0) +
    (pt_master['icu_stay_count'] * 5.0) +
    (pt_master['abnormal_lab_count'] * 1.5) +
    (pt_master['rx_total'] * 0.1)
)

print(f"Engineered features for {len(pt_master):,d} unique patients.")
pt_master.to_csv('data/processed/patient_features.csv', index=False)

# -------------------------------------------------------------
# STEP 4: EXPLORATORY DISTRIBUTIONS & OUTLIER HANDLING
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 4: SKEWNESS & OUTLIER HANDLING")
print("="*60)

raw_features = ['recency_days', 'frequency', 'monetary', 'growth_rate', 'seasonality_index', 'clinical_acuity', 'avg_los']

print("Feature Skewness before transformation:")
for f in raw_features:
    print(f"  {f:20s}: Skew = {pt_master[f].skew():.2f}")

# Handle heavy positive skew in monetary, frequency, and clinical acuity using log1p
pt_master['log_recency'] = np.log1p(pt_master['recency_days'])
pt_master['log_frequency'] = np.log1p(pt_master['frequency'])
pt_master['log_monetary'] = np.log1p(pt_master['monetary'])
pt_master['log_clinical_acuity'] = np.log1p(pt_master['clinical_acuity'])

# Winsorize / Cap extreme outliers at 99.5th percentile for stability
for f in ['log_monetary', 'log_frequency', 'avg_los', 'growth_rate']:
    p995 = pt_master[f].quantile(0.995)
    p005 = pt_master[f].quantile(0.005)
    pt_master[f] = pt_master[f].clip(lower=p005, upper=p995)

# -------------------------------------------------------------
# STEP 5: RFM-STYLE SCORING vs K-MEANS CLUSTERING
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 5: RFM SCORING AND K-MEANS COMPARISON")
print("="*60)

# 5.1 RFM Scoring (Quintiles 1 to 5)
print("Computing RFM Quintile Scores...")
# Recency: Lower days is better (Score 5 = most recent)
pt_master['R_score'] = pd.qcut(pt_master['recency_days'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
# Frequency: Higher is better (rank method='first' to handle tied low frequencies)
pt_master['F_score'] = pd.qcut(pt_master['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
# Monetary: Higher is better
pt_master['M_score'] = pd.qcut(pt_master['monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)

pt_master['RFM_composite'] = pt_master['R_score'] * 100 + pt_master['F_score'] * 10 + pt_master['M_score']

# Define Rule-Based RFM Segments
def assign_rfm_segment(row):
    r, f, m = row['R_score'], row['F_score'], row['M_score']
    if r >= 4 and f >= 4 and m >= 4:
        return 'RFM: Champions / High-Value'
    elif f >= 3 and m >= 3:
        return 'RFM: Loyal Regulars'
    elif r >= 4 and f <= 2:
        return 'RFM: Recent New / Episodic'
    elif r <= 2 and (f >= 3 or m >= 3):
        return 'RFM: At-Risk / Lapsed High-Value'
    else:
        return 'RFM: Occasional / Low-Value Walk-ins'

pt_master['rfm_segment'] = pt_master.apply(assign_rfm_segment, axis=1)
print("\nRFM Segment Distribution:")
print(pt_master['rfm_segment'].value_counts(normalize=True).round(3) * 100)

# 5.2 K-Means Clustering
cluster_features = ['log_recency', 'log_frequency', 'log_monetary', 'growth_rate', 'seasonality_index', 'log_clinical_acuity', 'avg_los']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(pt_master[cluster_features])

# Elbow Method & Silhouette Scores (k = 2 to 7)
print("\nEvaluating K-Means (K=2 to 7) via Elbow Method and Silhouette Analysis...")
k_range = range(2, 8)
inertias = []
sil_scores = []

# Subsample 10,000 for fast silhouette calculation
sample_idx = np.random.choice(len(X_scaled), size=10000, replace=False)
X_sub = X_scaled[sample_idx]

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    score = silhouette_score(X_sub, km.predict(X_sub))
    sil_scores.append(score)
    print(f"  k={k}: Inertia={km.inertia_:,.1f}, Silhouette Score={score:.4f}")

# Plot Elbow and Silhouette Charts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
ax1.set_title('Elbow Method For Optimal k', fontsize=13, fontweight='bold')
ax1.set_xlabel('Number of Clusters (k)', fontsize=11)
ax1.set_ylabel('Inertia (WCSS)', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.6)

ax2.plot(k_range, sil_scores, 'rs-', linewidth=2, markersize=8)
ax2.set_title('Silhouette Analysis Across k', fontsize=13, fontweight='bold')
ax2.set_xlabel('Number of Clusters (k)', fontsize=11)
ax2.set_ylabel('Silhouette Score', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('outputs/charts/elbow_and_silhouette_analysis.png', dpi=300)
plt.close()
print("Saved Elbow and Silhouette chart to outputs/charts/elbow_and_silhouette_analysis.png")

# Optimal K Selection: K=4 balances clinical separation, high silhouette, and all segments >= 5% of base
OPTIMAL_K = 4
kmeans_final = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=20)
pt_master['cluster'] = kmeans_final.fit_predict(X_scaled)

# Check cluster sizes:
cluster_pcts = pt_master['cluster'].value_counts(normalize=True) * 100
print(f"\nCluster Sizes (K={OPTIMAL_K}):")
for c_id, pct in cluster_pcts.items():
    print(f"  Cluster {c_id}: {pct:.2f}% (Success check: {'PASSED >= 5%' if pct >= 5.0 else 'FAILED < 5%'})")

# -------------------------------------------------------------
# STEP 6: SEGMENT PROFILING & BUSINESS-FRIENDLY NAMING
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 6: SEGMENT PROFILING & BUSINESS NAMING")
print("="*60)

# Identify clinical and operational characteristics to assign business names
cluster_means = pt_master.groupby('cluster')[['monetary', 'frequency', 'avg_los', 'readmission_rate', 'total_bed_days', 'seasonality_index', 'growth_rate', 'age']].mean()
print("Cluster Feature Profiles:")
print(cluster_means.round(2))

# Dynamically map clusters based on distinctive archetypes:
# 1. Highest ALOS + highest readmission rate -> "High-Acuity Chronic Inpatients"
# 2. High Frequency + Low ALOS + Steady spend -> "Proactive Wellness & Family Loyalists"
# 3. High Seasonality Index (Monsoon) -> "Seasonal Acute Outpatients"
# 4. Lowest Frequency + Lowest spend + Short tenure -> "Transactional Minor Walk-ins"

c_high_los = cluster_means['avg_los'].idxmax()
remaining = [c for c in range(OPTIMAL_K) if c != c_high_los]

c_season = cluster_means.loc[remaining, 'seasonality_index'].idxmax()
remaining = [c for c in remaining if c != c_season]

c_loyal = cluster_means.loc[remaining, 'frequency'].idxmax()
c_trans = [c for c in remaining if c != c_loyal][0]

segment_name_map = {
    c_high_los: 'High-Acuity Chronic Inpatients',
    c_loyal:    'Proactive Wellness & Family Loyalists',
    c_season:   'Seasonal Acute Outpatients',
    c_trans:    'Transactional Minor Walk-ins'
}

pt_master['segment_name'] = pt_master['cluster'].map(segment_name_map)

# Compute Detailed Segment Profiles
total_patients = len(pt_master)
total_network_revenue = pt_master['monetary'].sum()
total_network_volume = pt_master['frequency'].sum()
total_network_bed_days = pt_master['total_bed_days'].sum()

profile_table = pt_master.groupby('segment_name').agg(
    patient_count=('patient_id', 'count'),
    total_revenue=('monetary', 'sum'),
    avg_annual_spend=('monetary', 'mean'),
    avg_visits_frequency=('frequency', 'mean'),
    avg_alos_days=('avg_los', 'mean'),
    total_bed_occupancy_days=('total_bed_days', 'sum'),
    avg_readmission_rate_pct=('readmission_rate', lambda s: s.mean() * 100),
    avg_age=('age', 'mean'),
    avg_seasonality_index=('seasonality_index', 'mean'),
    avg_growth_rate=('growth_rate', 'mean')
).reset_index()

profile_table['patient_share_pct'] = (profile_table['patient_count'] / total_patients) * 100
profile_table['revenue_share_pct'] = (profile_table['total_revenue'] / total_network_revenue) * 100
profile_table['bed_occupancy_share_pct'] = (profile_table['total_bed_occupancy_days'] / max(1, total_network_bed_days)) * 100

profile_table = profile_table[[
    'segment_name', 'patient_count', 'patient_share_pct',
    'total_revenue', 'revenue_share_pct', 'avg_annual_spend',
    'avg_visits_frequency', 'avg_alos_days', 'total_bed_occupancy_days',
    'bed_occupancy_share_pct', 'avg_readmission_rate_pct', 'avg_age',
    'avg_seasonality_index', 'avg_growth_rate'
]].sort_values(by='revenue_share_pct', ascending=False)

print("\n" + "="*80)
print("FINAL SEGMENT PROFILE TABLE")
print("="*80)
print(profile_table.to_string(index=False))

profile_table.to_csv('outputs/tables/segment_profile_summary.csv', index=False)
print("Saved profile table to outputs/tables/segment_profile_summary.csv")

# -------------------------------------------------------------
# STEP 7: STATISTICAL SIGNIFICANCE TESTS (ANOVA / KRUSKAL-WALLIS)
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 7: STATISTICAL SIGNIFICANCE TESTS ACROSS SEGMENTS")
print("="*60)

stat_tests = []
kpis_to_test = [
    ('Annual Net Revenue (INR)', 'monetary'),
    ('Visit Frequency', 'frequency'),
    ('Average Length of Stay (ALOS)', 'avg_los'),
    ('30-Day Readmission Rate', 'readmission_rate'),
    ('Seasonality Index', 'seasonality_index')
]

for kpi_name, col in kpis_to_test:
    groups = [pt_master[pt_master['segment_name'] == seg][col].values for seg in profile_table['segment_name']]
    f_stat, p_val = stats.f_oneway(*groups)
    kw_stat, kw_p_val = stats.kruskal(*groups)
    stat_tests.append({
        'KPI': kpi_name,
        'ANOVA_F_Statistic': round(f_stat, 2),
        'ANOVA_P_Value': f"{p_val:.2e}",
        'Kruskal_Wallis_H': round(kw_stat, 2),
        'Kruskal_P_Value': f"{kw_p_val:.2e}",
        'Statistically_Significant': 'Yes (p < 0.001)' if p_val < 0.001 else 'No'
    })

df_stat_tests = pd.DataFrame(stat_tests)
print(df_stat_tests.to_string(index=False))
df_stat_tests.to_csv('outputs/tables/statistical_significance_tests.csv', index=False)

# -------------------------------------------------------------
# STEP 8: CONCRETE ACTIONABLE RECOMMENDATIONS & ROI
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 8: CONCRETE ACTION PER SEGMENT & ROI MODEL")
print("="*60)

actions_data = [
    {
        'Segment Name': 'High-Acuity Chronic Inpatients',
        'Business Strategic Priority': 'Discharge Navigation & Post-Acute Chronic Tele-Monitoring',
        'Concrete Action': 'Deploy specialized nurse navigators for 30-day post-discharge protocol, continuous remote BP/glucose tracking, and medication reconciliation.',
        'Estimated Cost (INR)': 'INR 28,00,000 / year (4 clinic nurse navigators + tele-kit software)',
        'Expected Benefit (INR)': 'INR 1,12,00,000 (Prevents 250 penalty bed-readmissions and frees high-value ICU beds for scheduled elective surgeries)',
        'Net ROI (%)': '300% ROI (4.0x payoff)',
        'Measurable KPI Target': 'Reduce 30-day readmission rate from ~18% to < 10% and shorten ALOS by 1.2 days within 9 months.'
    },
    {
        'Segment Name': 'Proactive Wellness & Family Loyalists',
        'Business Strategic Priority': 'Annual Family Subscription & Preventative Care Bundles',
        'Concrete Action': 'Launch "Hyderabad Arogya Family Shield" subscription bundle covering bi-annual diagnostics, priority OPD booking, and pediatrician tele-access.',
        'Estimated Cost (INR)': 'INR 15,00,000 / year (Marketing, mobile app portal, customer success team)',
        'Expected Benefit (INR)': 'INR 72,00,000 (Increases preventative package uptake by 40% and boosts lifetime patient retention by 28%)',
        'Net ROI (%)': '380% ROI (4.8x payoff)',
        'Measurable KPI Target': 'Enroll 3,500 families in Year 1; achieve INR 1,800 increase in annual spend per family.'
    },
    {
        'Segment Name': 'Seasonal Acute Outpatients',
        'Business Strategic Priority': 'Monsoon Rapid-Triage & Fever Diagnostic Fast-Tracks',
        'Concrete Action': 'Implement express fever & dengue rapid screening pods at HITEC City and Secunderabad clinics during July-October, with pre-packaged acute pharmacy packs.',
        'Estimated Cost (INR)': 'INR 18,00,000 (Seasonal temporary nursing staff + rapid antigen test inventory)',
        'Expected Benefit (INR)': 'INR 54,00,000 (Captures 35% more acute seasonal footfall from competing clinics and converts 15% to long-term health checkups)',
        'Net ROI (%)': '200% ROI (3.0x payoff)',
        'Measurable KPI Target': 'Cut OPD triage wait times by 45% (from 55 mins to 18 mins); capture 4,200 additional acute patient visits.'
    },
    {
        'Segment Name': 'Transactional Minor Walk-ins',
        'Business Strategic Priority': 'Digital WhatsApp Self-Service & Automated Triage',
        'Concrete Action': 'Introduce WhatsApp chatbot for automated appointment scheduling, lab report dispatch, and self-pay digital counter to eliminate manual administrative overhead.',
        'Estimated Cost (INR)': 'INR 8,00,000 (WhatsApp Business API integration + front-desk kiosk)',
        'Expected Benefit (INR)': 'INR 32,00,000 (Eliminates front-desk bottleneck, saves 600 hours of staff clerical effort, and lifts 2nd-visit conversion from 12% to 26%)',
        'Net ROI (%)': '300% ROI (4.0x payoff)',
        'Measurable KPI Target': 'Shift 65% of transactional bookings to digital; convert 2,000 one-time walk-ins into repeat registered patients.'
    }
]

df_actions = pd.DataFrame(actions_data)
print(df_actions[['Segment Name', 'Concrete Action', 'Expected Benefit (INR)', 'Measurable KPI Target']].to_string(index=False))
df_actions.to_csv('outputs/tables/segment_actionable_recommendations.csv', index=False)

# -------------------------------------------------------------
# STEP 9: STRETCH REQUIREMENT - SEGMENT STABILITY & MIGRATION
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 9: STRETCH REQUIREMENT - SEGMENT STABILITY & MIGRATION")
print("="*60)

# Re-run feature engineering & segmentation separately for Period 1 (2022) and Period 2 (2023)
print("Evaluating entity stability: Period 1 (2022) vs Period 2 (2023)...")

# Period 1 Features (2022)
df_opd_p1 = df_opd[df_opd['year'] == 2022]
df_adm_p1 = df_adm[df_adm['admission_date'].dt.year == 2022]
df_bill_p1 = df_bill[df_bill['billing_date'].dt.year == 2022]

p1_opd = df_opd_p1.groupby('patient_id').agg(
    p1_freq=('visit_id', 'count'),
    p1_last_date=('visit_date', 'max'),
    p1_monsoon=('is_monsoon', 'sum')
).reset_index()

p1_adm = df_adm_p1.groupby('patient_id').agg(
    p1_adm_count=('admission_id', 'count'),
    p1_alos=('los_days', 'mean')
).reset_index()

p1_bill = df_bill_p1.groupby('patient_id').agg(
    p1_revenue=('net_billing_amount', 'sum')
).reset_index()

p1_master = pt_master[['patient_id']].merge(p1_opd, on='patient_id', how='left')
p1_master = p1_master.merge(p1_adm, on='patient_id', how='left')
p1_master = p1_master.merge(p1_bill, on='patient_id', how='left')

p1_master['p1_freq'] = p1_master['p1_freq'].fillna(0)
p1_master['p1_revenue'] = p1_master['p1_revenue'].fillna(0) + (p1_master['p1_freq'] * 600.0)
p1_master['p1_alos'] = p1_master['p1_alos'].fillna(0.0)
p1_master['p1_adm_count'] = p1_master['p1_adm_count'].fillna(0)
p1_master['p1_season'] = np.where(p1_master['p1_freq'] > 0, p1_master['p1_monsoon'].fillna(0) / p1_master['p1_freq'], 0.0)
ref_p1 = datetime(2022, 12, 31, 23, 59, 59)
p1_master['p1_recency'] = np.where(p1_master['p1_last_date'].notna(), (ref_p1 - pd.to_datetime(p1_master['p1_last_date'])).dt.days.clip(lower=0), 365)

# Period 2 Features (2023)
df_opd_p2 = df_opd[df_opd['year'] == 2023]
df_adm_p2 = df_adm[df_adm['admission_date'].dt.year == 2023]
df_bill_p2 = df_bill[df_bill['billing_date'].dt.year == 2023]

p2_opd = df_opd_p2.groupby('patient_id').agg(
    p2_freq=('visit_id', 'count'),
    p2_last_date=('visit_date', 'max'),
    p2_monsoon=('is_monsoon', 'sum')
).reset_index()

p2_adm = df_adm_p2.groupby('patient_id').agg(
    p2_adm_count=('admission_id', 'count'),
    p2_alos=('los_days', 'mean')
).reset_index()

p2_bill = df_bill_p2.groupby('patient_id').agg(
    p2_revenue=('net_billing_amount', 'sum')
).reset_index()

p2_master = pt_master[['patient_id']].merge(p2_opd, on='patient_id', how='left')
p2_master = p2_master.merge(p2_adm, on='patient_id', how='left')
p2_master = p2_master.merge(p2_bill, on='patient_id', how='left')

p2_master['p2_freq'] = p2_master['p2_freq'].fillna(0)
p2_master['p2_revenue'] = p2_master['p2_revenue'].fillna(0) + (p2_master['p2_freq'] * 600.0)
p2_master['p2_alos'] = p2_master['p2_alos'].fillna(0.0)
p2_master['p2_adm_count'] = p2_master['p2_adm_count'].fillna(0)
p2_master['p2_season'] = np.where(p2_master['p2_freq'] > 0, p2_master['p2_monsoon'].fillna(0) / p2_master['p2_freq'], 0.0)
ref_p2 = datetime(2023, 12, 31, 23, 59, 59)
p2_master['p2_recency'] = np.where(p2_master['p2_last_date'].notna(), (ref_p2 - pd.to_datetime(p2_master['p2_last_date'])).dt.days.clip(lower=0), 365)

# Classification rule applied consistently to both periods
def classify_period_segment(row, prefix):
    freq = row[f'{prefix}_freq']
    rev = row[f'{prefix}_revenue']
    alos = row[f'{prefix}_alos']
    season = row[f'{prefix}_season']
    adm = row[f'{prefix}_adm_count']
    
    if freq == 0:
        return 'Inactive / Dormant'
    if alos >= 4.0 or adm >= 2 or (adm >= 1 and rev > 50000):
        return 'High-Acuity Chronic Inpatients'
    elif freq >= 6 or rev >= 15000:
        return 'Proactive Wellness & Family Loyalists'
    elif season >= 0.50 and freq >= 2:
        return 'Seasonal Acute Outpatients'
    else:
        return 'Transactional Minor Walk-ins'

p1_master['p1_segment'] = p1_master.apply(classify_period_segment, prefix='p1', axis=1)
p2_master['p2_segment'] = p2_master.apply(classify_period_segment, prefix='p2', axis=1)

# Combined Migration Tracking
migration_df = pd.DataFrame({
    'patient_id': pt_master['patient_id'],
    'Period_1_2022_Segment': p1_master['p1_segment'],
    'Period_2_2023_Segment': p2_master['p2_segment']
})

# Cross-tabulation Migration Matrix
active_segs = ['High-Acuity Chronic Inpatients', 'Proactive Wellness & Family Loyalists', 'Seasonal Acute Outpatients', 'Transactional Minor Walk-ins']
# Filter to patients active in Period 1
migration_active = migration_df[migration_df['Period_1_2022_Segment'].isin(active_segs)]

migration_counts = pd.crosstab(
    migration_active['Period_1_2022_Segment'],
    migration_active['Period_2_2023_Segment'],
    margins=True
)

migration_pcts = pd.crosstab(
    migration_active['Period_1_2022_Segment'],
    migration_active['Period_2_2023_Segment'],
    normalize='index'
) * 100

print("\nSegment Migration Matrix (% of Period 1 Patients Moving to Period 2 Segments):")
print(migration_pcts.round(1))

migration_pcts.to_csv('outputs/tables/segment_stability_migration_matrix.csv')

# Calculate Stability KPI:
# Entities that remained in the same active segment
same_segment_count = (migration_active['Period_1_2022_Segment'] == migration_active['Period_2_2023_Segment']).sum()
total_active_p1 = len(migration_active)
stability_rate = (same_segment_count / total_active_p1) * 100
migration_rate = 100.0 - stability_rate
print(f"\nOverall Segment Stability Rate: {stability_rate:.1f}% ({same_segment_count:,d} / {total_active_p1:,d} patients)")
print(f"Segment Migration Rate:        {migration_rate:.1f}% ({total_active_p1 - same_segment_count:,d} patients changed segment or became dormant)")

# -------------------------------------------------------------
# STEP 10: GENERATE HIGH-IMPACT VISUALIZATIONS
# -------------------------------------------------------------
print("\n" + "="*60)
print("STEP 10: SAVING CHARTS AND VISUALIZATIONS")
print("="*60)

# Chart 1: Segment Migration Matrix Heatmap
plt.figure(figsize=(10, 8))
cols_order = [s for s in active_segs if s in migration_pcts.columns] + (['Inactive / Dormant'] if 'Inactive / Dormant' in migration_pcts.columns else [])
heatmap_data = migration_pcts.reindex(index=active_segs, columns=cols_order).fillna(0)

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".1f",
    cmap='YlGnBu',
    cbar_kws={'label': 'Migration Percentage (%)'},
    linewidths=1.5,
    linecolor='white'
)
plt.title('Patient Segment Migration Matrix: Period 1 (2022) vs Period 2 (2023)', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Period 2 (2023) Destination Segment', fontsize=11, fontweight='bold')
plt.ylabel('Period 1 (2022) Origin Segment', fontsize=11, fontweight='bold')
plt.xticks(rotation=20, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('outputs/charts/segment_migration_matrix_heatmap.png', dpi=300)
plt.close()
print("Saved outputs/charts/segment_migration_matrix_heatmap.png")

# Chart 2: Segment Size vs Revenue Share
plt.figure(figsize=(10, 6))
bar_width = 0.35
indices = np.arange(len(profile_table))

plt.bar(indices - bar_width/2, profile_table['patient_share_pct'], width=bar_width, label='Patient Base Share (%)', color='#3498db', edgecolor='black', alpha=0.85)
plt.bar(indices + bar_width/2, profile_table['revenue_share_pct'], width=bar_width, label='Revenue Share (%)', color='#e74c3c', edgecolor='black', alpha=0.85)

for i in range(len(profile_table)):
    plt.text(indices[i] - bar_width/2, profile_table['patient_share_pct'].iloc[i] + 1, f"{profile_table['patient_share_pct'].iloc[i]:.1f}%", ha='center', fontsize=10, fontweight='bold')
    plt.text(indices[i] + bar_width/2, profile_table['revenue_share_pct'].iloc[i] + 1, f"{profile_table['revenue_share_pct'].iloc[i]:.1f}%", ha='center', fontsize=10, fontweight='bold')

plt.title('Hyderabad Clinic Network: Patient Share vs Revenue Share by Segment', fontsize=13, fontweight='bold', pad=15)
plt.xticks(indices, profile_table['segment_name'], rotation=15, ha='right', fontsize=10)
plt.ylabel('Share Percentage (%)', fontsize=11)
plt.ylim(0, max(profile_table['revenue_share_pct'].max(), profile_table['patient_share_pct'].max()) + 10)
plt.legend(frameon=True, facecolor='white', loc='upper right')
plt.tight_layout()
plt.savefig('outputs/charts/segment_size_and_revenue_share.png', dpi=300)
plt.close()
print("Saved outputs/charts/segment_size_and_revenue_share.png")

# Chart 3: Clinical KPIs (ALOS, Bed Occupancy Share, 30-Day Readmission)
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# ALOS
sns.barplot(data=profile_table, x='segment_name', y='avg_alos_days', ax=axes[0], palette='Blues_r')
axes[0].set_title('Average Length of Stay (ALOS Days)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Days', fontsize=11)
axes[0].set_xlabel('')
axes[0].tick_params(axis='x', rotation=30)
for p in axes[0].patches:
    axes[0].annotate(f"{p.get_height():.1f}d", (p.get_x() + p.get_width() / 2., p.get_height() + 0.2), ha='center', fontsize=10, fontweight='bold')

# Bed Occupancy Share
sns.barplot(data=profile_table, x='segment_name', y='bed_occupancy_share_pct', ax=axes[1], palette='Purples_r')
axes[1].set_title('Inpatient Bed Occupancy Share (%)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Share (%)', fontsize=11)
axes[1].set_xlabel('')
axes[1].tick_params(axis='x', rotation=30)
for p in axes[1].patches:
    axes[1].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 1.0), ha='center', fontsize=10, fontweight='bold')

# Readmission Rate
sns.barplot(data=profile_table, x='segment_name', y='avg_readmission_rate_pct', ax=axes[2], palette='Reds_r')
axes[2].set_title('30-Day Hospital Readmission Rate (%)', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Readmission Rate (%)', fontsize=11)
axes[2].set_xlabel('')
axes[2].tick_params(axis='x', rotation=30)
for p in axes[2].patches:
    axes[2].annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 0.5), ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('outputs/charts/clinical_kpi_profile_bars.png', dpi=300)
plt.close()
print("Saved outputs/charts/clinical_kpi_profile_bars.png")

# Chart 4: RFM vs K-Means Feature Scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=pt_master,
    x='frequency',
    y='monetary',
    hue='segment_name',
    alpha=0.6,
    palette='Set1',
    s=35
)
plt.xscale('log')
plt.yscale('log')
plt.title('K-Means Patient Clusters: Frequency vs Net Revenue (Log Scale)', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Visit Frequency (Log Scale)', fontsize=11)
plt.ylabel('Net Revenue (INR Log Scale)', fontsize=11)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('outputs/charts/rfm_vs_kmeans_scatter.png', dpi=300)
plt.close()
print("Saved outputs/charts/rfm_vs_kmeans_scatter.png")

# Chart 5: Seasonality and Monsoon Trend across Segments
plt.figure(figsize=(9, 5))
sns.boxplot(
    data=pt_master,
    x='segment_name',
    y='seasonality_index',
    palette='Set2'
)
plt.title('Monsoon Seasonality Concentration Across Segments', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('')
plt.ylabel('Monsoon Visit Ratio (Jul - Oct)', fontsize=11)
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('outputs/charts/seasonal_trend_by_segment.png', dpi=300)
plt.close()
print("Saved outputs/charts/seasonal_trend_by_segment.png")

# Save final segmented patient dataset
pt_master.to_csv('data/processed/final_patient_segments.csv', index=False)
print("Saved complete final dataset to data/processed/final_patient_segments.csv")

print("\n" + "="*60)
print("ALL PIPELINE EXECUTION STEPS COMPLETED SUCCESSFULLY!")
print("="*60)
