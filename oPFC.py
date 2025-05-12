import tkinter as tk
from tkinter import ttk, filedialog
import os

CHECKLIST_DATA = {
    "NIST Privacy Framework": [
        {"description": "Identified and mapped personal data.", "has_input": False},
        {"description": "Conducted privacy risk assessments.", "has_input": False},
        {"description": "Developed privacy policies and procedures.", "has_input": False},
        {"description": "Implemented controls to manage privacy risks.", "has_input": False},
        {"description": "Established communication channels about privacy practices.", "has_input": False},
        {"description": "Regularly review and improve privacy practices.", "has_input": False},
        {"description": "Notes on NIST Privacy Framework implementation:", "has_input": True},
    ],
    "SOC 2": [
        {"description": "Determined applicable Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy).", "has_input": False},
        {"description": "Identified and documented internal controls.", "has_input": False},
        {"description": "Implemented necessary controls.", "has_input": False},
        {"description": "Conducted internal readiness assessment/testing.", "has_input": False},
        {"description": "Engaged a third-party auditor (for Type I or Type II).", "has_input": False},
        {"description": "Provided evidence to auditors.", "has_input": False},
        {"description": "Notes on SOC 2 compliance efforts:", "has_input": True},
    ],
    "ISO 27001": [
        {"description": "Defined the scope of the Information Security Management System (ISMS).", "has_input": False},
        {"description": "Conducted information security risk assessment.", "has_input": False},
        {"description": "Developed a risk treatment plan.", "has_input": False},
        {"description": "Implemented security controls from Annex A.", "has_input": False},
        {"description": "Developed necessary policies and procedures.", "has_input": False},
        {"description": "Conducted internal audits of the ISMS.", "has_input": False},
        {"description": "Considered external certification.", "has_input": False},
        {"description": "Notes on ISO 27001 ISMS implementation:", "has_input": True},
    ],
    "PCI-DSS": [
        {"description": "Identified all systems that store, process, or transmit cardholder data (the CDE).", "has_input": False},
        {"description": "Implemented firewalls and configured them securely.", "has_input": False},
        {"description": "Protected stored cardholder data (e.g., encryption).", "has_input": False},
        {"description": "Encrypted transmission of cardholder data across open, public networks.", "has_input": False},
        {"description": "Used and regularly updated anti-virus software.", "has_input": False},
        {"description": "Developed and maintained secure systems and applications.", "has_input": False},
        {"description": "Restricted access to cardholder data by business need-to-know.", "has_input": False},
        {"description": "Assigned a unique ID to each person with computer access.", "has_input": False},
        {"description": "Restricted physical access to cardholder data.", "has_input": False},
        {"description": "Tracked and monitored all access to network resources and cardholder data.", "has_input": False},
        {"description": "Regularly tested security systems and processes.", "has_input": False},
        {"description": "Maintained an information security policy.", "has_input": False},
        {"description": "Completed required SAQ or ROC.", "has_input": False},
        {"description": "Completed required quarterly scans.", "has_input": False},
        {"description": "Notes on PCI-DSS compliance efforts:", "has_input": True},
    ],
    "HIPAA": [
        {"description": "Identified all electronic Protected Health Information (ePHI).", "has_input": False},
        {"description": "Conducted a security risk analysis.", "has_input": False},
        {"description": "Implemented physical safeguards (e.g., facility access controls).", "has_input": False},
        {"description": "Implemented technical safeguards (e.g., access controls, encryption where appropriate).", "has_input": False},
        {"description": "Implemented administrative safeguards (e.g., security management process, training).", "has_input": False},
        {"description": "Developed and distributed a Notice of Privacy Practices.", "has_input": False},
        {"description": "Established procedures for individuals' rights (access, amendment, etc.).", "has_input": False},
        {"description": "Entered into Business Associate Agreements (BAAs) with relevant partners.", "has_input": False},
        {"description": "Developed and implemented a breach notification procedure.", "has_input": False},
        {"description": "Notes on HIPAA compliance efforts:", "has_input": True},
    ],
    "CCPA": [
        {"description": "Determined if the business is subject to CCPA.", "has_input": False},
        {"description": "Mapped personal information collected from California residents.", "has_input": False},
        {"description": "Provided required 'Notice at Collection'.", "has_input": False},
        {"description": "Established methods for handling consumer rights requests (Know, Delete, Opt-Out).", "has_input": False},
        {"description": "Updated privacy policy to include CCPA-specific information.", "has_input": False},
        {"description": "Implemented 'Do Not Sell or Share My Personal Information' link/mechanism.", "has_input": False},
        {"description": "Ensured service provider contracts comply with CCPA.", "has_input": False},
        {"description": "Notes on CCPA compliance efforts:", "has_input": True},
    ],
    "GDPR": [
        {"description": "Determined if GDPR applies (processing data of EU/EEA residents).", "has_input": False},
        {"description": "Identified personal data processed and documented processing activities (ROPA).", "has_input": False},
        {"description": "Identified and documented a lawful basis for each processing activity.", "has_input": False},
        {"description": "Implemented mechanisms for handling data subject rights (Access, Rectification, Erasure, etc.).", "has_input": False},
        {"description": "Updated privacy policy to be GDPR compliant (transparent, accessible, informed consent).", "has_input": False},
        {"description": "Implemented appropriate technical and organizational security measures.", "has_input": False},
        {"description": "Established data breach notification procedures.", "has_input": False},
        {"description": "Considered Data Protection Impact Assessments (DPIAs) for high-risk processing.", "has_input": False},
        {"description": "Appointed a Data Protection Officer (DPO) if required.", "has_input": False},
        {"description": "Notes on GDPR compliance efforts:", "has_input": True},
    ],
}


