# 🛡️ VoxGuard - Jan Sahayak
### AI-Assisted Public Grievance Intelligence Platform
**PS-04 | Bihar Police Cyber Hackathon | Team: Civic Lens**

> Prototype for Demo — Use only permitted, public, or synthetic data. All predictions require human review.

### 🔴 Problem Statement (PS-04)
- Citizen complaints are scattered across social media, calls, and written reports.
- High volume of duplicate complaints, misinformation, and no priority tagging.
- Lack of real-time spike detection and location-wise insights for Police/Admin.

### ✅ Our Solution
**VoxGuard** is a Streamlit-based MVP that provides:
1.  **Auto-Classification**: Classifies issues into Pothole, Waterlogging, Garbage, Streetlight, etc.
2.  **Deduplication**: Groups similar complaints from the same area to avoid repetition.
3.  **Priority Scoring**: Calculates priority (P0-Critical to P3-Low) based on urgency, location, and keywords.
4.  **Department Routing**: Auto-suggests responsible department — Municipal, PWD, Electricity, etc.
5.  **Analytics Dashboard**: Shows daily trends, spike alerts, and status tracking.

### ✨ Key Features
- **Overview**: Total reports, high-priority count, recent spikes — with a clean civic theme
- **Submit Complaint**: Citizen form and CSV bulk upload
- **Incident Explorer**: Search, filter, sort, and update status (Pending / In-Progress / Resolved)
- **Resolution Tracker**: Audit history of actions taken
- **Evaluation**: Model performance metrics for prototype

### 🛠️ Tech Stack
- Frontend: Streamlit (Python) with Custom Light Theme
- Backend: Python modules — `classifier.py`, `deduplication.py`, `priority.py`, `location.py`
- Database: SQLite (`jan_sahayak.db`)
- Data: Pandas for analytics

### 🚀 Setup Locally
```bash
git clone https://github.com/samsh-kamar/JAN_SAHAYAK_MVP_Starter.git
cd JAN_SAHAYAK_MVP_Starter
pip install -r requirements.txt
streamlit run app.py --theme.base light