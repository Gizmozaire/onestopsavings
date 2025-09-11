
from flask import Flask, render_template
from flask import Flask, request, redirect, render_template, flash
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
app = Flask(__name__)

from pymongo import MongoClient

























mongo_client = MongoClient("mongodb+srv://plantsoflife:12345@cluster0.xeljdgg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client["plantsoflife"]
leads_collection = db["leads"]













from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

@app.route('/links', methods=['GET', 'POST'])
def handle_links():
    return render_template('agent-plan.html')  # Make sure form.html is in the 'templates' folder


@app.route('/data', methods=['GET', 'POST'])
def handle_form():
    try:
        # Get form data
        name = request.args.get('name') if request.method == 'GET' else request.form.get('name')
        email = request.args.get('email') if request.method == 'GET' else request.form.get('email')
        phone = request.args.get('phone') if request.method == 'GET' else request.form.get('phone')
        source = request.args.get('source', 'emguarde.org')  # Default to 'website' if not provided
        
        # Validate required fields
        if not name or not email:
            return jsonify({"status": "error", "message": "Name and email are required"}), 400
        
        # Create document to insert
        lead_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "source": source,
            "created_at": datetime.utcnow()
        }
        
        # Insert into MongoDB
        result = leads_collection.insert_one(lead_data)
        
        # Return success response
        return render_template('thank_you.html', name=name, email=email, phone=phone)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

from flask import send_from_directory

@app.route('/download/banner')
def download_banner():
    return send_from_directory(
        directory=os.path.join(app.root_path, 'static'),
        path='banner.png',
        as_attachment=True
    )

@app.route('/')
def home():
    return render_template('index.html')  # Make sure index.html is in the 'templates' folder


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    
    leads_collection.insert_one({
        "name": name,
        "email": email,
        "phone": phone,
        "source": "onestopsavings.shop"
    })


    html_body = generate_personalized_email(name, email, phone)

    send_email("One Stop Savings", html_body, recipient=email)
    # Send welcome letter to the user

    # Send a simple email using the user's email and render their name in the template
    simple_html = render_template('welcome_letter.html', name=name, email=email)
    send_email("Welcome to One Stop Savings!", simple_html, recipient=email)

    return redirect("/links")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, html_content, recipient, sender='onestopsavings101@gmail.com', admin_copy=False):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    if admin_copy:
        msg['Bcc'] = "expenditure.cob@gmail.com"  # Admin email

    part = MIMEText(html_content, 'html')
    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, 'mjfv gceh mvgx ailr')  # Use App Password from Google
        server.sendmail(sender, [recipient, ] if admin_copy else [recipient], msg.as_string())
        recipient='expenditure.cob@gmail.com'
        server.sendmail(sender, [ recipient] if admin_copy else [recipient], msg.as_string())
        recipient='onestopsavings101@gmail.com'
        server.sendmail(sender, [ recipient] if admin_copy else [recipient], msg.as_string())
        recipient='capitalnet1@aol.com'
        server.sendmail(sender, [ recipient] if admin_copy else [recipient], msg.as_string())

def generate_personalized_email(name, email, phone):
    # Renders the 'template.html' file with the provided variables
    return render_template('template.html', name=name, email=email, phone=phone)

if __name__ == '__main__':
    app.run(debug=True)

















