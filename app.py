from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create/', methods=['POST'])
def create():
    # Extract form data
    company_name = request.form.get('company-name', 'Your Company')
    company_address = request.form.get('company-address', 'No address provided')
    client_name = request.form.get('client-name', 'Client Name')
    client_address = request.form.get('client-address', 'No address provided')

    # Handle multiple items (description, quantity, price)
    items = []
    descriptions = request.form.getlist('item-description')
    quantities = request.form.getlist('item-quantity')
    prices = request.form.getlist('item-price')

    for desc, qty, price in zip(descriptions, quantities, prices):
        if desc and qty and price:  # Only include complete items
            items.append({
                'description': desc,
                'quantity': int(qty),
                'price': float(price),
                'total': int(qty) * float(price)
            })

    # Calculate total
    total_amount = sum(item['total'] for item in items)

    # Generate PDF using ReportLab
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(width / 2, height - 50, "Invoice")

    # Company and Client Details
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 100, "From:")
    pdf.drawString(50, height - 120, company_name)
    pdf.drawString(50, height - 140, company_address)

    pdf.drawString(300, height - 100, "To:")
    pdf.drawString(300, height - 120, client_name)
    pdf.drawString(300, height - 140, client_address)

    # Table Headers
    pdf.setFont("Helvetica-Bold", 12)
    y_position = height - 180
    pdf.drawString(50, y_position, "Description")
    pdf.drawString(250, y_position, "Quantity")
    pdf.drawString(350, y_position, "Unit Price")
    pdf.drawString(450, y_position, "Total")

    pdf.line(50, y_position - 10, 550, y_position - 10)  # Line under headers

    # Table Rows
    pdf.setFont("Helvetica", 12)
    y_position -= 30
    for item in items:
        pdf.drawString(50, y_position, item['description'])
        pdf.drawString(250, y_position, str(item['quantity']))
        pdf.drawString(350, y_position, f"${item['price']:.2f}")
        pdf.drawString(450, y_position, f"${item['total']:.2f}")
        y_position -= 20

    # Total Amount
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(350, y_position - 20, "Total:")
    pdf.drawString(450, y_position - 20, f"₹{total_amount:.2f}")

    # Save PDF
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    # Serve the PDF
    return send_file(
        buffer,
        download_name="invoice.pdf",
        as_attachment=True,
        mimetype='application/pdf'
    )

if __name__ == "__main__":
    app.run(debug=True)
