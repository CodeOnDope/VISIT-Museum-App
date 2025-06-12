# Simple License Generator for VISIT
# Developed by Dineshkumar Rajendran
# This version avoids GUI issues

import json
import hashlib
import secrets
from datetime import datetime, timedelta
import os

def generate_license():
    """Generate a license with user input"""
    
    print("="*50)
    print("VISIT License Generator")
    print("Developed by Dineshkumar Rajendran")
    print("="*50)
    
    # Get museum details
    museum_id = input("Enter Museum ID (e.g., MUSEUM_NYC_001): ").strip()
    if not museum_id:
        museum_id = "DEFAULT_MUSEUM_001"
    
    museum_name = input("Enter Museum Name: ").strip()
    if not museum_name:
        museum_name = "Default Museum"
    
    contact_email = input("Enter Contact Email: ").strip()
    if not contact_email:
        contact_email = "contact@museum.com"
    
    # License duration
    print("\nLicense Duration Options:")
    print("1. 1 Year (365 days)")
    print("2. 6 Months (180 days)")
    print("3. 3 Months (90 days)")
    print("4. Custom days")
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        days = 365
    elif choice == "2":
        days = 180
    elif choice == "3":
        days = 90
    elif choice == "4":
        try:
            days = int(input("Enter number of days: "))
        except ValueError:
            days = 365
            print("Invalid input, defaulting to 365 days")
    else:
        days = 365
        print("Invalid choice, defaulting to 365 days")
    
    # Generate license
    generated_date = datetime.now()
    expiry_date = generated_date + timedelta(days=days)
    license_key = secrets.token_urlsafe(32)
    
    # Create license data
    license_data = {
        "license_key": license_key,
        "museum_id": museum_id,
        "museum_name": museum_name,
        "contact_email": contact_email,
        "generated_date": generated_date.strftime('%Y-%m-%d %H:%M:%S'),
        "expiry": expiry_date.strftime('%Y-%m-%d'),
        "version": "1.0",
        "software": "VISIT Interactive Museum App",
        "developer": "Dineshkumar Rajendran"
    }
    
    # Calculate hash
    hash_input = f"{museum_id}{expiry_date.strftime('%Y-%m-%d')}VISIT_SECRET_KEY"
    license_data['hash'] = hashlib.sha256(hash_input.encode()).hexdigest()
    
    # Display license info
    print("\n" + "="*50)
    print("LICENSE GENERATED SUCCESSFULLY")
    print("="*50)
    print(f"Museum ID: {museum_id}")
    print(f"Museum Name: {museum_name}")
    print(f"Contact Email: {contact_email}")
    print(f"Generated: {license_data['generated_date']}")
    print(f"Expires: {license_data['expiry']} ({days} days)")
    print(f"License Key: {license_key}")
    print(f"Hash: {license_data['hash']}")
    
    # Save license
    save_choice = input("\nSave license file? (y/n): ").strip().lower()
    if save_choice in ['y', 'yes']:
        # Ask for save location
        save_path = input("Enter save path (or press Enter for current directory): ").strip()
        if not save_path:
            save_path = "."
        
        filename = input("Enter filename (or press Enter for 'license.key'): ").strip()
        if not filename:
            filename = "license.key"
        
        if not filename.endswith('.key'):
            filename += '.key'
        
        full_path = os.path.join(save_path, filename)
        
        try:
            with open(full_path, 'w') as f:
                json.dump(license_data, f, indent=4)
            
            print(f"\n✅ License saved to: {full_path}")
            
            # Verify saved file
            with open(full_path, 'r') as f:
                verify_data = json.load(f)
            
            if isinstance(verify_data, dict):
                print("✅ License file format verified (dictionary)")
            else:
                print(f"❌ Warning: License saved in wrong format: {type(verify_data)}")
                
            # Save to database
            save_to_database(license_data)
            
        except Exception as e:
            print(f"❌ Error saving license: {e}")
    
    return license_data

def save_to_database(license_data):
    """Save license to database file"""
    database_file = "visit_license_database.json"
    
    try:
        # Load existing database
        if os.path.exists(database_file):
            with open(database_file, 'r') as f:
                database = json.load(f)
        else:
            database = []
        
        # Add new license
        database.append(license_data)
        
        # Save database
        with open(database_file, 'w') as f:
            json.dump(database, f, indent=4)
        
        print(f"✅ License added to database ({len(database)} total licenses)")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not save to database: {e}")

def list_licenses():
    """List all generated licenses"""
    database_file = "visit_license_database.json"
    
    if not os.path.exists(database_file):
        print("No licenses found in database")
        return
    
    try:
        with open(database_file, 'r') as f:
            database = json.load(f)
        
        print(f"\nFound {len(database)} licenses:")
        print("-" * 80)
        
        for i, license_data in enumerate(database, 1):
            expiry_date = datetime.strptime(license_data['expiry'], '%Y-%m-%d')
            status = "Active" if datetime.now() < expiry_date else "Expired"
            
            print(f"{i}. {license_data['museum_name']} ({license_data['museum_id']})")
            print(f"   Email: {license_data['contact_email']}")
            print(f"   Generated: {license_data['generated_date']}")
            print(f"   Expires: {license_data['expiry']} - {status}")
            print("-" * 80)
            
    except Exception as e:
        print(f"Error reading database: {e}")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("VISIT License Generator Menu")
        print("="*50)
        print("1. Generate New License")
        print("2. List All Licenses")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            generate_license()
        elif choice == "2":
            list_licenses()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()