class ComplianceChecklistApp:
    def __init__(self, root):
        self.root = root
        root.title("Privacy and Security Compliance Checklist")
        root.geometry("900x700")

        # Create container frame
        container = ttk.Frame(root)
        container.pack(fill="both", expand=True)

        # Main canvas and scrollbar
        self.canvas = tk.Canvas(container, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.checklist_vars = {}

        # Mouse wheel support
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        for category, items in CHECKLIST_DATA.items():
            self.create_category_frame(category, items)

        ttk.Button(root, text="Export to HTML", command=self.export_to_html).pack(pady=10)

    def create_category_frame(self, category, items):
        frame = ttk.LabelFrame(self.scrollable_frame, text=category, padding=10)
        frame.pack(fill="x", padx=10, pady=8)

        self.checklist_vars[category] = []

        for item in items:
            container = ttk.Frame(frame)
            container.pack(fill="x", pady=2)

            check_var = tk.BooleanVar()
            chk = ttk.Checkbutton(container, variable=check_var)
            chk.grid(row=0, column=0, sticky="w", padx=5)

            label = ttk.Label(container, text=item["description"], wraplength=600, justify="left")
            label.grid(row=0, column=1, sticky="w", padx=5)

            input_var = None
            if item["has_input"]:
                input_var = tk.StringVar()
                entry = ttk.Entry(container, textvariable=input_var, width=50)
                entry.grid(row=0, column=2, padx=5)

            self.checklist_vars[category].append({
                "description": item["description"],
                "check_var": check_var,
                "input_var": input_var
            })

    def export_to_html(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html")],
            title="Save Checklist as HTML"
        )
        if not filepath:
            return

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n")
            f.write(f"<title>Compliance Checklist - {os.path.basename(filepath)}</title>\n")
            f.write("<style>\n")
            f.write("body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; background:#fff; }\n")
            f.write(".category { margin-bottom: 30px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; background:#f9f9f9; }\n")
            f.write(".category h2 { margin-top: 0; }\n")
            f.write(".item { margin: 8px 0; }\n")
            f.write(".status { font-weight: bold; margin-right: 10px; }\n")
            f.write(".notes { margin-top: 4px; font-style: italic; color:#555; }\n")
            f.write("</style>\n</head>\n<body>\n")
            f.write("<h1>Privacy and Security Compliance Checklist</h1>\n")

            for category, items in self.checklist_vars.items():
                f.write(f"<div class='category'><h2>{category}</h2>\n")
                for item in items:
                    status = "✔️" if item["check_var"].get() else "❌"
                    f.write(f"<div class='item'><span class='status'>{status}</span>{item['description']}</div>\n")
                    if item["input_var"] and item["input_var"].get().strip():
                        f.write(f"<div class='notes'>Note: {item['input_var'].get().strip()}</div>\n")
                f.write("</div>\n")

            f.write("</body>\n</html>")

if __name__ == "__main__":
    root = tk.Tk()
    app = ComplianceChecklistApp(root)
    root.mainloop()
