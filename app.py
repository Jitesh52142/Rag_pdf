from flask import Flask, render_template, request
from pdf_utils import extract_text_from_pdf, chunk_text
from rag_pipeline import store_chunks, generate_answer

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None

    if request.method == "POST":

        if "pdf" in request.files:
            file = request.files["pdf"]
            text = extract_text_from_pdf(file)
            chunks = chunk_text(text)
            store_chunks(chunks)
            answer = "PDF processed successfully."

        elif "question" in request.form:
            question = request.form["question"]
            answer = generate_answer(question)

    return render_template("index.html", answer=answer)


if __name__ == "__main__":
    app.run(debug=True)