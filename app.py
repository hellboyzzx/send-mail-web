import os
import requests
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        to_email = request.form["to"]
        subject = request.form["subject"]
        content = request.form["content"]

        attachment = request.files.get("attachment")
        file_data = None

        if attachment and allowed_file(attachment.filename):
            filename = secure_filename(attachment.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            attachment.save(filepath)
            with open(filepath, "rb") as f:
                file_data = f.read()
            os.remove(filepath)

        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }

        message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": content
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": to_email
                        }
                    }
                ]
            },
            "saveToSentItems": "true"
        }

        if file_data:
            import base64
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            message["message"]["attachments"] = [
                {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": attachment.filename,
                    "contentBytes": encoded_file
                }
            ]

        response = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                                 headers=headers, json=message)

        if response.status_code == 202:
            flash("✅ Email đã được gửi thành công!", "success")
        else:
            flash(f"❌ Gửi thất bại: {response.status_code} - {response.text}", "danger")

        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Correct config for Render
    app.run(host="0.0.0.0", port=port)
