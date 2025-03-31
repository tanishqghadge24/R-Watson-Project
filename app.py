from flask import Flask, render_template, request
import random
import string
import hashlib

app = Flask(__name__)

def generate_mapping(key: str):
    """Generate encryption & decryption mappings based on a given key."""
    if not key:
        return None, None  
    
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    random.seed(key_hash)
    
    original_letters = list(string.ascii_lowercase)
    shuffled_letters = original_letters[:]
    random.shuffle(shuffled_letters)
    
    encryption_dict = dict(zip(original_letters, shuffled_letters))
    decryption_dict = {v: k for k, v in encryption_dict.items()}
    
    return encryption_dict, decryption_dict

def transform_message(message: str, mapping: dict[str, str]):
    """Transform a message using a given mapping."""
    return ''.join(mapping.get(char, char) for char in message)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    error = ""

    if request.method == "POST":
        message = request.form.get("message", "").strip().lower()
        key = request.form.get("key", "").strip()
        action = request.form.get("action", "")

        if not message:
            error = "Error: Message cannot be empty!"
        elif not key:
            error = "Error: Key cannot be empty!"
        else:
            encryption_dict, decryption_dict = generate_mapping(key)

            if encryption_dict is None or decryption_dict is None:
                error = "Error: Invalid Key!"
            elif action == "encrypt":
                result = transform_message(message, encryption_dict)
            elif action == "decrypt":
                decrypted_text = transform_message(message, decryption_dict)
                
               
                if transform_message(decrypted_text, encryption_dict) != message:
                    error = "Error: Invalid Key! Decryption failed."
                else:
                    result = decrypted_text
            else:
                error = "Error: Invalid action specified."

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
