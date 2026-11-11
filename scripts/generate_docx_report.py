"""
Generate Comprehensive Word (.docx) Project Report
Title: Patient Segmentation Strategy Report - Hyderabad Community Clinic Network
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles & Colors
    NAVY = RGBColor(16, 44, 87)
    TEAL = RGBColor(14, 131, 136)
    CORAL = RGBColor(218, 73, 73)
    DARK_GRAY = RGBColor(50, 50, 50)
    
    # -------------------------------------------------------------
    # COVER / TITLE BLOCK
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(20)
    title_p.paragraph_format.space_after = Pt(6)
    r_tag = title_p.add_run("HYDERABAD COMMUNITY CLINIC NETWORK")
    r_tag.font.size = Pt(12)
    r_tag.font.bold = True
    r_tag.font.color.rgb = TEAL
    
    t_run = title_p.add_run("\nSTRATEGIC PATIENT SEGMENTATION REPORT")
    t_run.font.size = Pt(26)
    t_run.font.bold = True
    t_run.font.color.rgb = NAVY
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(24)
    sub_run = sub_p.add_run("Data-Driven Resource Allocation, Clinical Optimization, and Revenue Protection Across 4 Hospitals (501,690 Records)")
    sub_run.font.size = Pt(14)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(100, 116, 139)
    
    # Metadata Box
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    meta_data = [
        ("Prepared For:", "Managing Director, Head of Clinical Operations & Network Management"),
        ("Prepared By:", "Lead Healthcare Data Analytics & Clinical Strategy Team"),
        ("Hospitals Covered:", "Banjara Hills, HITEC City, Secunderabad, Kukatpally"),
        ("Date & Version:", "November 2026 | Comprehensive Technical & Business Report (v1.0)")
    ]
    
    for r_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[r_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.2)
        cell_v.width = Inches(4.3)
        set_cell_background(cell_k, "F1F5F9")
        set_cell_background(cell_v, "F8FAFC")
        set_cell_margins(cell_k)
        set_cell_margins(cell_v)
        
        pk = cell_k.paragraphs[0]
        rk = pk.add_run(k)
        rk.font.bold = True
        rk.font.size = Pt(10)
        rk.font.color.rgb = NAVY
        
        pv = cell_v.paragraphs[0]
        rv = pv.add_run(v)
        rv.font.size = Pt(10)
        rv.font.color.rgb = DARK_GRAY
        
    doc.add_paragraph().paragraph_format.space_after = Pt(20)
    
    # -------------------------------------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------------------------------------
    h1 = doc.add_heading("Executive Summary", level=1)
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(8)
    h1.runs[0].font.color.rgb = NAVY
    
    p = doc.add_paragraph()
    p.add_run("The Hyderabad Network of Community Clinics encompasses 4 primary tertiary and outpatient facilities (Banjara Hills Medical Centre, HITEC City Community Hospital, Secunderabad Care Clinic, and Kukatpally Health Hub). Historically, clinic leadership operated under a ").font.size = Pt(11)
    r_b = p.add_run("uniform treatment paradigm")
    r_b.font.bold = True
    p.add_run("—allocating identical physician consultation slots, clinical triage pathways, and administrative overhead across all patients regardless of clinical acuity or lifetime engagement.").font.size = Pt(11)
    
    p2 = doc.add_paragraph()
    p2.add_run("This one-size-fits-all operational model created severe organizational friction:\n").font.size = Pt(11)
    bullets_exec = [
        "Wasted Clinical Capacity on Low-Value Walk-ins: Senior specialist physicians routinely expended 15-minute consultations on minor, 1-off episodic issues that could be resolved digitally or via nurse triage.",
        "Under-Servicing High-Risk Chronic Cohorts: Patients with multi-morbid cardiometabolic disorders received insufficient structured post-discharge care, driving an unsustainable 15.0% 30-day inpatient readmission rate.",
        "Monsoon Outpatient Paralysis: Hyderabad's annual July-October monsoon rains triggered massive outbreaks of dengue, typhoid, and acute gastroenteritis, paralyzing emergency rooms and clinic outpatient departments.",
        "Compounded Billing Distortions: An undetected ERP calculation bug double-counted 18% GST across 39.8% of billing invoices, distorting financial accounts receivable by ₹ 24.85 Crore."
    ]
    for b in bullets_exec:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        run = bp.add_run(b)
        run.font.size = Pt(10.5)
        
    p3 = doc.add_paragraph()
    p3.add_run("By forensically cleaning and modeling ").font.size = Pt(11)
    p3.add_run("501,690 transactional records").bold = True
    p3.add_run(" using multi-dimensional K-Means clustering (validated against traditional RFM scoring), we segmented the 30,000 unique patient population into ").font.size = Pt(11)
    p3.add_run("4 distinct, operationally viable segments").bold = True
    p3.add_run(". Each segment strictly exceeds the 5% population threshold, exhibits statistically significant differentiation across all core clinical and financial KPIs (ANOVA p < 0.001), and maps to a concrete operational initiative delivering an estimated ").font.size = Pt(11)
    p3.add_run("₹ 2.70 Crore in annual net financial benefit with a 391% ROI").bold = True
    p3.add_run(".")
    
    # -------------------------------------------------------------
    # SECTION 1: DATA ARCHITECTURE & FORENSIC AUDIT
    # -------------------------------------------------------------
    h1 = doc.add_heading("1. Data Architecture & Forensic Quality Audit", level=1)
    h1.runs[0].font.color.rgb = NAVY
    
    doc.add_paragraph("The enterprise health data ecosystem comprises four relational tables totaling 501,690 rows across the 2022-2023 calendar years:").runs[0].font.size = Pt(11)
    
    data_summary = [
        ("Outpatient (OPD) Consultations", "280,970 records", "Contains patient demographics, appointment dates, departments, consulting doctors, raw age strings, and unstructured clinical diagnoses."),
        ("Inpatient (IPD) Admissions", "45,720 records", "Tracks hospital stays, admission/discharge timestamps, ward types (General, Semi-Private, Deluxe, ICU), bed numbers, ALOS, 30-day readmissions, and clinical outcomes."),
        ("Laboratory Diagnostics", "115,000 records", "Diagnostic test orders across Biochemistry, Haematology, Microbiology, and Pathology, recording test names, quantitative/qualitative values, units, and abnormality flags."),
        ("Billing & Revenue Records", "60,000 records", "Itemized hospital charges, service categories, base fees, reported GST, gross invoice amounts, and settlement statuses.")
    ]
    
    t_data = doc.add_table(rows=len(data_summary)+1, cols=3)
    t_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_data.autofit = False
    
    t_headers = ["Transactional Table", "Volume (Rows)", "Core Functional Scope"]
    for c_idx, h_text in enumerate(t_headers):
        cell = t_data.cell(0, c_idx)
        set_cell_background(cell, "102C57")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    t_widths = [Inches(2.2), Inches(1.3), Inches(3.0)]
    for r_idx, (tbl_name, vol, scope) in enumerate(data_summary):
        row = t_data.rows[r_idx + 1]
        for c_idx, (val, w) in enumerate(zip([tbl_name, vol, scope], t_widths)):
            cell = row.cells[c_idx]
            cell.width = w
            set_cell_background(cell, "FFFFFF" if r_idx % 2 == 0 else "F8FAFC")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            r.font.color.rgb = DARK_GRAY
            if c_idx == 0: r.font.bold = True
            
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    h2 = doc.add_heading("Forensic Resolution of Real-World Data Anomalies", level=2)
    h2.runs[0].font.color.rgb = TEAL
    
    anomalies = [
        ("Rectification of Double-Counted GST Billing Bug:", "Analysis of the billing system identified an ERP taxation routine error where 18% GST was compounded twice on hospital invoices: Total Billed = Base Charge × 1.18 × 1.18 = Base Charge × 1.3924. This error was detected in exactly 23,894 invoices (39.8% of all billing transactions). The pipeline flagged each affected invoice and recalculated true net revenue as Total Billed / 1.18. This audit eliminated ₹ 24,85,09,288.97 (₹ 24.85 Crore) in fictitious accounts-receivable overstatement."),
        ("Standardization of Free-Text Clinical Diagnoses:", "EHR records contained highly unstructured free-text entries riddled with abbreviations, typos, and mixed case (e.g., 'T2DM uncontrolled', 'diabtes type 2', 'DM-II with neuropathy', 'HTN with mild chest pain', 'viral fever / suspected Dengue'). A clinical regex taxonomy engine was developed to map all 280,000+ OPD and IPD diagnosis strings into 6 standardized diagnostic categories: Cardiometabolic (Diabetes), Cardiovascular & Metabolic, Respiratory, Acute Infectious / GI, Orthopedic & Musculoskeletal, Maternal & Child Health, and Preventive & Wellness."),
        ("Standardization of Dirty Age & Date-of-Birth Entries:", "Approximately 25% of patient records had full date-of-birth timestamps stored in the age field in mixed ISO ('1985-04-12') and DMY ('12/05/1972') formats, while 10% contained string suffixes ('45 yrs', '62 Y'). A multi-pattern parser resolved all records into exact numerical ages relative to reference year 2023, yielding a clean distribution ranging from 5 to 88 years with a median of 46.0 years.")
    ]
    for title, desc in anomalies:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r_t = p.add_run(f"• {title} ")
        r_t.font.bold = True
        r_t.font.size = Pt(10.5)
        r_t.font.color.rgb = NAVY
        r_d = p.add_run(desc)
        r_d.font.size = Pt(10.5)
        r_d.font.color.rgb = DARK_GRAY
        
    # -------------------------------------------------------------
    # SECTION 2: FEATURE ENGINEERING
    # -------------------------------------------------------------
    h1 = doc.add_heading("2. Behavioral & Clinical Feature Engineering", level=1)
    h1.runs[0].font.color.rgb = NAVY
    
    doc.add_paragraph("To capture both commercial engagement and hospital operational impact, the transactional records were aggregated into an analytical feature store at the individual patient entity level (30,000 unique patients):").runs[0].font.size = Pt(11)
    
    features_list = [
        ("Recency (days):", "Days elapsed from the patient's latest clinical touchpoint (OPD, admission, lab, billing) to December 31, 2023. Identifies active vs. dormant patients."),
        ("Frequency (encounters):", "Total cumulative touchpoints across outpatient visits, inpatient admissions, and diagnostic lab test orders."),
        ("Monetary Value (₹):", "Total net revenue generated per patient after rectifying the double-GST billing error."),
        ("Growth Trajectory (YoY):", "Trend in patient visit frequency from Period 1 (2022) to Period 2 (2023), computed as (Visits_2023 - Visits_2022) / (Visits_2022 + 1)."),
        ("Seasonality Concentration Index:", "Proportion of visits occurring during Hyderabad's intense monsoon season (July to October), exposing vulnerability to seasonal epidemics."),
        ("Average Length of Stay (ALOS):", "Mean inpatient days per hospital admission. Directly correlates with inpatient bed resource consumption."),
        ("30-Day Hospital Readmission Rate:", "Ratio of unplanned inpatient admissions occurring within 30 days of previous discharge."),
        ("Clinical Acuity Score:", "Composite weighted clinical risk index combining inpatient stays (weight 3.0), ICU admissions (5.0), abnormal lab diagnostic results (1.5), and prescription intensity (0.1).")
    ]
    for fname, fdesc in features_list:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        rf = p.add_run(f"{fname} ")
        rf.bold = True
        rf.font.size = Pt(10)
        rd = p.add_run(fdesc)
        rd.font.size = Pt(10)
        
    p_skew = doc.add_paragraph()
    p_skew.paragraph_format.space_before = Pt(8)
    p_skew.add_run("Skewness Handling & Outlier Winsorization: ").bold = True
    p_skew.add_run("Healthcare financial and clinical metrics exhibit extreme positive skewness (Monetary Skew = 4.22, Clinical Acuity Skew = 3.18, Recency Skew = 2.51). Logarithmic transformations (log(1 + x)) were applied to compress heavy tails. Furthermore, extreme outliers were winsorized at the 99.5th percentile to prevent high-cost outlier surgeries from distorting Euclidean distance calculations in cluster modeling.").font.size = Pt(10.5)
    
    # -------------------------------------------------------------
    # SECTION 3: METHODOLOGY EVALUATION
    # -------------------------------------------------------------
    h1 = doc.add_heading("3. Methodology Evaluation: RFM Scoring vs Multi-Dimensional K-Means", level=1)
    h1.runs[0].font.color.rgb = NAVY
    
    doc.add_paragraph("A core objective of this project was to critically evaluate traditional RFM (Recency, Frequency, Monetary) quintile scoring against unsupervised Multi-Dimensional K-Means clustering.").runs[0].font.size = Pt(11)
    
    if os.path.exists('outputs/charts/elbow_and_silhouette_analysis.png'):
        doc.add_picture('outputs/charts/elbow_and_silhouette_analysis.png', width=Inches(6.2))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_run = cap.add_run("Figure 1: Elbow Method (Inertia WCSS) and Silhouette Score Analysis (k = 2 to 7)")
        cap_run.font.size = Pt(9)
        cap_run.font.italic = True
        
    doc.add_paragraph("Why Traditional RFM Scoring Fails Healthcare Operations:").runs[0].font.bold = True
    rfm_critique = [
        "Clinical Risk Blindness: RFM evaluates only transaction timing, frequency, and spend. An individual visiting 6 times for cosmetic skin consultations receives the identical score (F=4, M=4) as an elderly diabetic patient admitted for acute ketoacidosis and 5 emergency reviews.",
        "Inpatient Capacity Invisibility: Hospital operating margins and capacity constraints are dictated by Average Length of Stay (ALOS) and bed occupancy. RFM is fundamentally blind to whether a patient occupied an ICU bed for 10 days or attended a 15-minute OPD consultation.",
        "Epidemiological Seasonality Blindness: Hyderabad clinics experience massive July-October surges in dengue and viral pyrexia. RFM treats visits in dry summer months identically to monsoon spikes, failing to support seasonal clinical staffing models."
    ]
    for rc in rfm_critique:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.add_run(rc).font.size = Pt(10)
        
    doc.add_paragraph("Why Multi-Dimensional K-Means Clustering Won:").runs[0].font.bold = True
    doc.add_paragraph("By scaling log(Monetary), log(Frequency), log(Recency), Growth Rate, Seasonality Index, Clinical Acuity, and ALOS via StandardScaler, K-Means minimizes within-cluster variance across both financial and clinical dimensions. Silhouette analysis identified an optimal inflection point at k=4 (Silhouette Score = 0.3305, Inertia = 82,418.1), establishing four robust cohorts that satisfy the >= 5% population requirement and provide distinct operational workflows.").runs[0].font.size = Pt(10.5)
    
    # -------------------------------------------------------------
    # SECTION 4: SEGMENT PROFILES
    # -------------------------------------------------------------
    h1 = doc.add_heading("4. Comprehensive Segment Profiles & Clinical Benchmarking", level=1)
    h1.runs[0].font.color.rgb = NAVY
    
    doc.add_paragraph("The 30,000 patients were segmented into 4 business-friendly cohorts. The table below outlines their volume, financial contribution, and clinical resource consumption:").runs[0].font.size = Pt(11)
    
    profile_headers = ["Segment Name", "Patients", "Share %", "Net Revenue", "Avg Visits", "ALOS", "30d Readm", "Bed-Days %"]
    profile_rows = [
        ["High-Acuity Chronic Inpatients", "5,627", "18.8%", "₹ 344.9 Cr (94.1%)", "22.1 visits", "8.53 days", "15.0%", "99.3%"],
        ["Proactive Wellness & Loyalists", "11,234", "37.5%", "₹ 16.7 Cr (4.6%)", "15.3 visits", "0.04 days", "0.0%", "0.3%"],
        ["Seasonal Acute Outpatients", "8,011", "26.7%", "₹ 4.0 Cr (1.1%)", "5.4 visits", "0.02 days", "0.0%", "0.3%"],
        ["Transactional Minor Walk-ins", "5,128", "17.1%", "₹ 0.9 Cr (0.2%)", "2.5 visits", "0.00 days", "0.0%", "0.1%"]
    ]
    
    t_prof = doc.add_table(rows=len(profile_rows)+1, cols=len(profile_headers))
    t_prof.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_prof.autofit = False
    
    col_w = [Inches(2.1), Inches(0.7), Inches(0.6), Inches(1.3), Inches(0.8), Inches(0.7), Inches(0.7), Inches(0.8)]
    for c_idx, h_text in enumerate(profile_headers):
        cell = t_prof.cell(0, c_idx)
        cell.width = col_w[c_idx]
        set_cell_background(cell, "102C57")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_idx, r_data in enumerate(profile_rows):
        row = t_prof.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = col_w[c_idx]
            set_cell_background(cell, "FFFFFF" if r_idx % 2 == 0 else "F1F5F9")
            set_cell_margins(cell, top=90, bottom=90, left=90, right=90)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            r.font.color.rgb = DARK_GRAY
            if c_idx == 0: r.font.bold = True
            
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    if os.path.exists('outputs/charts/segment_size_and_revenue_share.png'):
        doc.add_picture('outputs/charts/segment_size_and_revenue_share.png', width=Inches(5.8))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.add_run("Figure 2: Patient Base Share vs Net Revenue Share by Segment").font.size = Pt(9)
        
    if os.path.exists('outputs/charts/clinical_kpi_profile_bars.png'):
        doc.add_picture('outputs/charts/clinical_kpi_profile_bars.png', width=Inches(6.2))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.add_run("Figure 3: Core Clinical Benchmarks: ALOS, Bed Occupancy Share, and 30-Day Readmission Rate").font.size = Pt(9)
        
    h2 = doc.add_heading("Statistical Validation Across Core KPIs", level=2)
    h2.runs[0].font.color.rgb = TEAL
    
    doc.add_paragraph("To confirm that segments are not statistical artifacts, both parametric One-Way ANOVA and non-parametric Kruskal-Wallis tests were executed:").runs[0].font.size = Pt(10.5)
    
    stat_data = [
        ("Annual Net Revenue (₹)", "9,226.28", "0.00e+00", "23,338.81", "0.00e+00", "Yes (p < 0.001)"),
        ("Visit Frequency", "13,206.62", "0.00e+00", "21,135.09", "0.00e+00", "Yes (p < 0.001)"),
        ("Average Length of Stay (ALOS)", "46,518.83", "0.00e+00", "28,933.74", "0.00e+00", "Yes (p < 0.001)"),
        ("30-Day Readmission Rate", "7,400.59", "0.00e+00", "16,026.97", "0.00e+00", "Yes (p < 0.001)"),
        ("Seasonality Index", "19,873.86", "0.00e+00", "19,227.03", "0.00e+00", "Yes (p < 0.001)")
    ]
    
    t_stat = doc.add_table(rows=len(stat_data)+1, cols=6)
    t_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_stat.autofit = False
    
    s_headers = ["Core Clinical / Financial KPI", "ANOVA F", "ANOVA p", "Kruskal H", "Kruskal p", "Significant?"]
    for c_idx, h_text in enumerate(s_headers):
        cell = t_stat.cell(0, c_idx)
        set_cell_background(cell, "102C57")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_idx, r_data in enumerate(stat_data):
        row = t_stat.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            set_cell_background(cell, "FFFFFF" if r_idx % 2 == 0 else "F8FAFC")
            set_cell_margins(cell, top=70, bottom=70, left=70, right=70)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            r.font.color.rgb = DARK_GRAY
            if c_idx == 0: r.font.bold = True
            
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # -------------------------------------------------------------
    # SECTION 5: CONCRETE ACTIONS & ROI
    # -------------------------------------------------------------
    h1 = doc.add_heading("5. Strategic Action Plans, Cost Estimates & Financial ROI", level=1)
    h1.runs[0].font.color.rgb = NAVY
    
    doc.add_paragraph("A distinct operational and financial intervention was designed for each segment, complete with cost modeling, projected benefit, and measurable targets:").runs[0].font.size = Pt(11)
    
    actions_desc = [
        ("High-Acuity Chronic Inpatients: Post-Discharge Navigation & Tele-Monitoring",
         "Operational Action: Station 4 dedicated Nurse Navigators across Banjara Hills and HITEC City to lead a structured 30-day post-discharge protocol, distribute remote cellular blood pressure/glucose monitors, and execute medication reconciliation.\n"
         "• Annual Cost: ₹ 28,00,000 (Navigator salaries + cellular tele-kit software licenses)\n"
         "• Expected Benefit: ₹ 1,12,00,000 (Prevents 250 penalty bed-readmissions and unblocks high-margin ICU beds for elective surgeries)\n"
         "• Net Projected ROI: 300% Net ROI (4.0x payoff)\n"
         "• Measurable KPI Target: Reduce 30-day readmissions from 15.0% to < 10.0% and shorten ALOS by 1.2 days within 9 months."),
        
        ("Proactive Wellness & Family Loyalists: 'Hyderabad Arogya Family Shield' Subscription",
         "Operational Action: Launch an annual family subscription package bundling bi-annual executive health diagnostics, priority outpatient booking, and 24/7 pediatric tele-triage access.\n"
         "• Annual Cost: ₹ 15,00,000 (Mobile app portal, patient onboarding, customer success)\n"
         "• Expected Benefit: ₹ 72,00,000 (Increases preventative package sales by 40% and boosts retention by 28%)\n"
         "• Net Projected ROI: 380% Net ROI (4.8x payoff)\n"
         "• Measurable KPI Target: Enroll 3,500 families in Year 1; achieve +₹ 1,800 increase in annual spend per family."),
        
        ("Seasonal Acute Outpatients: Monsoon Rapid-Triage Pods & Fever Fast-Tracks",
         "Operational Action: Erect temporary rapid-triage fever pods at HITEC City and Secunderabad clinics during the July-October monsoon surge, equipped with Dengue NS1 rapid tests, hydration stations, and pre-packaged fever pharmacotherapy packs.\n"
         "• Annual Cost: ₹ 18,00,000 (Seasonal temporary nursing staff + rapid antigen test inventory)\n"
         "• Expected Benefit: ₹ 54,00,000 (Captures 35% more acute seasonal footfall; converts 15% to long-term wellness checks)\n"
         "• Net Projected ROI: 200% Net ROI (3.0x payoff)\n"
         "• Measurable KPI Target: Cut triage wait times by 45% (from 55m to 18m); capture 4,200 additional acute patient visits."),
        
        ("Transactional Minor Walk-ins: WhatsApp Self-Service Bot & Automated Counters",
         "Operational Action: Introduce a multilingual WhatsApp business chatbot for self-service appointment scheduling, digital lab report delivery, and UPI self-checkout to eliminate front-desk bottlenecks.\n"
         "• Annual Cost: ₹ 8,00,000 (WhatsApp API integration + self-service digital kiosks)\n"
         "• Expected Benefit: ₹ 32,00,000 (Saves 600 hours clerical labor; lifts 2nd-visit conversion from 12% to 26%)\n"
         "• Net Projected ROI: 300% Net ROI (4.0x payoff)\n"
         "• Measurable KPI Target: Shift 65% of bookings to WhatsApp; convert 2,000 one-off walk-ins into repeat registered patients.")
    ]
    for atitle, abody in actions_desc:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(4)
        rt = p.add_run(f"• {atitle}\n")
        rt.bold = True
        rt.font.size = Pt(10.5)
        rt.font.color.rgb = NAVY
        rb = p.add_run(abody)
        rb.font.size = Pt(10)
        rb.font.color.rgb = DARK_GRAY
        
    p_tot = doc.add_paragraph()
    p_tot.paragraph_format.space_before = Pt(8)
    set_cell_background(doc.add_table(rows=1, cols=1).cell(0, 0), "E2F1E7")
    
    # -------------------------------------------------------------
    # SECTION 6: STRETCH REQUIREMENT - STABILITY & MIGRATION
    # -------------------------------------------------------------
    h1 = doc.add_heading("6. Stretch Requirement: 2-Year Segment Stability & Migration", level=1)
    h1.runs[0].font.color.rgb = NAVY
    
    doc.add_paragraph("To evaluate temporal stability, the feature engineering and segmentation pipeline was executed independently across Period 1 (2022) and Period 2 (2023). Tracking patient movements between periods yielded an overall stability rate of 56.5%:").runs[0].font.size = Pt(11)
    
    if os.path.exists('outputs/charts/segment_migration_matrix_heatmap.png'):
        doc.add_picture('outputs/charts/segment_migration_matrix_heatmap.png', width=Inches(5.8))
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.add_run("Figure 4: 2-Year Segment Migration Matrix Heatmap (Period 1 2022 vs Period 2 2023)").font.size = Pt(9)
        
    mig_observations = [
        ("High-Acuity Chronic Inpatients Retain 88.1% Stability:", "Once a patient is admitted for complex inpatient care, institutional retention is extraordinarily sticky. This segment represents the network's financial core and warrants dedicated nurse navigator investments to prevent post-discharge readmission penalties."),
        ("Transactional Walk-ins Suffer 25.2% Churn/Dormancy:", "Over a quarter of episodic walk-ins never return to the network in Year 2. Deploying automated WhatsApp outreach and follow-up lab notifications directly addresses this customer leakage."),
        ("Seasonal Acute Outpatients Migrate Volatily (33.3% to Walk-ins):", "Patients entering the network solely during monsoon disease outbreaks frequently revert to single-visit walk-ins or dormancy in drier years. Converting them into the 'Hyderabad Arogya Family Shield' plan creates recurring year-round clinical engagement.")
    ]
    for mtitle, mdesc in mig_observations:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        rt = p.add_run(f"• {mtitle} ")
        rt.bold = True
        rt.font.size = Pt(10)
        rt.font.color.rgb = NAVY
        rd = p.add_run(mdesc)
        rd.font.size = Pt(10)
        
    # -------------------------------------------------------------
    # SECTION 7: IMPLEMENTATION ROADMAP
    # -------------------------------------------------------------
    h1 = doc.add_heading("7. Executive Implementation Roadmap & Governance", level=1)
    h1.runs[0].font.color.rgb = NAVY
    
    roadmap_steps = [
        ("Phase 1: Immediate Controls (Months 1 - 3)",
         "1. Deploy ERP software patch to permanently stop double-counting 18% GST across all 4 hospital billing systems.\n"
         "2. Mandate ICD-10 standardized diagnostic dropdown selectors in the outpatient EMR to eliminate free-text ambiguities.\n"
         "3. Launch WhatsApp Self-Service Bot for automated appointment scheduling, lab PDF delivery, and digital payments."),
        
        ("Phase 2: Clinical Optimization & Care Navigation (Months 4 - 6)",
         "1. Recruit and station 4 Nurse Navigators across Banjara Hills and HITEC City hospitals.\n"
         "2. Procure cellular-connected blood pressure and glucometer kits for post-acute discharge distribution.\n"
         "3. Institute an inpatient bed reservation protocol adjusting ward allocations based on predicted segment ALOS."),
        
        ("Phase 3: Revenue Scaling & Monsoon Preparedness (Months 7 - 12)",
         "1. Roll out the 'Hyderabad Arogya Family Shield' subscription targeting 11,000+ loyal patient households.\n"
         "2. Erect rapid-triage fever pods ahead of the July monsoon surge at HITEC City and Secunderabad clinics.\n"
         "3. Monitor quarterly segment migration KPIs to realize the full ₹ 2.70 Crore annual net benefit.")
    ]
    for rtitle, rbody in roadmap_steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(4)
        rt = p.add_run(f"{rtitle}\n")
        rt.bold = True
        rt.font.size = Pt(10.5)
        rt.font.color.rgb = TEAL
        rb = p.add_run(rbody)
        rb.font.size = Pt(10)
        rb.font.color.rgb = DARK_GRAY
        
    doc_path = "Presentation/Patient_Segmentation_Project_Report.docx"
    doc.save(doc_path)
    print(f"Project report successfully created at: {doc_path}")

create_report()
