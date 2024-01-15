from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load model using environment variables or default
model_name = os.getenv("MODEL_NAME", "unicamp-dl/translation-en-pt-t5")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
enpt_pipeline = pipeline('text2text-generation', model=model, tokenizer=tokenizer, max_length=512, num_beams=5)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        content = request.json
        text_to_translate = content.get('text')
        if not text_to_translate:
            raise ValueError("No text provided for translation")
        
        result = enpt_pipeline(f"translate English to Portuguese: {text_to_translate}")
        return jsonify({"translated_text": result[0]["generated_text"]})
    except Exception as e:
        logging.error(f"Error
during translation: {e}")
return jsonify({"error": str(e)}), 500

if name == 'main':
port = int(os.getenv("PORT", 5000))
app.run(debug=True, port=port)
