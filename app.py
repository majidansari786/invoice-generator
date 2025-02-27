from flask import Flask, render_template, request, send_file
from weasyprint import HTML
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

    # Generate HTML for the PDF
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .details {{ margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .total {{ text-align: right; margin-top: 20px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Invoice</h1>
        </div>
        <div class="details">
            <h3>From:</h3>
            <p>{company_name}</p>
            <p>{company_address.replace('\n', '<br>')}</p>
        </div>
        <div class="details">
            <h3>To:</h3>
            <p>{client_name}</p>
            <p>{client_address.replace('\n', '<br>')}</p>
        </div>
        <table>
            <tr>
                <th>Description</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total</th>
            </tr>
    """

    for item in items:
        html_content += f"""
            <tr>
                <td>{item['description']}</td>
                <td>{item['quantity']}</td>
                <td>${item['price']:.2f}</td>
                <td>${item['total']:.2f}</td>
            </tr>
        """

    html_content += f"""
        </table>
        <div class="total">
            Total: ${total_amount:.2f}
        </div>
    </body>
    </html>
    """

    # Generate PDF
    pdf_bytes = HTML(string=html_content).write_pdf()

    # Serve the PDF
    return send_file(
        io.BytesIO(pdf_bytes),
        download_name="invoice.pdf",
        as_attachment=True,
        mimetype='application/pdf'
    )

if __name__ == "__main__":
    app.run(debug=True)