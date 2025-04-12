from flask import Flask, jsonify, request, send_from_directory
import random
import string
import time
import os

app = Flask(__name__, static_folder='static')

users = {}
inbox = {}
DOMAIN = "safemode.com"

def generate_email():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    email = f"{name}@{DOMAIN}"
    users[email] = time.time()
    inbox[email] = []
    return email

@app.route("/generate", methods=["GET"])
def generate():
    email = generate_email()
    return jsonify({"email": email})

@app.route("/inbox/<email>", methods=["GET"])
def get_inbox(email):
    email_full = email if "@" in email else f"{email}@{DOMAIN}"
    if email_full not in inbox:
        return jsonify({"error": "Email not found"}), 404
    return jsonify({"inbox": inbox[email_full]})

@app.route("/send", methods=["POST"])
def send_email():
    data = request.json
    to = data.get("to")
    subject = data.get("subject", "No Subject")
    body = data.get("body", "")

    if to not in inbox:
        return jsonify({"error": "Recipient not found"}), 404

    inbox[to].append({
        "subject": subject,
        "body": body,
        "timestamp": time.time()
    })
    return jsonify({"status": "sent"})

@app.route("/")
def
