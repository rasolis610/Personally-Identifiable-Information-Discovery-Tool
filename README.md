# Personally-Identifiable-Information-Discovery-Tool
Personally Identifiable Information--PII Data Discovery

PII Data Discovery Tool
Username=Username
Password=Password




**Version 2.7 — Updated 11/06/2025**
**Created by: Ramón Solís**

---

Overview

The **PII Data Discovery Tool** is a Python-based desktop application designed to recursively scan folders and documents for **Personally Identifiable Information (PII)**. It uses advanced regex patterns to detect sensitive data such as emails, passwords, SSNs, credit card numbers, usernames, phone numbers, and more.

The script supports multiple file formats, generates a **professional PDF report**, and includes a simple authentication and GUI interface using Tkinter.

This tool is intended for **internal IT security teams, auditors, and compliance analysts** to help identify exposure risks and protect organizational data.

---

## 🛡️ Features

### ✔️ Multi-format File Scanning

The tool extracts and scans text from:

* `.txt`
* `.pdf` (via PyMuPDF / Fitz)
* `.json`
* `.docx`, `.doc`
* `.csv`
* `.xlsx`, `.xls`

---

### ✔️ PII Types Detected

The script detects the following sensitive data patterns:

* Credentials
* Credit Card numbers
* Date of Birth
* Emails
* IP Addresses
* Login
* MAC Addresses
* Passwords
* Phone numbers
* Postal/Street addresses
* SSN (Social Security Number)
* Usernames
* Vehicle Registration Numbers

All detections also support a checkbox GUI selector so the user can choose what PII they want to scan for.

---

### ✔️ GUI Interface

The tool includes:

* 🔐 **Login Window**
* 🧩 **PII Pattern Selection Window**
* 📁 **Directory Picker**
* 📄 **PDF Report Generator**

All generated reports are automatically timestamped.

---

## 📄 PDF Reporting

After each scan, the tool generates a detailed, timestamped PDF report that includes:

* A confidentiality disclaimer
* Date & time
* Each file containing PII
* Type(s) of PII found
* Total number of flagged files

Reports use **ReportLab** in U.S. Letter format.

---

## 🧠 Technologies Used

| Component         | Library                |
| ----------------- | ---------------------- |
| GUI               | Tkinter                |
| PDF Extraction    | PyMuPDF (fitz)         |
| DOCX Extraction   | python-docx / docx2txt |
| PDF Reporting     | ReportLab              |
| Excel Reading     | pandas                 |
| JSON/XML Handling | json / xml.etree       |
| File Parsing      | os, re, csv            |

---

## 🚀 How to Run



### **Run the tool**

```bash
PII Data Discovery  Tool © 2025 by Ramon Solis v2.7.py
(exe on windows just double clicj the exe file.)

---

## 📦 Folder Structure Example

```
project/
│
├── PII Data Discovery  Tool © 2025 by Ramon Solis v2.7.py
├── README.md
└── reports/
    ├── Report_Data_Discovery_Found_20250101_153000.pdf
```

---

## ⚙️ Configuration

You may customize:

* Regex patterns
* Excluded paths
* Login credentials
* PDF footer text
* Default output folder

All modifications can be done near the top of the script.

---

## ⚠️ Confidentiality Disclaimer

```
The information produced by this tool is confidential and intended solely 
for authorized IT and security personnel. Unauthorized use, distribution, 
or disclosure is strictly prohibited.

Copyright © 2025 — Ramon Solis
```

---

## 📝 License

This tool is free use.
You are alow to copy, modify, or redistribute.

---

## 🧑‍💻 Author

**Ramon Solis**
© 2025

---


