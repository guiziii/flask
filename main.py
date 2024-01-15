from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("unicamp-dl/translation-en-pt-t5")
model = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/translation-en-pt-t5")
enpt_pipeline = pipeline('text2text-generation', model=model, tokenizer=tokenizer, max_length=512, num_beams=5)


@app.route('/translate', methods=['POST'])
def translate():
    content = request.json
    text_to_translate = content['text']
    result = enpt_pipeline(f"translate English to Portuguese: {text_to_translate}")
    return jsonify({"translated_text": result[0]["generated_text"]})


if __name__ == '__main__':
    app.run(debug=True)
