import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas for adding page numbers and running header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (on pages after the first)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "CardioGuard AI — Machine Learning Project Documentation")
            self.drawRightString(letter[0] - 54, letter[1] - 36, "Academic Evaluation Report")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_text)
        self.drawString(54, 36, "Confidential — Prepared for Machine Learning Course Examination")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, letter[0] - 54, 48)
        
        self.restoreState()


def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0f766e") # Deep Teal
    accent_color = colors.HexColor("#4338ca")  # Royal Indigo
    dark_text = colors.HexColor("#0f172a")
    muted_text = colors.HexColor("#475569")
    card_bg = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_color,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=dark_text,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a")
    )

    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=dark_text
    )

    td_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=primary_color
    )

    story = []

    # Title & Metadata Banner
    story.append(Paragraph("CardioGuard AI — Project Documentation", title_style))
    story.append(Paragraph("End-to-End Machine Learning System for Cardiovascular Disease Risk Stratification", subtitle_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Subject:</b> Machine Learning Project Evaluation", body_style),
            Paragraph("<b>Architecture:</b> Stacking Classifier Meta-Ensemble", body_style)
        ],
        [
            Paragraph("<b>Model ROC-AUC:</b> 0.8048 (73.20% Test Accuracy)", body_style),
            Paragraph("<b>Tech Stack:</b> Python, FastAPI, Scikit-learn, XGBoost, React, Vite", body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdfa")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#99f6e4")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ccfbf1")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # 1. Executive Summary & Problem Statement
    story.append(Paragraph("1. Executive Summary & Problem Formulation", h1_style))
    story.append(Paragraph(
        "Cardiovascular diseases (CVDs) are the leading cause of mortality globally. Early detection of asymptomatic high-risk patients using routine clinical biomarkers allows preventive lifestyle and therapeutic interventions. "
        "This project presents <b>CardioGuard AI</b>, a production-grade machine learning application designed to assess 10-year cardiovascular disease risk from physiological, hemodynamic, and lifestyle indicators.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Core Objectives:</b><br/>"
        "• Establish a leakage-free preprocessing and feature engineering pipeline on 70,000 clinical records.<br/>"
        "• Implement and benchmark baseline models (Logistic Regression, Decision Tree) and modern gradient boosting algorithms (XGBoost, LightGBM, HistGradientBoosting).<br/>"
        "• Engineer a heterogeneous <b>Stacking Ensemble Classifier</b> with a cross-validated meta-model achieving superior ROC-AUC (0.8048).<br/>"
        "• Deploy an asynchronous REST API using <b>FastAPI</b> paired with an interactive <b>React + Vite</b> responsive dashboard.",
        body_style
    ))

    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=8, spaceAfter=8))

    # 2. Dataset Description & Preprocessing Pipeline
    story.append(Paragraph("2. Dataset & Preprocessing Pipeline", h1_style))
    story.append(Paragraph(
        "The model is trained on the Cardiovascular Disease Dataset comprising 70,000 patient records across 12 primary features.",
        body_style
    ))

    data_desc_rows = [
        [Paragraph("Feature Name", th_style), Paragraph("Type", th_style), Paragraph("Clinical Description", th_style), Paragraph("Data Range / Units", th_style)],
        [Paragraph("age_years", td_bold), Paragraph("Continuous", td_style), Paragraph("Patient age in full solar years (age in days / 365.25)", td_style), Paragraph("18 – 100 years", td_style)],
        [Paragraph("gender", td_bold), Paragraph("Categorical", td_style), Paragraph("Biological sex", td_style), Paragraph("1: Female, 2: Male", td_style)],
        [Paragraph("height / weight", td_bold), Paragraph("Continuous", td_style), Paragraph("Stature and mass", td_style), Paragraph("100-220 cm / 30-200 kg", td_style)],
        [Paragraph("ap_hi / ap_lo", td_bold), Paragraph("Continuous", td_style), Paragraph("Systolic / Diastolic arterial blood pressure", td_style), Paragraph("50-250 / 30-150 mmHg", td_style)],
        [Paragraph("cholesterol", td_bold), Paragraph("Ordinal", td_style), Paragraph("Total serum cholesterol level tier", td_style), Paragraph("1: Normal, 2: Above, 3: High", td_style)],
        [Paragraph("gluc", td_bold), Paragraph("Ordinal", td_style), Paragraph("Fasting serum glucose level tier", td_style), Paragraph("1: Normal, 2: Above, 3: High", td_style)],
        [Paragraph("smoke / alco", td_bold), Paragraph("Binary", td_style), Paragraph("Tobacco smoking / Alcohol consumption habits", td_style), Paragraph("0: No, 1: Yes", td_style)],
        [Paragraph("active", td_bold), Paragraph("Binary", td_style), Paragraph("Regular physical activity commitment", td_style), Paragraph("0: Inactive, 1: Active", td_style)],
        [Paragraph("cardio (Target)", td_bold), Paragraph("Binary", td_style), Paragraph("Presence or absence of cardiovascular disease", td_style), Paragraph("0: Healthy, 1: Diseased", td_style)],
    ]
    data_table = Table(data_desc_rows, colWidths=[90, 65, 230, 119])
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(data_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Data Cleaning & Outlier Filtration:", h2_style))
    story.append(Paragraph(
        "1. <b>Physiological Consistency:</b> Filtered records where diastolic pressure exceeded systolic pressure (<code>ap_hi <= ap_lo</code>).<br/>"
        "2. <b>Extreme Outlier Removal:</b> Removed impossible blood pressures (<50 mmHg or >250 mmHg for systolic; <30 mmHg or >150 mmHg for diastolic).<br/>"
        "3. <b>Anthropometric Bounds:</b> Constrained height to [100, 220] cm and weight to [30, 200] kg.<br/>"
        "4. <b>Resulting Dataset:</b> <b>68,640 clean records</b> (50.0% class balance maintained).",
        body_style
    ))

    story.append(Paragraph("Leakage-Free Feature Engineering Pipeline:", h2_style))
    story.append(Paragraph(
        "To maximize predictive signal without causing data leakage, the following clinical features are computed dynamically inside an <code>sklearn.base.TransformerMixin</code> (<code>FeatureEngineer</code>):<br/>"
        "• <b>Body Mass Index (BMI):</b> \\( \\text{weight (kg)} / (\\text{height (m)})^2 \\)<br/>"
        "• <b>Pulse Pressure (PP):</b> \\( \\text{ap\\_hi} - \\text{ap\\_lo} \\) (measures arterial vascular stiffness)<br/>"
        "• <b>Mean Arterial Pressure (MAP):</b> \\( \\text{ap\\_lo} + \\frac{\\text{PP}}{3} \\) (measures continuous organ perfusion)<br/>"
        "• <b>Blood Pressure Ratio:</b> \\( \\text{ap\\_hi} / \\text{ap\\_lo} \\)<br/>"
        "• <b>Interaction Features:</b> \\( \\text{Age} \\times \\text{ap\\_hi} \\), \\( \\text{Cholesterol} \\times \\text{Glucose} \\), \\( \\text{BMI} \\times \\text{Age} \\)<br/>"
        "• <b>Log Transformations:</b> \\( \\ln(1 + \\text{weight}) \\), \\( \\ln(1 + \\text{BMI}) \\) to normalize right-skewed distributions.<br/>"
        "• <b>Infinite-Bounded Binning:</b> Robust categorization for age groups, BMI tiers, and systolic ranges using \\([-\\infty, \\dots, \\infty]\\) to prevent <code>NaN</code> evaluation.",
        body_style
    ))

    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=8, spaceAfter=8))

    # 3. Machine Learning Algorithms & Model Comparison
    story.append(Paragraph("3. Machine Learning Algorithms & Benchmark Evaluation", h1_style))
    story.append(Paragraph(
        "Models were evaluated using <b>Repeated Stratified K-Fold Cross-Validation</b> (3 splits, 2 repeats, 6 folds total) to guarantee statistical robustness. A separate untouched 20% test partition (13,728 patients) was used for final validation.",
        body_style
    ))

    results_table_data = [
        [Paragraph("Model Architecture", th_style), Paragraph("Classification Paradigm", th_style), Paragraph("CV Mean Acc", th_style), Paragraph("Test Acc", th_style), Paragraph("Test ROC-AUC", th_style), Paragraph("F1 Score", th_style), Paragraph("Role", th_style)],
        [Paragraph("Stacking Classifier Ensemble", td_bold), Paragraph("Heterogeneous Meta-Learner", td_style), Paragraph("73.53% ±0.26%", td_style), Paragraph("73.20%", td_bold), Paragraph("0.8048", td_bold), Paragraph("0.7165", td_style), Paragraph("Production Model", td_bold)],
        [Paragraph("HistGradientBoosting", td_style), Paragraph("Binned Tree Boosting", td_style), Paragraph("73.56% ±0.23%", td_style), Paragraph("73.15%", td_style), Paragraph("0.7999", td_style), Paragraph("0.7151", td_style), Paragraph("Base Estimator", td_style)],
        [Paragraph("XGBoost Classifier", td_style), Paragraph("Regularized Boosting (XGB)", td_style), Paragraph("73.50% ±0.27%", td_style), Paragraph("73.08%", td_style), Paragraph("0.7991", td_style), Paragraph("0.7145", td_style), Paragraph("Base Estimator", td_style)],
        [Paragraph("LightGBM Classifier", td_style), Paragraph("Leaf-wise Boosting (LGBM)", td_style), Paragraph("73.50% ±0.31%", td_style), Paragraph("73.09%", td_style), Paragraph("0.7991", td_style), Paragraph("0.7147", td_style), Paragraph("Base Estimator", td_style)],
        [Paragraph("Decision Tree (depth=5)", td_style), Paragraph("Single Decision Tree", td_style), Paragraph("—", td_style), Paragraph("73.11%", td_style), Paragraph("0.7919", td_style), Paragraph("0.7134", td_style), Paragraph("Baseline Benchmark", td_style)],
        [Paragraph("Logistic Regression (Sklearn)", td_style), Paragraph("L2 Linear Logistic Model", td_style), Paragraph("—", td_style), Paragraph("72.67%", td_style), Paragraph("0.7935", td_style), Paragraph("0.7070", td_style), Paragraph("Meta-Model", td_style)],
        [Paragraph("Logistic Regression (Scratch)", td_style), Paragraph("Custom Gradient Descent", td_style), Paragraph("—", td_style), Paragraph("72.70%", td_style), Paragraph("0.7920", td_style), Paragraph("0.7065", td_style), Paragraph("Algorithm Verification", td_style)],
    ]

    results_table = Table(results_table_data, colWidths=[120, 105, 75, 50, 60, 44, 50])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f0fdfa"), colors.white, colors.white, colors.white, colors.white, colors.white, colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(results_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Stacking Ensemble Architecture Explained:", h2_style))
    story.append(Paragraph(
        "<b>Level-0 Base Learners:</b> Three diverse gradient boosting algorithms (HistGradientBoosting, XGBoost, LightGBM) learn non-linear feature interactions and high-dimensional boundaries independently.<br/>"
        "<b>Level-1 Meta-Learner:</b> A regularized Logistic Regression classifier receives out-of-fold probability predictions from the level-0 models and computes optimal ensemble blend weights. This reduces variance and overcomes individual tree biases, yielding the highest overall ROC-AUC (<b>0.8048</b>).",
        body_style
    ))

    story.append(Paragraph("Confusion Matrix & Threshold Analysis (Test Partition - 13,728 samples):", h2_style))
    story.append(Paragraph(
        "• <b>True Negatives (TN):</b> 5,400 &nbsp;|&nbsp; <b>False Positives (FP):</b> 1,537<br/>"
        "• <b>False Negatives (FN):</b> 2,142 &nbsp;|&nbsp; <b>True Positives (TP):</b> 4,649<br/>"
        "• <b>Optimal Clinical Threshold:</b> At \\( t = 0.40 \\), Sensitivity (Recall) rises to <b>76.56%</b> with 73.12% accuracy, ideal for medical screening scenarios where missing a diseased patient carries high penalty.",
        body_style
    ))

    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=8, spaceAfter=8))

    # 4. System Architecture & Full-Stack Integration
    story.append(Paragraph("4. System Architecture & Full-Stack Integration", h1_style))
    story.append(Paragraph(
        "The project follows a decoupled, production-oriented client-server architecture:",
        body_style
    ))

    arch_points = [
        [
            Paragraph("<b>Backend ML Service (FastAPI)</b>", body_bold),
            Paragraph("• Asynchronous ASGI server running on Uvicorn.<br/>• Pydantic schema validation for patient inputs.<br/>• Dynamic pipeline loader with <code>joblib</code> deserialization.<br/>• Multi-tiered fallback mechanism (Ensemble $\\rightarrow$ Baseline $\\rightarrow$ Clinical formula).<br/>• Standardized endpoints: <code>/health</code>, <code>/predict</code>, <code>/docs</code>.", body_style)
        ],
        [
            Paragraph("<b>Frontend Dashboard (React 18 + Vite)</b>", body_bold),
            Paragraph("• Component-driven UI with responsive navigation.<br/>• Real-time client-side BMI and blood pressure gauge calculation.<br/>• 1-click interactive demo profile presets for instant evaluation.<br/>• Transparent metric breakdowns (MAP, Pulse Pressure, Arterial Stiffness).<br/>• Resilient multi-endpoint fetch engine with proxy fallback.", body_style)
        ],
        [
            Paragraph("<b>How Backend & Frontend Connect</b>", body_bold),
            Paragraph("• The React frontend sends JSON payloads via HTTP POST to <code>http://127.0.0.1:8000/predict</code>.<br/>• FastAPI receives the request, validates the schema, applies <code>FeatureEngineer</code>, computes model probabilities, and returns a structured JSON response in &lt;50ms.<br/>• Vite development proxy forwards <code>/predict</code> and <code>/health</code> seamlessly without CORS barriers.", body_style)
        ]
    ]
    arch_table = Table(arch_points, colWidths=[160, 344])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=8, spaceAfter=8))

    # 5. Teacher Evaluation & Viva Defense Q&A
    story.append(Paragraph("5. Key Viva & Evaluation Q&A (Defense Preparation)", h1_style))
    story.append(Paragraph(
        "Anticipated questions and technical answers for course evaluation:",
        body_style
    ))

    qas = [
        ("Q1: Why did you use a Stacking Ensemble instead of a single algorithm?",
         "A1: Single models like XGBoost or LightGBM have individual inductive biases (e.g. tree depth limits or split heuristics). Stacking uses out-of-fold cross-validation predictions from multiple distinct algorithms as meta-features into a regularized logistic meta-learner, minimizing generalization variance and boosting ROC-AUC to 0.8048."),
        
        ("Q2: How did you ensure there was no data leakage in feature engineering?",
         "A2: All feature transformations (Pulse Pressure, MAP, log transformations, binning) are encapsulated inside an scikit-learn Pipeline using a custom TransformerMixin (FeatureEngineer). Scalers and estimators are fitted strictly on training folds and transformed on validation/test folds without sharing global statistics."),

        ("Q3: Why is ROC-AUC more clinically relevant than Accuracy?",
         "A3: In cardiovascular disease screening, False Negatives (predicting a diseased patient as healthy) have severe consequences. ROC-AUC evaluates true positive rate vs false positive rate across all decision thresholds, allowing doctors to tune the sensitivity threshold (e.g. t=0.40) to catch 76.5% of cases."),

        ("Q4: How does the Logistic Regression from scratch work?",
         "A4: It implements batch gradient descent from first principles using NumPy: \\( z = Xw + b \\), sigmoid activation \\( \\sigma(z) = \\frac{1}{1 + e^{-z}} \\), binary cross-entropy loss gradients \\( \\frac{\\partial L}{\\partial w} = \\frac{1}{m} X^T (\\hat{y} - y) \\), and iterative parameter updates \\( w := w - \\alpha \\frac{\\partial L}{\\partial w} \\). It achieved 72.70% accuracy, verifying scikit-learn's result.")
    ]

    for q, a in qas:
        q_box = [
            [Paragraph(f"<b>{q}</b>", td_bold)],
            [Paragraph(a, body_style)]
        ]
        qt = Table(q_box, colWidths=[504])
        qt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#ffffff")),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(qt)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=8, spaceAfter=8))

    # 6. Execution Instructions
    story.append(Paragraph("6. Project Execution Commands", h1_style))
    exec_data = [
        [Paragraph("Component", th_style), Paragraph("Directory", th_style), Paragraph("Command to Run", th_style)],
        [Paragraph("Backend ML Service", td_bold), Paragraph("<code>ML_Project-main/ml-service</code>", td_style), Paragraph("<code>.\\.venv\\Scripts\\uvicorn api.app:app --reload --port 8000</code>", code_style)],
        [Paragraph("Frontend UI", td_bold), Paragraph("<code>ML_Project-main/frontend</code>", td_style), Paragraph("<code>npm run dev</code> (Open http://localhost:5173)", code_style)],
        [Paragraph("Automated Tests", td_bold), Paragraph("<code>ML_Project-main/ml-service</code>", td_style), Paragraph("<code>.\\.venv\\Scripts\\pytest tests/test_api.py -v</code>", code_style)],
        [Paragraph("Retrain Ensemble", td_bold), Paragraph("<code>ML_Project-main/ml-service</code>", td_style), Paragraph("<code>.\\.venv\\Scripts\\python.exe training/train_advanced_models.py</code>", code_style)],
    ]
    exec_table = Table(exec_data, colWidths=[110, 140, 254])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(exec_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Successfully generated at: {output_path}")

if __name__ == "__main__":
    out1 = "c:/Users/ADMIN/Desktop/ML_Project-main_/CardioGuard_AI_Project_Report.pdf"
    out2 = "c:/Users/ADMIN/Desktop/ML_Project-main_/ML_Project-main/CardioGuard_AI_Project_Report.pdf"
    build_pdf(out1)
    build_pdf(out2)
