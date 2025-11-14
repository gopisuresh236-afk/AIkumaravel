from flask import Flask, request, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

# ----------------------- CONFIG -----------------------
TEACH_PASSWORD = "annan"
KNOWLEDGE_FILE = "knowledge.json"

# ------------------- LOAD KNOWLEDGE -------------------
try:
    with open(KNOWLEDGE_FILE, "r") as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    knowledge_base = {}

# ---------------------- HTML -------------------------
html = """
<!DOCTYPE html>
<html>
<head>
<title>AI Chatbot</title>
<style>
body { font-family: Arial; padding: 20px; max-width: 600px; margin: auto; }
input, button { padding: 10px; margin-top: 10px; width: 100%; }
.chat { border: 1px solid #aaa; padding: 15px; height: 300px; overflow-y: scroll; background: #f7f7f7; }
.user { background: #d1ecf1; padding: 5px; border-radius: 5px; margin: 5px 0; }
.bot { background: #f8d7da; padding: 5px; border-radius: 5px; margin: 5px 0; }
button { background: #0275d8; color: white; border: none; cursor: pointer; }
button:hover { background: #025aa5; }
h2 { display: flex; align-items: center; gap: 10px; }
</style>
</head>
<body>

<h2>
    <img src="/static/logo.png" alt="AI Logo" width="100" height="100">
    Dr Kumaravel Govindharasu - KumBot AI (University of Technology and Applied Sciences, ibri, Sultanate of Oman)
</h2>

<div class="chat" id="chat">{{chat|safe}}</div>

<form method="POST">
    <input name="message" placeholder="Type your message..." required>
    <button type="submit" name="action" value="ask">Ask</button>
    <button type="submit" name="action" value="teach_request">Teach</button>
</form>

{% if show_password %}
<form method="POST" style="margin-top:20px;">
    <input type="password" name="password" placeholder="Enter Teach Password" required>
    <input name="teach_data" placeholder="Format: question = answer" required>
    <button type="submit" name="action" value="teach">Submit Teaching</button>
</form>
{% endif %}

<script>
var chatDiv = document.getElementById('chat');
chatDiv.scrollTop = chatDiv.scrollHeight;
</script>

</body>
</html>
"""

# ------------------- CHAT HISTORY ---------------------
chat_history = []

# ------------------- FUNCTIONS -----------------------
def get_response(user_input):
    user_input_lower = user_input.lower()
    
    # Check exact knowledge base
    if user_input_lower in knowledge_base:
        return knowledge_base[user_input_lower]
    
    # Keyword matching
    for key, value in knowledge_base.items():
        for word in key.split():
            if word in user_input_lower:
                return value
    
    return "I don't know the answer. Please teach me!"

def save_knowledge():
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(knowledge_base, f)

# ------------------- ROUTES --------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history
    show_password = False

    if request.method == "POST":
        action = request.form["action"]

        if action == "ask":
            msg = request.form["message"]
            ans = get_response(msg)
            timestamp = datetime.now().strftime("%H:%M")
            chat_history.append(f"<div class='user'>{timestamp} - You: {msg}</div>")
            chat_history.append(f"<div class='bot'>{timestamp} - Bot: {ans}</div>")

        elif action == "teach_request":
            show_password = True

        elif action == "teach":
            pwd = request.form["password"]
            teach_data = request.form["teach_data"]
            timestamp = datetime.now().strftime("%H:%M")

            if pwd != TEACH_PASSWORD:
                chat_history.append(f"<div class='bot'>{timestamp} - Bot: ❌ Incorrect password!</div>")
            else:
                if "=" in teach_data:
                    q, a = teach_data.split("=", 1)
                    knowledge_base[q.strip().lower()] = a.strip()
                    save_knowledge()
                    chat_history.append(f"<div class='bot'>{timestamp} - Bot: ✔ I learned the new answer!</div>")
                else:
                    chat_history.append(f"<div class='bot'>{timestamp} - Bot: Use correct format → question = answer</div>")

    # Show only last 4 messages (2 Q&A)
    last_chats = chat_history[-4:]
    chat_html = "".join(last_chats)

    return render_template_string(html, chat=chat_html, show_password=show_password)

# ------------------- RUN APP -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
