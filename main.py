import pandas as pd
from simple_salesforce import Salesforce

# Step 1: Salesforce Authentication
# Replace these with your Salesforce credentials
sf_username = 'honestopedia@gmail.com'  
sf_password = 'Ahmad.0912'  
sf_security_token = 'SAUn8ZUIN53mhaBuK9Fb19xQ'  

sf = Salesforce(username=sf_username, password=sf_password, security_token=sf_security_token)

csv_file = 'UMHCADirectoryMaster.csv'  # Path to your CSV file (e.g., 'C:/path/to/your/companies_data.csv')

# Read the CSV file into a DataFrame
data = pd.read_csv(csv_file)

# Step 3: Loop Through Data and Add Records to Salesforce
for index, row in data.iterrows():
    # Prepare company information (Account in Salesforce)
    company_record = {
        'Name': row['Company Name'],  # Company name
        'Website': row['Website'],  # Company website
        'Phone': row['Phone Number'],  # Company phone number
        'BillingStreet': row['Address']  # Company address
    }

    try:
        # Insert Company (Account) into Salesforce
        account = sf.Account.create(company_record)
        account_id = account.get('id')
        print(f"Account '{row['Company Name']}' created with ID: {account_id}")

        # Prepare contact information (Contact in Salesforce)
        contact_name_parts = row['Contact Name'].split()  # Split contact name into parts
        contact_record = {
            'FirstName': contact_name_parts[0],  # First name (first word of Contact Name)
            'LastName': contact_name_parts[-1] if len(contact_name_parts) > 1 else '',  # Last name (last word of Contact Name)
            'Email': row['Email'],  # Contact email
            'Phone': row['Phone Number'],  # Contact phone number
            'AccountId': account_id  # Link contact to the created account
        }

        # Insert Contact into Salesforce
        contact = sf.Contact.create(contact_record)
        contact_id = contact.get('id')
        print(f"Contact '{row['Contact Name']}' created with ID: {contact_id}")

    except Exception as e:
        print(f"Error creating record for {row['Company Name']}: {str(e)}")
