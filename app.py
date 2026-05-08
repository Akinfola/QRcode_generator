from flask import Flask, request, render_template_string
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium QR Code Generator</title>
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            --card-bg: rgba(255, 255, 255, 0.1);
            --text-color: #ffffff;
            --primary: #00d2ff;
            --primary-hover: #3a7bd5;
        }
        body {
            font-family: 'Inter', system-ui, sans-serif;
            margin: 0;
            padding: 0;
            background: var(--bg-gradient);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            max-width: 400px;
            width: 100%;
        }
        h1 {
            margin-top: 0;
            font-size: 2rem;
            font-weight: 700;
            background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            margin: 15px 0;
            border: none;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 1rem;
            box-sizing: border-box;
            outline: none;
            transition: box-shadow 0.3s ease;
        }
        input[type="text"]:focus {
            box-shadow: 0 0 0 3px rgba(0, 210, 255, 0.5);
        }
        button {
            background: linear-gradient(45deg, var(--primary), var(--primary-hover));
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
        }
        .qr-result {
            margin-top: 30px;
            animation: fadeIn 0.5s ease;
        }
        .qr-result img {
            border-radius: 12px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            max-width: 100%;
            background: white;
            padding: 10px;
        }
        .download-btn {
            background: transparent;
            border: 2px solid var(--primary);
            color: var(--primary);
            margin-top: 10px;
        }
        .download-btn:hover {
            background: var(--primary);
            color: white;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>QR Generator</h1>
        <form method="POST">
            <input type="text" name="data" placeholder="Enter URL or text" value="{{ data }}" required>
            <button type="submit">Generate QR Code</button>
        </form>
        
        {% if qr_b64 %}
        <div class="qr-result">
            <img src="data:image/png;base64,{{ qr_b64 }}" alt="QR Code">
            <a href="data:image/png;base64,{{ qr_b64 }}" download="qrcode.png" style="text-decoration: none;">
                <button class="download-btn">Download QR Code</button>
            </a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    qr_b64 = None
    data = ""
    if request.method == "POST":
        data = request.form.get("data", "")
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            qr_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
    return render_template_string(HTML, qr_b64=qr_b64, data=data)

if __name__ == "__main__":
    try:
        from waitress import serve
        print("Starting production server at http://localhost:5000...")
        serve(app, host="0.0.0.0", port=5000)
    except ImportError:
        print("Waitress not installed. Falling back to development server.")
        app.run(host="0.0.0.0", port=5000, debug=True)
