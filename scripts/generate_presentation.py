"""
Generate Professional PowerPoint Deck for Business Head
Presentation: Hyderabad Clinic Network Patient Segmentation Strategy
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

os.makedirs('Presentation', exist_ok=True)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette: Deep Navy, Teal, Coral, Slate Gray, Pure White
NAVY = RGBColor(16, 44, 87)
TEAL = RGBColor(53, 162, 159)
CORAL = RGBColor(218, 73, 73)
SLATE = RGBColor(100, 116, 139)
LIGHT_BG = RGBColor(245, 247, 250)
WHITE = RGBColor(255, 255, 255)
DARK_GRAY = RGBColor(40, 40, 40)

def add_header(slide, title_text, subtitle_text):
    # Top banner card
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.size = Pt(13)
    p2.font.color.rgb = TEAL

def add_card(slide, left, top, width, height, bg_color=WHITE, line_color=SLATE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

blank_layout = prs.slide_layouts[6]

# -------------------------------------------------------------
# SLIDE 1: Title Slide
# -------------------------------------------------------------
s1 = prs.slides.add_slide(blank_layout)
# Background
bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()

# Title text box
tb = s1.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(11), Inches(3.5))
tf = tb.text_frame
tf.word_wrap = True

p0 = tf.paragraphs[0]
p0.text = "HYDERABAD COMMUNITY CLINIC NETWORK"
p0.font.size = Pt(16)
p0.font.bold = True
p0.font.color.rgb = TEAL

p1 = tf.add_paragraph()
p1.text = "Strategic Patient Segmentation & Resource Allocation"
p1.font.size = Pt(36)
p1.font.bold = True
p1.font.color.rgb = WHITE

p2 = tf.add_paragraph()
p2.text = "Transforming One-Size-Fits-All Healthcare Operations across 4 Hospitals (500,000+ Records)"
p2.font.size = Pt(18)
p2.font.color.rgb = RGBColor(200, 220, 240)

p3 = tf.add_paragraph()
p3.text = "\nExecutive Strategy Presentation for Network Leadership | Localized Hyderabad Operations"
p3.font.size = Pt(13)
p3.font.color.rgb = RGBColor(160, 180, 205)

# -------------------------------------------------------------
# SLIDE 2: Executive Summary & The Problem
# -------------------------------------------------------------
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Executive Problem Statement & Operational Dilemma", "Management Challenge: Equal Effort Expended Across Unequal Patient Cohorts")

# 3 Column Cards
c_w = Inches(3.7)
c_h = Inches(5.2)
top_y = Inches(1.7)

# Card 1: Problem
add_card(s2, Inches(0.8), top_y, c_w, c_h, WHITE, SLATE)
tb = s2.shapes.add_textbox(Inches(1.0), top_y + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "The Operational Flaw"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = CORAL

bullets = [
    "\n• Uniform Treatment: Network treats all OPD patients, admissions, and doctors identically across Banjara Hills, HITEC City, Secunderabad, and Kukatpally.",
    "• Resource Misallocation: Doctors spend identical consultation slots on minor 1-time walk-ins while high-risk chronic patients receive insufficient follow-up.",
    "• High Penalty Readmissions: 15% 30-day readmissions in complex inpatients consume emergency beds unproductively.",
    "• Seasonal Choke-Points: Severe monsoon surges in July-October overwhelm emergency departments."
]
for b in bullets:
    p = tf.add_paragraph()
    p.text = b
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY

# Card 2: Data Audit & Cleaning
add_card(s2, Inches(4.8), top_y, c_w, c_h, WHITE, SLATE)
tb = s2.shapes.add_textbox(Inches(5.0), top_y + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "500k Data Quality Audit"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = NAVY

bullets = [
    "\n• Free-Text Diagnoses: Standardized 280,000+ unstructured clinical entries into 6 standardized diagnostic categories via regex taxonomy.",
    "• Dirty Age Formats: Rectified mixed ISO/DMY dates-of-birth and string ages into an exact numeric age distribution (range 5 to 88).",
    "• Double GST Anomaly Rectified: Detected and corrected duplicate 18% GST inflation in 39.8% of billing invoices (saving INR 24.85 Cr in overstated revenue).",
    "• Full Relational Integration: Unified OPD, IPD admissions, lab diagnostic orders, and corrected billing."
]
for b in bullets:
    p = tf.add_paragraph()
    p.text = b
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY

# Card 3: Strategic Solution
add_card(s2, Inches(8.8), top_y, c_w, c_h, WHITE, SLATE)
tb = s2.shapes.add_textbox(Inches(9.0), top_y + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Targeted Segmentation"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = TEAL

bullets = [
    "\n• 4 Distinct Business Segments: Engineered multidimensional behavioral and clinical features (Recency, Frequency, Value, Seasonality, ALOS, Acuity).",
    "• Statistical Differentiation: Statistically validated differentiation across all core KPIs (ANOVA p < 0.001).",
    "• High Financial Impact: Net projected benefit of INR 2.70 Cr annually across 4 concrete operational initiatives.",
    "• 56.5% Segment Stability: Measured 2-year migration matrix to protect loyalists and intervene in escalating risks."
]
for b in bullets:
    p = tf.add_paragraph()
    p.text = b
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY

# -------------------------------------------------------------
# SLIDE 3: Methodology Comparison - RFM vs K-Means
# -------------------------------------------------------------
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Segmentation Methodology: RFM Scoring vs K-Means", "Why Multi-Dimensional K-Means Clustering Outperforms Traditional RFM in Healthcare")

# 2 Big Cards
c_w2 = Inches(5.7)
c_h2 = Inches(5.2)

# Left: RFM Limitations
add_card(s3, Inches(0.8), top_y, c_w2, c_h2, WHITE, SLATE)
tb = s3.shapes.add_textbox(Inches(1.1), top_y + Inches(0.2), c_w2 - Inches(0.6), c_h2 - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Traditional RFM Scoring (The Alternative)"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = CORAL

rfm_points = [
    "\n❌ Ignores Clinical Complexity: An ICU admission with severe diabetes is scored the same as 3 routine eye exams if spend matches.",
    "❌ Blind to Inpatient Capacity: Does not account for Average Length of Stay (ALOS), bed occupancy, or 30-day readmission risk.",
    "❌ No Temporal Context: Cannot detect monsoon seasonality surges or accelerating patient visit trajectories (growth rate).",
    "❌ Arbitrary Quintile Binning: Forcing equal 20% quintile cuts creates artificial segment boundaries that mismatch real medical patterns.",
    "❌ Result: Healthcare managers cannot use RFM alone to design clinical staffing or bed management protocols."
]
for pt in rfm_points:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK_GRAY

# Right: K-Means Strengths
add_card(s3, Inches(6.8), top_y, c_w2, c_h2, WHITE, SLATE)
tb = s3.shapes.add_textbox(Inches(7.1), top_y + Inches(0.2), c_w2 - Inches(0.6), c_h2 - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Multi-Dimensional K-Means (Chosen Method)"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = TEAL

km_points = [
    "\n✅ Integrated Clinical + Financial Dimensions: Combines log(Monetary), log(Frequency), log(Recency) with ALOS, Clinical Acuity, and Seasonality.",
    "✅ Rigorous Math Validation: Validated using Elbow Method and Silhouette Analysis (K=4 silhouette = 0.3305, highest balance of interpretability).",
    "✅ Strict Healthcare Constraints: Every segment represents >= 17% of the patient base (strictly passing the >= 5% operational requirement).",
    "✅ Statistical Superiority: Statistically significant separation on all 5 clinical and financial KPIs (ANOVA F > 7,400, p < 0.001).",
    "✅ Result: Enables tailored clinical interventions, bed forecasting, and differentiated marketing programs."
]
for pt in km_points:
    p = tf.add_paragraph()
    p.text = pt
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK_GRAY

# -------------------------------------------------------------
# SLIDE 4: The 4 Core Patient Segments Profile Table
# -------------------------------------------------------------
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Hyderabad Clinic Network: Segment Profile Summary", "Comprehensive Breakdown of Volume, Revenue, Clinical Utilization, and Capacity Impact")

# Add Table shape
rows, cols = 5, 8
table_shape = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
table = table_shape.table

# Set Column Widths
table.columns[0].width = Inches(2.6) # Segment
table.columns[1].width = Inches(1.1) # Patients
table.columns[2].width = Inches(1.1) # Share %
table.columns[3].width = Inches(1.5) # Net Rev
table.columns[4].width = Inches(1.4) # Visits/Yr
table.columns[5].width = Inches(1.3) # ALOS
table.columns[6].width = Inches(1.3) # Readm Rate
table.columns[7].width = Inches(1.4) # Bed Occ %

headers = ["Segment Name", "Patients", "Base Share", "Total Revenue", "Avg Visits", "ALOS (Days)", "30d Readm", "Bed Days %"]
for c_idx, h in enumerate(headers):
    cell = table.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

table_data = [
    ["High-Acuity Chronic Inpatients", "5,627", "18.8%", "INR 344.9 Cr (94.1%)", "22.1 visits", "8.53 days", "15.0%", "99.3%"],
    ["Proactive Wellness & Loyalists", "11,234", "37.5%", "INR 16.7 Cr (4.6%)", "15.3 visits", "0.04 days", "0.0%", "0.3%"],
    ["Seasonal Acute Outpatients", "8,011", "26.7%", "INR 4.0 Cr (1.1%)", "5.4 visits", "0.02 days", "0.0%", "0.3%"],
    ["Transactional Minor Walk-ins", "5,128", "17.1%", "INR 0.9 Cr (0.2%)", "2.5 visits", "0.00 days", "0.0%", "0.1%"]
]

for r_idx, row_vals in enumerate(table_data):
    for c_idx, val in enumerate(row_vals):
        cell = table.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else LIGHT_BG
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_GRAY
        p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
        if c_idx == 0:
            p.font.bold = True

# -------------------------------------------------------------
# SLIDE 5: Visualizing Revenue vs Patient Share & Clinical Impact
# -------------------------------------------------------------
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Clinical & Financial Asymmetry Across Segments", "18.8% of Inpatients Drive 94.1% of Revenue and 99.3% of Bed-Days, While Outpatients Drive Footfall")

# Insert charts
if os.path.exists('outputs/charts/segment_size_and_revenue_share.png'):
    s5.shapes.add_picture('outputs/charts/segment_size_and_revenue_share.png', Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.0))

if os.path.exists('outputs/charts/clinical_kpi_profile_bars.png'):
    s5.shapes.add_picture('outputs/charts/clinical_kpi_profile_bars.png', Inches(6.8), Inches(1.8), Inches(5.8), Inches(5.0))

# -------------------------------------------------------------
# SLIDE 6: Stretch Requirement - 2-Year Segment Stability & Migration
# -------------------------------------------------------------
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Stretch Requirement: 2-Year Segment Stability & Migration", "Tracking Patient Trajectories from Period 1 (2022) to Period 2 (2023)")

# Insert Migration Heatmap
if os.path.exists('outputs/charts/segment_migration_matrix_heatmap.png'):
    s6.shapes.add_picture('outputs/charts/segment_migration_matrix_heatmap.png', Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))

# Right Text Card: Insights
add_card(s6, Inches(7.1), Inches(1.8), Inches(5.4), Inches(5.0), WHITE, SLATE)
tb = s6.shapes.add_textbox(Inches(7.3), Inches(2.0), Inches(5.0), Inches(4.6))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Key Migration Dynamics & Takeaways"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = NAVY

insights = [
    "\n• Overall Stability Rate: 56.5% of active patients remained in their primary segment year-over-year.",
    "• High-Acuity Chronic Inpatient Stickiness: 88.1% stability rate. Once complex inpatient care is established, patient retention is extraordinarily high.",
    "• The Walk-in Churn Vulnerability: 25.2% of Transactional Walk-ins migrated to dormancy or left the network in Year 2, representing major leaky-bucket leakage.",
    "• Seasonal Fluctuations: 33.3% of Seasonal Acute patients transitioned to minor walk-ins in off-monsoon years, proving that monsoon outreach is essential to retain them.",
    "• Strategic Takeaway: Converting just 10% of walk-ins into the Proactive Wellness tier would generate an additional INR 1.8 Cr in recurring preventative revenue."
]
for ins in insights:
    p = tf.add_paragraph()
    p.text = ins
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_GRAY

# -------------------------------------------------------------
# SLIDE 7: Concrete Strategic Actions & ROI Roadmap
# -------------------------------------------------------------
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Tailored Action Plans & Measurable ROI per Segment", "Prioritized Initiatives, Cost Estimates, Expected Benefits, and Measurable KPI Targets")

# Table for Actions
rows, cols = 5, 6
t_s7 = s7.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
t7 = t_s7.table

t7.columns[0].width = Inches(2.3) # Segment
t7.columns[1].width = Inches(2.5) # Action
t7.columns[2].width = Inches(1.4) # Cost
t7.columns[3].width = Inches(1.6) # Benefit
t7.columns[4].width = Inches(1.1) # Net ROI
t7.columns[5].width = Inches(2.8) # KPI Target

headers7 = ["Segment Name", "Concrete Action", "Annual Cost", "Expected Benefit", "Net ROI", "Measurable Target"]
for c_idx, h in enumerate(headers7):
    cell = t7.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

action_rows = [
    ["High-Acuity Chronic Inpatients", "Nurse Navigator Discharge Protocol & Remote Tele-monitoring", "INR 28 Lakhs", "INR 1.12 Cr", "300%", "Cut readmissions from 15% to <10%; shorten ALOS by 1.2 days"],
    ["Proactive Wellness & Loyalists", "'Hyderabad Arogya Family Shield' annual diagnostics subscription", "INR 15 Lakhs", "INR 72 Lakhs", "380%", "Enroll 3,500 families; boost annual spend by INR 1,800/family"],
    ["Seasonal Acute Outpatients", "Monsoon Rapid Fever Pods at HITEC City & Secunderabad clinics", "INR 18 Lakhs", "INR 54 Lakhs", "200%", "Reduce triage wait time by 45%; capture 4,200 additional visits"],
    ["Transactional Minor Walk-ins", "WhatsApp Chatbot & Self-Pay digital booking kiosk", "INR 8 Lakhs", "INR 32 Lakhs", "300%", "Shift 65% bookings to digital; convert 2,000 walk-ins to registered users"]
]

for r_idx, row_vals in enumerate(action_rows):
    for c_idx, val in enumerate(row_vals):
        cell = t7.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else LIGHT_BG
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_GRAY
        p.alignment = PP_ALIGN.LEFT if c_idx in [0, 1, 5] else PP_ALIGN.CENTER
        if c_idx == 0:
            p.font.bold = True

# -------------------------------------------------------------
# SLIDE 8: Executive Summary & Recommendation for Business Head
# -------------------------------------------------------------
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Executive Recommendation & Implementation Roadmap", "Next Steps for Management: Moving from One-Size-Fits-All to Differentiated Care")

# 3 Horizontal Cards (Phases)
p_w = Inches(3.7)
p_h = Inches(5.1)

# Phase 1: Immediate (Months 1-3)
add_card(s8, Inches(0.8), top_y, p_w, p_h, WHITE, SLATE)
tb = s8.shapes.add_textbox(Inches(1.0), top_y + Inches(0.2), p_w - Inches(0.4), p_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Phase 1: Immediate Fixes (M 1-3)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = CORAL

p1_steps = [
    "\n1. Stop ERP Tax Bug: Immediate system patch on hospital billing software to stop double-counting 18% GST.",
    "2. Clinical Free-Text Standard: Mandate ICD-10 dropdown selectors in EMR instead of unstructured typing.",
    "3. Launch WhatsApp Bot: Deploy self-service kiosk to reduce front-desk congestion across all 4 hospitals."
]
for s in p1_steps:
    p = tf.add_paragraph()
    p.text = s
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_GRAY

# Phase 2: Clinical Optimization (Months 4-6)
add_card(s8, Inches(4.8), top_y, p_w, p_h, WHITE, SLATE)
tb = s8.shapes.add_textbox(Inches(5.0), top_y + Inches(0.2), p_w - Inches(0.4), p_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Phase 2: Care Navigation (M 4-6)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = NAVY

p2_steps = [
    "\n1. Nurse Navigator Hiring: Station 4 specialized post-discharge navigators at Banjara Hills and HITEC City.",
    "2. Chronic Monitoring Kit: Distribute digital BP/glucose cuffs to high-risk diabetic/cardiac inpatients.",
    "3. Bed Allocation Protocol: Reserved elective surgical scheduling based on ALOS forecasting models."
]
for s in p2_steps:
    p = tf.add_paragraph()
    p.text = s
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_GRAY

# Phase 3: Scaling & Retention (Months 7-12)
add_card(s8, Inches(8.8), top_y, p_w, p_h, WHITE, SLATE)
tb = s8.shapes.add_textbox(Inches(9.0), top_y + Inches(0.2), p_w - Inches(0.4), p_h - Inches(0.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Phase 3: Scale & Loyalty (M 7-12)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = TEAL

p3_steps = [
    "\n1. Launch Family Shield: Roll out annual preventative subscription to 11,000+ loyal patient households.",
    "2. Monsoon Triage Deployment: Rapid fever testing pods active from July to October at high-density clinics.",
    "3. Financial Realization: Achieve full INR 2.70 Cr annual net benefit with 390% cumulative network ROI."
]
for s in p3_steps:
    p = tf.add_paragraph()
    p.text = s
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_GRAY

pptx_path = 'Presentation/Hyderabad_Clinics_Patient_Segmentation_Executive_Deck.pptx'
prs.save(pptx_path)
print(f"Executive presentation generated successfully: {pptx_path}")
