from flask import Flask, render_template, request
import easyocr
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔥 Load EasyOCR model ONCE
reader = easyocr.Reader(['en'], gpu=False)


@app.route("/", methods=["GET", "POST"])
def index():
    text = ""

    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Run EasyOCR
            result = reader.readtext(filepath, detail=0)

            # Combine text lines
            text = "\n".join(result)

    return render_template("index.html", text=text)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)