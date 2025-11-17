
"""
 Ramon Solis
 Pyhton Script to find PII Data
 Modify on 11-06-2025
 Version 2.7
"""

    
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
print ('\n' *7)

print ('██████╗ ██╗██╗    ████████╗ ██████╗  ██████╗ ██╗       ')
print ('██╔══██╗██║██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║       ')
print ('██████╔╝██║██║       ██║   ██║   ██║██║   ██║██║       ')
print ('██╔═══╝ ██║██║       ██║   ██║   ██║██║   ██║██║       ')
print ('██║     ██║██║       ██║   ╚██████╔╝╚██████╔╝███████╗  ')
print ('╚═╝     ╚═╝╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝  ')



print ('\n' *1)       
print ('PII Data Discovery Tool © 2025 by Ramon Solis')
print ('\n' *1)

text_context = """Searching for PII Data:\n\nCredit Card, Date of Birth, Emails, IP Addresses, Login, MAC Address, Password, 
\nPhone Number, Postal Address, SSN (Social Security Number), Username.
"""
text_disclaimer = """***Confidentiality Disclaimer***     \n\nThe information contained within any report, document, or
communication originating from this source is the exclusive \nproperty of the IT Department. It is intended solely for the designated recipient(s) and \nis considered confidential. If you have received this information
in error, please inform the Technology Department promptly \nand delete all copies of the information from your systems.
Furthermore, refrain from using, sharing, printing, or \ntransmitting the information in any form without proper authorization.
\nCopyright Ramon Solis © 2025.
"""

print(text_disclaimer)
print ('\n' *1)
print(text_context)
print ('\n' *1)

import os
import re
import csv
import datetime
import textract
import docx2txt
import pandas as pd
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from reportlab.lib.units import inch
from io import StringIO
import fitz  # PyMuPDF
import json
import getpass  # used to take password input
import xml.etree.ElementTree as ET
from PyPDF2 import PdfWriter, PdfReader
import sys
import pdfrw
from tkinter import Tk, Label, Entry, Button, messagebox, Checkbutton, IntVar


# Define regex patterns for PII data
patterns = {
    'Credentials': r'(?i)(?<!\S)(credentials\s*[:=]\s*[a-zA-Z0-9._%+-]+)',
    'Credit_Card': r'(\d{4}[-\s]{1,2}){3}\d{4}',
    'Date_of_Birth': r'(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d{2}',
    'Email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'IPV4': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    'Login': r'(?i)(?<!\S)(login\s*[:=]\s*[a-zA-Z0-9._%+-]+)',
    'Mac_Address': r'(?i)\b((?:[0-9A-F]{2}[:-]){5}[0-9A-F]{2})\b',
    'Password': r'(?i)(?<!\S)(pass(word)?\s*[:=]\s*[a-zA-Z0-9._%+-]+)',
    'Phone': r'\+1?\s*\(?([2-9][0-8][0-9])\)?[-.\s]*([2-9][0-9]{2})[-.\s]*([0-9]{4})',
    'Postal_Address': r'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|pk|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)',
    'SSN': r'\d{3}-\d{2}-\d{4}',
    'Username': r'(?i)(?<!\S)(user(name)?\s*[:=]\s*[a-zA-Z0-9._%+-]+)',
    'Vehicle_Reg': r'\b[A-Z]{2}\d{2} [A-Z]{3}\b',
}

selected_patterns = []


