import tempfile
from flask import Flask, request, send_file, jsonify, after_this_request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
import os
import subprocess
from backend.ocr import predict_latex

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "math_formulas")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/compile", methods=["POST"])
def compile_latex():
    tex_code = request.form["code"]

    temp_dir = tempfile.mkdtemp()  # Create a temporary directory
    tex_file = os.path.join(temp_dir, "document.tex")
    pdf_file = os.path.join(temp_dir, "document.pdf")

    with open(tex_file, "w") as f:
        f.write(tex_code)

    try:
        subprocess.run(["tectonic", tex_file], check=True)

        # Schedule cleanup after the response is sent
        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(tex_file):
                    os.remove(tex_file)
                if os.path.exists(pdf_file):
                    os.remove(pdf_file)
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)  # Remove the temporary directory
            except Exception as e:
                print(f"Error during cleanup: {e}")
            return response

        return send_file(
            os.path.abspath(pdf_file),
            mimetype="application/pdf",
            download_name="output.pdf",
            as_attachment=True,
            conditional=True,
        )
    except subprocess.CalledProcessError:
        return "Failed to compile LaTeX", 500


@app.route("/ocr", methods=["POST"])
def ocr_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    filename = secure_filename(image.filename)
    path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
    image.save(path)
    print("Image saved to:", path)
    print("Exists?", os.path.exists(path))

    try:
        latex = predict_latex(path)
        return jsonify({"latex": latex})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(path):
            os.remove(path)


@app.route("/", methods=["GET"])
def index_ui():
    ui_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    return send_file(ui_path)


if __name__ == "__main__":  # pragma: no cover
    # dummy = Image.new("RGB", (10, 10), color="white")
    # _ = predictor([dummy])
    app.run(host="127.0.0.1", port=5050, debug=True, use_reloader=False)
