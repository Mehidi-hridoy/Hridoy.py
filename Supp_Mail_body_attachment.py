import imaplib
import email
from email.header import decode_header
import os
import csv
import re
from bs4 import BeautifulSoup  # For cleaning up HTML
from email.utils import parseaddr  # To extract the email address from the sender

# Gmail IMAP server details
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL_ACCOUNT = "Support@happyhaat.com"
APP_PASSWORD = "iuym zglh nzxr hunp"  # Use the generated App Password

# Folder to save email attachments
ATTACHMENT_FOLDER = "email_attachments"
CSV_FILE = "email_attachments_data.csv"

# Create folder if not exists
if not os.path.exists(ATTACHMENT_FOLDER):
    os.makedirs(ATTACHMENT_FOLDER)

# Function to sanitize filenames
def sanitize_filename(filename):
    # Remove any invalid characters for Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Function to clean up HTML content
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

# Connect to Gmail IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(EMAIL_ACCOUNT, APP_PASSWORD)

# Select the inbox folder
mail.select("inbox")

# Search for all emails
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

# Get the last 100 emails
email_ids = email_ids[-100:]  # Get the last 100 emails

# Open CSV file to save email details
with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Sender", "Subject", "Body", "Attachment Saved"])  # CSV Header

    print("Fetching the last 100 emails...\n")

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse the email
                msg = email.message_from_bytes(response_part[1])
                
                # Extract the sender's email address only (no name, no extra info)
                from_email = parseaddr(msg.get("From"))[1]  # Get only the email address
                subject = msg.get("Subject")
                body = ""
                
                # Initialize attachment flag
                attachment_saved = "No Attachment"
                
                # Check if the email is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        # Check for attachments
                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                # Decode the filename
                                filename, encoding = decode_header(filename)[0]
                                if isinstance(filename, bytes):
                                    filename = filename.decode(encoding if encoding else "utf-8")
                                
                                # Sanitize the filename
                                filename = sanitize_filename(filename)
                                
                                # Save the attachment
                                filepath = os.path.join(ATTACHMENT_FOLDER, filename)
                                try:
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))
                                    
                                    # Set attachment flag
                                    attachment_saved = filename  # Update attachment name
                                except Exception as e:
                                    print(f"Failed to save attachment: {e}")
                        
                        # Extract the email body text
                        if part.get_content_type() == "text/plain":
                            charset = part.get_content_charset()
                            if charset is None:
                                charset = "utf-8"  # Default to 'utf-8' if charset is None
                            body = part.get_payload(decode=True).decode(charset, errors="ignore")
                        elif part.get_content_type() == "text/html":
                            # For HTML content, clean it using BeautifulSoup
                            html_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                            body = clean_html(html_body)  # Clean HTML to text

                else:
                    # For non-multipart emails
                    body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")
                
                # Clean up the body (to remove extra HTML tags if any)
                body = clean_html(body).strip()
                # Write email details (Sender, Subject, Body, Attachment) to CSV
                writer.writerow([from_email, subject, body, attachment_saved])

                print(f"Sender: {from_email}")
                print(f"Subject: {subject}")
                print(f"Body: {body}")
                print(f"Attachment: {attachment_saved}")
                print("-" * 50)

# Close the connection
mail.logout()

print(f"\n✅ Last 100 emails fetched.")
print(f"✅ Email data and attachments saved to '{CSV_FILE}' and '{ATTACHMENT_FOLDER}' folder.")
