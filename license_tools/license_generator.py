# VISIT License Generator Tool
# For Software Owner Use Only
# Developed by Dineshkumar Rajendran

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import hashlib
import secrets
import json
from datetime import datetime, timedelta
import os
from cryptography.fernet import Fernet
import base64

class LicenseGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VISIT License Generator - Owner Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Master key for encryption (keep this secret!)
        self.SECRET_KEY = "VISIT_SECRET_KEY"
        
        # Generated licenses storage
        self.generated_licenses = []
        
        self.setup_ui()
        self.load_existing_licenses()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = ttk.Label(self.root, text="VISIT License Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        subtitle_label = ttk.Label(self.root, text="Software Owner Tool - Developed by Dineshkumar Rajendran", 
                                  font=('Arial', 10))
        subtitle_label.pack(pady=5)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # License generation frame
        gen_frame = ttk.LabelFrame(main_frame, text="Generate New License")
        gen_frame.pack(fill='x', pady=10)
        
        # Museum ID
        ttk.Label(gen_frame, text="Museum ID:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.museum_id_entry = ttk.Entry(gen_frame, width=30)
        self.museum_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Museum Name
        ttk.Label(gen_frame, text="Museum Name:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.museum_name_entry = ttk.Entry(gen_frame, width=30)
        self.museum_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Contact Email
        ttk.Label(gen_frame, text="Contact Email:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.email_entry = ttk.Entry(gen_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # License Duration
        ttk.Label(gen_frame, text="License Duration:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        duration_frame = ttk.Frame(gen_frame)
        duration_frame.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        self.duration_var = tk.IntVar(value=365)
        ttk.Radiobutton(duration_frame, text="1 Year", variable=self.duration_var, value=365).pack(side='left')
        ttk.Radiobutton(duration_frame, text="6 Months", variable=self.duration_var, value=180).pack(side='left')
        ttk.Radiobutton(duration_frame, text="3 Months", variable=self.duration_var, value=90).pack(side='left')
        
        # Custom duration
        custom_frame = ttk.Frame(gen_frame)
        custom_frame.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Radiobutton(custom_frame, text="Custom (days):", variable=self.duration_var, value=0).pack(side='left')
        self.custom_days_entry = ttk.Entry(custom_frame, width=10)
        self.custom_days_entry.pack(side='left', padx=5)
        
        # Generate button
        ttk.Button(gen_frame, text="Generate License", 
                  command=self.generate_license).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Generated license display
        license_frame = ttk.LabelFrame(main_frame, text="Generated License")
        license_frame.pack(fill='both', expand=True, pady=10)
        
        # License text area
        self.license_text = tk.Text(license_frame, height=10, wrap=tk.WORD)
        license_scrollbar = ttk.Scrollbar(license_frame, orient="vertical", command=self.license_text.yview)
        self.license_text.configure(yscrollcommand=license_scrollbar.set)
        
        self.license_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        license_scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=10)
        
        ttk.Button(buttons_frame, text="Save License File", 
                  command=self.save_license_file).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="View All Licenses", 
                  command=self.view_all_licenses).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Export Database", 
                  command=self.export_database).pack(side='left', padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to generate licenses")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def generate_secure_key(self):
        """Generate a cryptographically secure key"""
        return secrets.token_urlsafe(32)
    
    def generate_license(self):
        """Generate a new license"""
        # Validate inputs
        museum_id = self.museum_id_entry.get().strip()
        museum_name = self.museum_name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not museum_id or not museum_name or not email:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        # Calculate expiry date
        duration = self.duration_var.get()
        if duration == 0:  # Custom duration
            try:
                duration = int(self.custom_days_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of days")
                return
        
        expiry_date = datetime.now() + timedelta(days=duration)
        
        # Generate unique license key
        license_key = self.generate_secure_key()
        
        # Generate secure hash
        hash_input = f"{museum_id}{expiry_date.strftime('%Y-%m-%d')}{self.SECRET_KEY}"
        secure_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        # Create license data
        license_data = {
            "license_key": license_key,
            "museum_id": museum_id,
            "museum_name": museum_name,
            "contact_email": email,
            "generated_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "expiry": expiry_date.strftime('%Y-%m-%d'),
            "hash": secure_hash,
            "version": "1.0",
            "software": "VISIT Interactive Museum App",
            "developer": "Dineshkumar Rajendran"
        }
        
        # Add to generated licenses
        self.generated_licenses.append(license_data)
        
        # Display license
        self.display_license(license_data)
        
        # Save to database
        self.save_license_database()
        
        self.status_var.set(f"License generated for {museum_name} (Expires: {expiry_date.strftime('%Y-%m-%d')})")
    
    def display_license(self, license_data):
        """Display the generated license"""
        self.license_text.delete(1.0, tk.END)
        
        license_display = f"""
VISIT INTERACTIVE MUSEUM APPLICATION LICENSE
===========================================

License Key: {license_data['license_key']}
Museum ID: {license_data['museum_id']}
Museum Name: {license_data['museum_name']}
Contact Email: {license_data['contact_email']}

Generated: {license_data['generated_date']}
Expires: {license_data['expiry']}
Version: {license_data['version']}

Developer: {license_data['developer']}
Software: {license_data['software']}

Security Hash: {license_data['hash']}

===========================================
IMPORTANT: This license is required for the VISIT application to function.
Save this license as 'license.key' in the VISIT application directory.
Do not share this license key with unauthorized parties.
===========================================
        """
        
        self.license_text.insert(1.0, license_display.strip())
        self.current_license = license_data
    
    def save_license_file(self):
        """Save license to file"""
        if not hasattr(self, 'current_license'):
            messagebox.showerror("Error", "No license generated to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".key",
            filetypes=[("License files", "*.key"), ("JSON files", "*.json"), ("All files", "*.*")],
            initialname="license.key"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_license, f, indent=4)
                messagebox.showinfo("Success", f"License saved to {filename}")
                self.status_var.set(f"License saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save license: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy license to clipboard"""
        license_content = self.license_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(license_content)
        messagebox.showinfo("Success", "License copied to clipboard")
        self.status_var.set("License copied to clipboard")
    
    def view_all_licenses(self):
        """View all generated licenses"""
        if not self.generated_licenses:
            messagebox.showinfo("Info", "No licenses have been generated yet")
            return
        
        # Create new window for license list
        list_window = tk.Toplevel(self.root)
        list_window.title("All Generated Licenses")
        list_window.geometry("900x600")
        
        # Create treeview
        columns = ('Museum ID', 'Museum Name', 'Email', 'Generated', 'Expires', 'Status')
        tree = ttk.Treeview(list_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        # Add data
        for license_data in self.generated_licenses:
            expiry_date = datetime.strptime(license_data['expiry'], '%Y-%m-%d')
            status = "Active" if datetime.now() < expiry_date else "Expired"
            
            tree.insert('', tk.END, values=(
                license_data['museum_id'],
                license_data['museum_name'],
                license_data['contact_email'],
                license_data['generated_date'],
                license_data['expiry'],
                status
            ))
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        button_frame = ttk.Frame(list_window)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        def regenerate_selected():
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                museum_id = item['values'][0]
                for license_data in self.generated_licenses:
                    if license_data['museum_id'] == museum_id:
                        self.display_license(license_data)
                        list_window.destroy()
                        break
        
        ttk.Button(button_frame, text="View Selected", command=regenerate_selected).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Close", command=list_window.destroy).pack(side='right', padx=5)
    
    def export_database(self):
        """Export license database"""
        if not self.generated_licenses:
            messagebox.showinfo("Info", "No licenses to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialname="visit_licenses_database.json"
        )
        
        if filename:
            try:
                export_data = {
                    "export_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "total_licenses": len(self.generated_licenses),
                    "licenses": self.generated_licenses
                }
                
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=4)
                
                messagebox.showinfo("Success", f"Database exported to {filename}")
                self.status_var.set(f"Database exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export database: {str(e)}")
    
    def save_license_database(self):
        """Save license database to local file"""
        try:
            database_file = "visit_license_database.json"
            with open(database_file, 'w') as f:
                json.dump(self.generated_licenses, f, indent=4)
        except Exception as e:
            print(f"Failed to save database: {str(e)}")
    
    def load_existing_licenses(self):
        """Load existing licenses from database"""
        try:
            database_file = "visit_license_database.json"
            if os.path.exists(database_file):
                with open(database_file, 'r') as f:
                    self.generated_licenses = json.load(f)
                self.status_var.set(f"Loaded {len(self.generated_licenses)} existing licenses")
        except Exception as e:
            print(f"Failed to load existing licenses: {str(e)}")
            self.generated_licenses = []
    
    def run(self):
        """Start the license generator"""
        self.root.mainloop()

if __name__ == "__main__":
    generator = LicenseGenerator()
    generator.run()