def main_code():
                
    def should_exclude(file_path):
        # Define your exclusion logic here
        excluded_paths = [
            "/path/to/excluded_directory",
            "/path/to/excluded_file.txt"
        ]
        return file_path in excluded_paths

    def read_plain_text(file_path):
        if os.access(file_path, os.R_OK):  # Check if the file is readable
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        else:
            print(f"Permission denied for file: {file_path}")
            return ""

    def read_json(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError:
            print(f"Failed to process JSON file: {file_path}")
            return None

    def read_pdf(file_path):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except (RuntimeError, Exception):
            print(f"Error reading PDF file: {file_path}")
            return ""

    def read_xml(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        return ET.tostring(root, encoding='utf8').decode('utf8')

    def read_word(file_path):
        try:
            doc = Document(file_path)
            text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error reading Word file {file_path}: {e}")
            return None

    def read_excel(file_path):
        content = []
        try:
            df = pd.read_excel(file_path, header=None)
            content = df.stack().astype(str).tolist()
        except Exception as e:
            print(f"Error reading Excel file {file_path}: {e}")
        return ' '.join(content)

    def read_csv(file_path):
        content = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            for row in reader:
                content.append(' '.join(row))
        return ' '.join(content)

    def scan_files(folder_path):
        found_pii_data = set()

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                try:
                    if should_exclude(file_path):
                        continue

                    content = ''
                    if file.lower().endswith('.txt'):
                        content = read_plain_text(file_path)
                    elif file.lower().endswith('.pdf'):
                        content = read_pdf(file_path)
                    elif file.lower().endswith('.json'):
                        data = read_json(file_path)
                        if data is not None:
                            content = json.dumps(data)
                    elif file.lower().endswith(('.docx', '.doc')):
                        content = read_word(file_path)
                    elif file.lower().endswith(('.xlsx', '.xls')):
                        content = read_excel(file_path)
                    elif file.lower().endswith('.csv'):
                        content = read_csv(file_path)

                    if content:
                        for key, pattern in patterns.items():
                            if key in selected_patterns and re.search(pattern, content):
                                found_pii_data.add((file_path, key))
                                print(f"Found {key} in file: {file_path}")
                        if not found_pii_data:
                            print("No Data Found")

                except PermissionError:
                    print(f"Permission denied for file: {file_path}")
                    continue

        return found_pii_data

    def create_pdf_report(pii_data_list, output_filename):
        doc = SimpleDocTemplate(output_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.textColor = colors.red
        story = [Paragraph("Report PII Data Discovery Found - PPS © 2024", title_style)]
        story.append(Paragraph("""***Confidentiality Disclaimer***      The information contained within this report, document, or
        communication originating from this source is the exclusive property of the IT Department.
        It is intended solely for the designated recipient(s) and is considered confidential. If you have received this information
        in error, please inform the Technology Department promptly and delete all copies of the information from your systems.
        Furthermore, refrain from using, sharing, printing, or transmitting the information in any form without proper authorization.

                                    Copyright Ramon Solis © 2025."""))
        
        story.append(Paragraph(f"Date and Time: {datetime.datetime.now()}", styles["BodyText"]))

        counter = 1
        for file_path, data_type in pii_data_list:
            story.append(Paragraph(f"{counter}. Found {data_type}: {file_path}", styles["BodyText"]))
            counter += 1

        story.append(Paragraph(f"Total files with sensitive data found: {len(pii_data_list)}", styles["BodyText"]))

        doc.build(story)


      

    def login():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        if entered_username == "Username" and entered_password == "Password":
            login_window.destroy()
            pattern_selection_window()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

            

    def pattern_selection_window():
        def scan():
            for i in range(len(pattern_checkboxes)):
                if pattern_var[i].get() == 1:
                    selected_patterns.append(patterns_list[i])
            pattern_selection_window.destroy()
            folder_path = filedialog.askdirectory()
            pii_data_list = scan_files(folder_path)

            
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"Report_Data_Discovery_Found_{current_time}.pdf"

            create_pdf_report(pii_data_list, output_filename)
            if pii_data_list:
                print("PDF report created successfully.")
            else:
                print("No PII data found. Empty report created.")
            
        pattern_selection_window = Tk()
        pattern_selection_window.title("Regex Pattern Selection")
        pattern_selection_window.geometry("300x425")  # Set window size

        patterns_list = list(patterns.keys())
        pattern_var = [IntVar() for _ in range(len(patterns_list))]
        pattern_checkboxes = []

        for i, pattern in enumerate(patterns_list):
            checkbox = Checkbutton(pattern_selection_window, text=pattern, variable=pattern_var[i])
            checkbox.pack(anchor=tk.W)
            pattern_checkboxes.append(checkbox)

        scan_button = Button(pattern_selection_window, text="SCAN", command=scan, bg="green", width=25, height=25)  # Set button color and size
        scan_button.pack(pady=10)

        pattern_selection_window.mainloop()

    login_window = Tk()
    login_window.title("User Login")
    login_window.geometry("300x125")  # Set window size

    username_label = Label(login_window, text="Username:")
    username_entry = Entry(login_window)
    password_label = Label(login_window, text="Password:")
    password_entry = Entry(login_window, show="*")
    login_button = Button(login_window, text="Login", command=login)

    username_label.grid(row=0, column=0, padx=10, pady=5)
    username_entry.grid(row=0, column=1, padx=10, pady=5)
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)


    
    login_window.mainloop()

    sys.exit()


if __name__ == "__main__":
    main_code()
