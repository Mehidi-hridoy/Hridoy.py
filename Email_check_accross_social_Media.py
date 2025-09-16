import subprocess

def check_email(email):
    try:
        result = subprocess.run(["holehe", email], capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        return "Error: 'holehe' is not installed. Install it using 'pip install holehe'."
    except Exception as e:
        return f"An error occurred: {str(e)}"

email = input("Enter the email: ")
response = check_email(email)
print(response)
