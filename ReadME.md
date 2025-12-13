# Data-Gov Hub: Intelligent Governance for Enterprise CSVs

> **From Data Chaos to Data Compliance: A Full-Stack Solution**

## 📋 Overview
**Data-Gov Hub** is a centralized, secure, and intelligent web platform designed to upload, analyze, govern, and trust enterprise CSV data sources. 

Enterprises today run on data, but much of it remains "dark"—locked away in thousands of scattered CSV files. This creates "data silos," quality issues, and massive compliance risks (GDPR, CCPA) due to hidden PII. Data-Gov Hub transforms this reactive chaos into proactive management by providing a complete automated governance lifecycle.

## 🚀 Key Features

### 1. Automated Ingestion & Profiling
* **Seamless Upload:** Modern drag-and-drop interface handling multiple CSVs simultaneously.
* **Deep Analysis:** Automatic profiling of column statistics, type inference, null counts, and distinctness metrics.
* **Anomaly Detection:** Automatically flags outliers, duplicates, and formatting errors.

### 2. Intelligent Quality Scoring
* **At-a-Glance Grading:** Datasets receive **A-F scores** based on completeness, uniqueness, and validity.
* **Stop "Garbage In":** Ensures only trustworthy data is used for analytics and decision-making.

### 3. Automated Governance & Compliance
* **PII Detection Engine:** Scans and tags sensitive information automatically:
    * Email addresses
    * Phone numbers
    * Social Security Numbers (SSNs)
    * Credit card numbers
    * Custom patterns (e.g., Employee IDs)
* **Compliance Flags:** Routes datasets containing PII for immediate review to ensure GDPR/CCPA compliance.

### 4. Custom Rules & Lineage
* **Rules Engine:** Empower data stewards to define custom validation rules.
* **Data Lineage:** detailed audit trails tracking who uploaded what and when modifications occurred.
* **Centralized Catalog:** A searchable view of all governed CSV sources with metadata tags and business glossaries.

## 🛠️ Tech Stack
This project utilizes a modern, scalable architecture:

* **Core Framework: Streamlit** (Python) for the interactive UI and dashboard elements.
* **Data Processing: Pandas** for loading, cleaning, profiling, and analyzing data.
* **Visualization:** **Plotly** for interactive charts and data quality graphs.
* **Configuration:** **PyYAML** for parsing governance rules (`rules.yaml`).

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/keya-05/Automated-Data-Governance-Tool.git](https://github.com/keya-05/Automated-Data-Governance-Tool.git)
    cd Automated-Data-Governance-Tool
    ```

2.  **Install Dependencies**
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing, install the core libs: `pip install streamlit pandas plotly pyyaml`)*

3.  **Run the Application**
    ```bash
    streamlit run app.py
    ```
    

## 🗺️ Project Roadmap

| Phase | Status | Description |
| :--- | :--- | :--- |
| **Phase 1: The Core (MVP)** | ✅ | User Auth, Backend Upload, Core Profiling, Read-only Catalog |
| **Phase 2: Governance Engine** | 🚧 | Backend PII Detection, Custom Rules Engine, Governance Console |
| **Phase 3: Insights** | 📅 | Interactive Recharts Dashboards, Exportable Audit Reports |
| **Phase 4: Enterprise Scale** | 🔮 | PostgreSQL Migration, RBAC, Cloud Storage (S3/Azure) |


---
*Built to turn scattered, "dark" CSVs into a secure and searchable enterprise asset.*
