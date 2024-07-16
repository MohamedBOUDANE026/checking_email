import smtplib
from email_validator import validate_email, EmailNotValidError  # type: ignore
import dns.resolver  # type: ignore
import sqlite3
import random
import string

# Fonction pour créer la base de données et insérer des données aléatoires


def create_database():
    conn = sqlite3.connect('email_validation.db')
    c = conn.cursor()

    # Créer la table
    c.execute('''CREATE TABLE IF NOT EXISTS email_validation
                (email TEXT, syntax_result TEXT, mx_result TEXT, deliverability_result TEXT)''')

    # Insérer des données de test aléatoires
    for _ in range(10):
        email = ''.join(random.choices(
            string.ascii_lowercase, k=5)) + '@example.com'
        c.execute("INSERT INTO email_validation (email, syntax_result, mx_result, deliverability_result) VALUES (?, ?, ?, ?)",
                  (email, None, None, None))
    conn.close()

# Étape 1 : Valider la syntaxe de l'email


def validate_email_syntax(email):
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError as e:
        return f"Invalid email syntax: {e}"

# Étape 2 : Vérifier les enregistrements MX du domaine de l'email


def check_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange
        return f"MX record found: {mx_record}"
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout) as e:
        return f"No MX record found for domain {domain}: {e}"
    except Exception as e:
        return f"An error occurred while checking MX record for domain {domain}: {e}"

# Étape 3 : Vérifier la délivrabilité de l'email


def verify_email_deliverability(email):
    domain = email.split('@')[1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange.to_text()

        with smtplib.SMTP(mx_record, 25, timeout=30) as server:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.mail('test@example.com')
            code, message = server.rcpt(email)

            if code == 250:
                return f"Email {email} is deliverable."
            else:
                return f"Email {email} is not deliverable: {message}"
    except smtplib.SMTPConnectError as e:
        return f"SMTP connect error: {e}"
    except smtplib.SMTPServerDisconnected as e:
        return f"SMTP server disconnected: {e}"
    except smtplib.SMTPException as e:
        return f"SMTP error checking deliverability for {email}: {e}"
    except Exception as e:
        return f"Error checking deliverability for {email}: {e}"

# Fonction pour enregistrer les résultats dans la base de données


def store_results_in_db(email, syntax_result, mx_result, deliverability_result):
    conn = sqlite3.connect('email_validation.db')
    c = conn.cursor()

    c.execute("UPDATE email_validation SET syntax_result = ?, mx_result = ?, deliverability_result = ? WHERE email = ?",
              (syntax_result, mx_result, deliverability_result, email))

    conn.commit()
    conn.close()

# Fonction principale pour valider un email et stocker les résultats dans la base de données


def validate_email_address(email):
    syntax_result = validate_email_syntax(email)
    print(f"Syntax validation result: {syntax_result}")

    if "Invalid email syntax" in syntax_result:
        mx_result = None
        deliverability_result = None
    else:
        domain = email.split('@')[1]
        mx_result = check_mx_record(domain)
        print(f"MX record check result: {mx_result}")

        if "No MX record found" in mx_result:
            deliverability_result = None
        else:
            deliverability_result = verify_email_deliverability(email)
            print(f"Deliverability check result: {deliverability_result}")

    store_results_in_db(email, syntax_result, mx_result, deliverability_result)


# Créer la base de données avec des données aléatoires
create_database()

# Tester les fonctions avec les emails de la base de données
if __name__ == "__main__":
    conn = sqlite3.connect('email_validation.db')
    c = conn.cursor()

    c.execute("SELECT email FROM email_validation")
    emails = c.fetchall()

    for email in emails:
        validate_email_address(email[0])

    conn.close()
