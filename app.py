from flask import Flask, request, jsonify, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from weasyprint import HTML
import io
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'abhasbvhbb82y4`92r1ubbu1bru2asfbab'

db = SQLAlchemy(app)

class Invoices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.Text)
    date_created = db.Column(db.DateTime, server_default=db.func.now())

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create/', methods=['POST'])
def create():
    html = render_template('index.html')
    pdf = HTML(string=html).write_pdf("output.pdf")
    return send_file(
        io.BytesIO(pdf),
        download_name="invoice.pdf",
        as_attachment=True,
        mimetype='application/pdf'
    )

@app.route('/bills/')
def bill():
    return render_template('bill.html')

if __name__ == '__main__':
    app.run(debug=True)
