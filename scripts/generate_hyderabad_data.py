"""
Data Generation Script for Hyderabad Network of Community Clinics
Generates ~500,000 rows of realistic, anonymized healthcare data across 4 hospitals:
1. Banjara Hills Medical Centre
2. HITEC City Community Hospital
3. Secunderabad Care Clinic
4. Kukatpally Health Hub

Tables:
- OPD Visits (~280,000 rows)
- Inpatient Admissions (~45,000 rows)
- Laboratory Tests (~115,000 rows)
- Billing Records (~60,000 rows)
Total = 500,000 rows.

Data Quality Anomalies Embedded:
- Free text diagnoses instead of ICD codes (misspellings, clinical abbreviations, mixed case)
- Age entered as Date of Birth ('YYYY-MM-DD', 'DD/MM/YYYY') in ~25% of rows, strings ('45 yrs') in ~10%, and numeric integers elsewhere
- Billing records with double-counted 18% GST (amount inflated by 1.18 * 1.18) in ~40% of records
- Multi-hospital visits, seasonal dengue/viral surges in July-October (Hyderabad monsoon)
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

HOSPITALS = [
    'Banjara Hills Medical Centre',
    'HITEC City Community Hospital',
    'Secunderabad Care Clinic',
    'Kukatpally Health Hub'
]

HOSPITAL_PROBS = [0.32, 0.28, 0.22, 0.18]

DEPARTMENTS = [
    'General Medicine', 'Cardiology', 'Endocrinology', 'Pulmonology',
    'Pediatrics', 'Obstetrics & Gynecology', 'Orthopedics', 'Gastroenterology',
    'Dermatology', 'Emergency / Triage'
]

DOCTORS = {
    dept: [f"Dr. {name} ({dept[:4]})" for name in ["Rao", "Reddy", "Sharma", "Khan", "Patel", "Prasad", "Verma", "Murthy"]]
    for dept in DEPARTMENTS
}

FREE_TEXT_DIAGNOSES = {
    'Chronic Cardiometabolic': [
        'Type 2 Diabetes Mellitus', 'T2DM uncontrolled', 'diabtes type 2', 'DM-II with neuropathy',
        'Hypertension Stage 2', 'Essential HTN', 'HTN with dizziness', 'Coronary Artery Disease',
        'CAD post-stent', 'Dyslipidemia and Fatty Liver', 'Metabolic Syndrome'
    ],
    'Respiratory': [
        'Bronchial Asthma exacerbation', 'Astma chronic', 'COPD Grade II', 'Acute Bronchitis',
        'Upper Respiratory Tract Infection (URTI)', 'Allergic Rhinitis and Sinusitis'
    ],
    'Acute / Infectious': [
        'Acute Gastroenteritis with dehydration', 'AGE vomiting and diarrhea', 'Viral pyrexia / fever',
        'Suspected Dengue NS1 positive', 'Enteric Fever (Typhoid)', 'Malaria Vivax',
        'Urinary Tract Infection (UTI)', 'Acute Pharyngitis'
    ],
    'Orthopedic & Musculoskeletal': [
        'Osteoarthritis bilateral knees', 'OA Knees severe', 'Lumbar Disc Prolapse / Sciatica',
        'Chronic lower backache', 'Cervical Spondylosis', 'Right Ankle Ligament Sprain'
    ],
    'Women & Child Health': [
        'Antenatal Care (ANC) 2nd Trimester', 'Normal Pregnancy Routine Check', 'PCOS / PCOD with irregular cycles',
        'Pediatric Bronchiolitis', 'Well Baby immunization visit', 'Failure to thrive infant'
    ],
    'General / Preventive': [
        'Annual Executive Master Health Checkup', 'Routine Pre-employment Screening',
        'General malaise and fatigue', 'Vitamin D / B12 deficiency', 'Mild gastritis / dyspepsia'
    ]
}

ALL_DIAG_CATEGORIES = list(FREE_TEXT_DIAGNOSES.keys())

NUM_PATIENTS = 30000
patient_ids = [f"PAT-{10000 + i}" for i in range(NUM_PATIENTS)]

# Assign patient archetypes:
# 0: Chronic / High-Acuity (elderly, frequent, high spend, higher admission rate) -> ~20%
# 1: Proactive Family / Preventative (frequent OPD/lab, low admission, moderate spend) -> ~25%
# 2: Seasonal / Acute (younger, monsoon surges in Jul-Oct) -> ~30%
# 3: Episodic / Transactional (1-2 visits, low spend, drop-off) -> ~25%
archetypes = np.random.choice([0, 1, 2, 3], size=NUM_PATIENTS, p=[0.20, 0.25, 0.30, 0.25])

# Baseline patient true ages and gender
genders = np.random.choice(['M', 'F'], size=NUM_PATIENTS, p=[0.49, 0.51])
true_ages = np.zeros(NUM_PATIENTS, dtype=int)

for i in range(NUM_PATIENTS):
    arch = archetypes[i]
    if arch == 0:
        true_ages[i] = int(np.clip(np.random.normal(62, 10), 40, 88))
    elif arch == 1:
        true_ages[i] = int(np.clip(np.random.normal(38, 12), 18, 65))
    elif arch == 2:
        true_ages[i] = int(np.clip(np.random.normal(30, 14), 5, 60))
    else:
        true_ages[i] = int(np.clip(np.random.normal(35, 15), 12, 75))

preferred_hospitals = np.random.choice(HOSPITALS, size=NUM_PATIENTS, p=HOSPITAL_PROBS)

print("Simulating OPD Visits (~280,000 rows)...")
# Time span: 2022-01-01 to 2023-12-31 (730 days)
start_date = datetime(2022, 1, 1)

opd_records = []
TARGET_OPD_ROWS = 280000

# Calculate visit distributions per archetype
visit_counts = np.zeros(NUM_PATIENTS, dtype=int)
for i in range(NUM_PATIENTS):
    arch = archetypes[i]
    if arch == 0:
        visit_counts[i] = np.random.negative_binomial(12, 0.5) + 3 # Mean ~15 visits
    elif arch == 1:
        visit_counts[i] = np.random.negative_binomial(8, 0.5) + 2  # Mean ~10 visits
    elif arch == 2:
        visit_counts[i] = np.random.negative_binomial(4, 0.5) + 1  # Mean ~5 visits
    else:
        visit_counts[i] = np.random.choice([1, 2, 3], p=[0.65, 0.25, 0.10]) # Mean ~1.5 visits

# Normalize to around 280,000 total
scale_factor = TARGET_OPD_ROWS / visit_counts.sum()
visit_counts = np.maximum(1, np.round(visit_counts * scale_factor).astype(int))

current_visit_id = 1000000

for i in range(NUM_PATIENTS):
    n_v = visit_counts[i]
    p_id = patient_ids[i]
    arch = archetypes[i]
    p_gender = genders[i]
    t_age = true_ages[i]
    pref_hosp = preferred_hospitals[i]
    
    # Generate noisy age representation
    # 25% DOB format, 10% 'XX yrs', 65% integer
    age_style = np.random.choice(['dob_iso', 'dob_dmy', 'yrs_str', 'int'], p=[0.15, 0.10, 0.10, 0.65])
    birth_year = 2023 - t_age
    birth_month = np.random.randint(1, 13)
    birth_day = np.random.randint(1, 28)
    
    if age_style == 'dob_iso':
        raw_age_val = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
    elif age_style == 'dob_dmy':
        raw_age_val = f"{birth_day:02d}/{birth_month:02d}/{birth_year}"
    elif age_style == 'yrs_str':
        raw_age_val = f"{t_age} yrs"
    else:
        raw_age_val = str(t_age)
        
    for v_idx in range(n_v):
        # Determine visit timing based on archetype (seasonality)
        if arch == 2: # Seasonal Acute (monsoon peak Jul-Oct)
            if np.random.rand() < 0.60:
                # Monsoon months: Jul (day 181/546) to Oct (day 304/669)
                yr_offset = 365 if np.random.rand() < 0.5 else 0
                day_offset = yr_offset + np.random.randint(182, 305)
            else:
                day_offset = np.random.randint(0, 730)
        elif arch == 0: # Chronic regular intervals
            day_offset = int((v_idx / max(1, n_v - 1)) * 710) + np.random.randint(-15, 15)
            day_offset = np.clip(day_offset, 0, 729)
        else:
            day_offset = np.random.randint(0, 730)
            
        v_date = start_date + timedelta(days=int(day_offset), hours=np.random.randint(8, 20), minutes=np.random.randint(0, 60))
        
        # Hospital selection (85% preferred, 15% other clinic)
        hosp = pref_hosp if np.random.rand() < 0.85 else np.random.choice(HOSPITALS)
        
        # Diagnosis & Department selection
        if arch == 0:
            diag_cat = np.random.choice(['Chronic Cardiometabolic', 'Orthopedic & Musculoskeletal', 'General / Preventive'], p=[0.7, 0.2, 0.1])
            dept = np.random.choice(['General Medicine', 'Cardiology', 'Endocrinology', 'Orthopedics'], p=[0.4, 0.3, 0.2, 0.1])
        elif arch == 1:
            diag_cat = np.random.choice(['General / Preventive', 'Women & Child Health', 'Respiratory'], p=[0.5, 0.3, 0.2])
            dept = np.random.choice(['General Medicine', 'Pediatrics', 'Obstetrics & Gynecology', 'Dermatology'], p=[0.4, 0.25, 0.25, 0.1])
        elif arch == 2:
            diag_cat = 'Acute / Infectious'
            dept = np.random.choice(['Emergency / Triage', 'General Medicine', 'Pediatrics'], p=[0.5, 0.3, 0.2])
        else:
            diag_cat = np.random.choice(ALL_DIAG_CATEGORIES)
            dept = np.random.choice(DEPARTMENTS)
            
        diag = np.random.choice(FREE_TEXT_DIAGNOSES[diag_cat])
        doc = np.random.choice(DOCTORS[dept])
        
        rx_count = np.random.poisson(3 if arch == 0 else 2) + 1
        referred_ipd = 1 if (arch == 0 and np.random.rand() < 0.12) or (arch == 2 and np.random.rand() < 0.08) else 0
        
        current_visit_id += 1
        opd_records.append({
            'visit_id': f"OPD-{current_visit_id}",
            'patient_id': p_id,
            'hospital': hosp,
            'visit_date': v_date.strftime('%Y-%m-%d %H:%M:%S'),
            'department': dept,
            'doctor_name': doc,
            'diagnosis_raw': diag,
            'raw_age': raw_age_val,
            'gender': p_gender,
            'prescription_count': rx_count,
            'referred_to_ipd': referred_ipd
        })

df_opd = pd.DataFrame(opd_records)
print(f"Generated OPD Visits: {len(df_opd)} rows. Saving...")
df_opd.to_csv('data/raw/hyderabad_opd_visits.csv', index=False)

# Simulating Inpatient Admissions (~45,000 rows)
print("Simulating Inpatient Admissions (~45,000 rows)...")
admission_records = []
current_adm_id = 500000

# High acuity arch 0 has higher admission probability, arch 2 acute emergency, arch 1 occasional, arch 3 rare
adm_probs = [0.45, 0.12, 0.20, 0.05]
adm_patients = []
for i in range(NUM_PATIENTS):
    arch = archetypes[i]
    if np.random.rand() < adm_probs[arch]:
        adm_patients.append(i)

TARGET_ADM_ROWS = 45000
adm_counts = np.zeros(len(adm_patients), dtype=int)
for idx, p_idx in enumerate(adm_patients):
    arch = archetypes[p_idx]
    if arch == 0:
        adm_counts[idx] = np.random.choice([1, 2, 3, 4, 5], p=[0.40, 0.30, 0.15, 0.10, 0.05])
    else:
        adm_counts[idx] = np.random.choice([1, 2], p=[0.85, 0.15])

scale_factor_adm = TARGET_ADM_ROWS / adm_counts.sum()
adm_counts = np.maximum(1, np.round(adm_counts * scale_factor_adm).astype(int))

WARDS = ['General Ward', 'Semi-Private', 'Deluxe Private', 'ICU / CCU']
WARD_PROBS = [0.45, 0.30, 0.15, 0.10]

for idx, p_idx in enumerate(adm_patients):
    n_adm = adm_counts[idx]
    p_id = patient_ids[p_idx]
    arch = archetypes[p_idx]
    t_age = true_ages[p_idx]
    pref_hosp = preferred_hospitals[p_idx]
    
    # Adm dates
    last_disch = start_date
    for a_idx in range(n_adm):
        current_adm_id += 1
        days_after = np.random.randint(15, 180)
        adm_date = last_disch + timedelta(days=days_after)
        if adm_date >= datetime(2023, 12, 25):
            adm_date = datetime(2023, 12, np.random.randint(1, 20))
            
        # ALOS depends on archetype & ward
        if arch == 0:
            los = int(np.clip(np.random.negative_binomial(6, 0.4) + 3, 2, 28))
            ward = np.random.choice(WARDS, p=[0.30, 0.30, 0.20, 0.20])
            readmission_30d = 1 if np.random.rand() < 0.24 else 0
        elif arch == 2: # Acute infectious (fever/dengue)
            los = int(np.clip(np.random.negative_binomial(4, 0.5) + 2, 1, 10))
            ward = np.random.choice(WARDS, p=[0.55, 0.30, 0.10, 0.05])
            readmission_30d = 1 if np.random.rand() < 0.08 else 0
        else:
            los = int(np.clip(np.random.negative_binomial(3, 0.5) + 2, 1, 8))
            ward = np.random.choice(WARDS, p=WARD_PROBS)
            readmission_30d = 1 if np.random.rand() < 0.05 else 0
            
        disch_date = adm_date + timedelta(days=los)
        last_disch = disch_date
        
        # Outcomes: 92% Discharged, 4% Transferred, 2% LAMA (Left Against Medical Advice), 2% Deceased
        outcome = np.random.choice(['Discharged', 'Transferred', 'LAMA', 'Deceased'], p=[0.93, 0.03, 0.02, 0.02])
        
        diag_category = 'Chronic Cardiometabolic' if arch == 0 else ('Acute / Infectious' if arch == 2 else 'General / Preventive')
        primary_diag = np.random.choice(FREE_TEXT_DIAGNOSES[diag_category])
        
        admission_records.append({
            'admission_id': f"ADM-{current_adm_id}",
            'patient_id': p_id,
            'hospital': pref_hosp if np.random.rand() < 0.9 else np.random.choice(HOSPITALS),
            'admission_date': adm_date.strftime('%Y-%m-%d %H:%M:%S'),
            'discharge_date': disch_date.strftime('%Y-%m-%d %H:%M:%S'),
            'ward': ward,
            'bed_number': f"B-{np.random.randint(101, 350)}",
            'diagnosis_admission': primary_diag,
            'los_days': los,
            'readmission_30d': readmission_30d,
            'outcome': outcome
        })

df_adm = pd.DataFrame(admission_records)
print(f"Generated Admissions: {len(df_adm)} rows. Saving...")
df_adm.to_csv('data/raw/hyderabad_admissions.csv', index=False)

# Simulating Lab Tests (~115,000 rows)
print("Simulating Lab Tests (~115,000 rows)...")
LAB_TESTS = [
    ('Biochemistry', 'HbA1c Glycated Hemoglobin', '%', 4.0, 5.6, 6.5, 14.0),
    ('Biochemistry', 'Fasting Blood Sugar (FBS)', 'mg/dL', 70, 99, 126, 350),
    ('Biochemistry', 'Lipid Profile - Total Cholesterol', 'mg/dL', 125, 200, 201, 380),
    ('Biochemistry', 'Serum Creatinine (KFT)', 'mg/dL', 0.6, 1.2, 1.5, 6.5),
    ('Haematology', 'Complete Blood Count - Hemoglobin', 'g/dL', 12.0, 16.0, 7.0, 11.5),
    ('Haematology', 'Total Leukocyte Count (WBC)', 'cells/cumm', 4000, 11000, 12000, 28000),
    ('Haematology', 'Platelet Count', 'lakhs/cumm', 1.5, 4.5, 0.2, 1.4),
    ('Microbiology', 'Dengue NS1 Antigen Rapid', 'Qualitative', 0, 0, 1, 1),
    ('Microbiology', 'Widal Slide Agglutination (Typhoid)', 'Qualitative', 0, 0, 1, 1),
    ('Pathology', 'Urine Routine & Microscopy', 'Qualitative', 0, 0, 1, 1)
]

TARGET_LAB_ROWS = 115000
lab_records = []
current_lab_id = 700000

# Arch 0 and 1 have more lab tests (monitoring and health checkups)
lab_patients = np.random.choice(range(NUM_PATIENTS), size=TARGET_LAB_ROWS, p=np.where(archetypes==0, 0.40, np.where(archetypes==1, 0.35, np.where(archetypes==2, 0.20, 0.05))) / np.where(archetypes==0, 0.40, np.where(archetypes==1, 0.35, np.where(archetypes==2, 0.20, 0.05))).sum())

for idx in range(TARGET_LAB_ROWS):
    current_lab_id += 1
    p_idx = lab_patients[idx]
    p_id = patient_ids[p_idx]
    arch = archetypes[p_idx]
    pref_hosp = preferred_hospitals[p_idx]
    
    test_meta = random.choice(LAB_TESTS)
    dept, t_name, unit, norm_low, norm_high, abn_low, abn_high = test_meta
    
    # Abnormal result probability depends on archetype
    p_abnormal = 0.45 if arch == 0 else (0.35 if arch == 2 else 0.12)
    is_abnormal = 1 if np.random.rand() < p_abnormal else 0
    
    if unit == 'Qualitative':
        result_val = 'Positive' if is_abnormal else 'Negative'
    else:
        if is_abnormal:
            result_val = str(round(np.random.uniform(abn_low, abn_high), 2))
        else:
            result_val = str(round(np.random.uniform(norm_low, norm_high), 2))
            
    t_date = start_date + timedelta(days=np.random.randint(0, 730), hours=np.random.randint(7, 18))
    
    lab_records.append({
        'test_id': f"LAB-{current_lab_id}",
        'patient_id': p_id,
        'hospital': pref_hosp,
        'test_date': t_date.strftime('%Y-%m-%d %H:%M:%S'),
        'department': dept,
        'test_name': t_name,
        'result_value': result_val,
        'unit': unit,
        'is_abnormal': is_abnormal
    })

df_lab = pd.DataFrame(lab_records)
print(f"Generated Lab Tests: {len(df_lab)} rows. Saving...")
df_lab.to_csv('data/raw/hyderabad_lab_tests.csv', index=False)

# Simulating Billing Records (~60,000 rows) with Double GST Anomaly
print("Simulating Billing Records (~60,000 rows)...")
# Billing arises from admissions (1-2 bills per admission) and high-value OPD/diagnostics packages
billing_records = []
current_bill_id = 900000

# Link bills to admissions
for adm in admission_records:
    current_bill_id += 1
    # Base amount depends on ward and LOS
    ward = adm['ward']
    los = adm['los_days']
    if 'ICU' in ward:
        base_per_day = 12000
    elif 'Deluxe' in ward:
        base_per_day = 6500
    elif 'Semi-Private' in ward:
        base_per_day = 4000
    else:
        base_per_day = 2200
        
    pharm_and_proc = np.random.uniform(3000, 25000)
    base_bill = (los * base_per_day) + pharm_and_proc
    
    # DOUBLE GST ANOMALY EMBEDDED:
    # Proper 18% GST: billed = base * 1.18
    # In ~40% of records, the ERP system bug applied 18% GST twice: base * 1.18 * 1.18 = base * 1.3924!
    has_double_gst = np.random.rand() < 0.40
    if has_double_gst:
        billed_amount = round(base_bill * 1.18 * 1.18, 2)
        gst_reported = round(base_bill * 0.18, 2) # ERP printed 18% on receipt but charged double in total!
    else:
        billed_amount = round(base_bill * 1.18, 2)
        gst_reported = round(base_bill * 0.18, 2)
        
    billing_records.append({
        'bill_id': f"INV-{current_bill_id}",
        'patient_id': adm['patient_id'],
        'admission_id': adm['admission_id'],
        'hospital': adm['hospital'],
        'billing_date': adm['discharge_date'],
        'service_type': f"Inpatient Stay ({ward})",
        'base_charge': round(base_bill, 2),
        'gst_rate_percent': 18.0,
        'gst_amount_itemized': gst_reported,
        'total_billed_amount': billed_amount,
        'payment_status': np.random.choice(['Settled', 'Insurance TPA Paid', 'Partial Pending'], p=[0.70, 0.25, 0.05])
    })

# Add Outpatient Specialized Packages / Executive Health Checks to reach 60,000 bills
REMAINING_BILLS = 60000 - len(billing_records)
opd_bill_patients = np.random.choice(range(NUM_PATIENTS), size=REMAINING_BILLS, p=np.where(archetypes==1, 0.45, np.where(archetypes==0, 0.35, np.where(archetypes==2, 0.15, 0.05))) / np.where(archetypes==1, 0.45, np.where(archetypes==0, 0.35, np.where(archetypes==2, 0.15, 0.05))).sum())

for idx in range(REMAINING_BILLS):
    current_bill_id += 1
    p_idx = opd_bill_patients[idx]
    p_id = patient_ids[p_idx]
    arch = archetypes[p_idx]
    pref_hosp = preferred_hospitals[p_idx]
    
    svc = np.random.choice([
        'Master Health Checkup Package', 'Cardiology ECHO + TMT Consultation',
        'Advanced Diabetic Screening Package', 'MRI / CT Scan Diagnostic Package',
        'Endoscopy / Colonoscopy Day Care'
    ], p=[0.30, 0.25, 0.20, 0.15, 0.10])
    
    base_svc_cost = {
        'Master Health Checkup Package': 4500,
        'Cardiology ECHO + TMT Consultation': 3800,
        'Advanced Diabetic Screening Package': 3200,
        'MRI / CT Scan Diagnostic Package': 7500,
        'Endoscopy / Colonoscopy Day Care': 9000
    }[svc] + np.random.uniform(-300, 800)
    
    has_double_gst = np.random.rand() < 0.40
    if has_double_gst:
        billed_amount = round(base_svc_cost * 1.18 * 1.18, 2)
        gst_reported = round(base_svc_cost * 0.18, 2)
    else:
        billed_amount = round(base_svc_cost * 1.18, 2)
        gst_reported = round(base_svc_cost * 0.18, 2)
        
    b_date = start_date + timedelta(days=np.random.randint(0, 730), hours=np.random.randint(9, 19))
    
    billing_records.append({
        'bill_id': f"INV-{current_bill_id}",
        'patient_id': p_id,
        'admission_id': 'OPD-SERVICE',
        'hospital': pref_hosp,
        'billing_date': b_date.strftime('%Y-%m-%d %H:%M:%S'),
        'service_type': svc,
        'base_charge': round(base_svc_cost, 2),
        'gst_rate_percent': 18.0,
        'gst_amount_itemized': gst_reported,
        'total_billed_amount': billed_amount,
        'payment_status': np.random.choice(['Settled', 'UPI Paid', 'Credit Card'], p=[0.5, 0.3, 0.2])
    })

df_bill = pd.DataFrame(billing_records)
print(f"Generated Billing Records: {len(df_bill)} rows. Saving...")
df_bill.to_csv('data/raw/hyderabad_billing.csv', index=False)

print("\n--- Summary of Generated Datasets ---")
print(f"OPD Visits:     {len(df_opd):,d} rows")
print(f"Admissions:     {len(df_adm):,d} rows")
print(f"Lab Tests:      {len(df_lab):,d} rows")
print(f"Billing:        {len(df_bill):,d} rows")
print(f"TOTAL ROWS:     {len(df_opd) + len(df_adm) + len(df_lab) + len(df_bill):,d} rows!")
