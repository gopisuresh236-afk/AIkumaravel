from flask import Flask, request, render_template_string

app = Flask(__name__)

knowledge_base = {}
TEACH_PASSWORD = "Anna2026!"

html = """
<!DOCTYPE html>
<html>
<head>
<title>AI Chatbot</title>
<style>
body { font-family: Arial; padding: 20px; max-width: 600px; margin: auto; }
input, button { padding: 10px; margin-top: 10px; width: 100%; }
.chat { border: 1px solid #aaa; padding: 15px; height: 300px; overflow-y: scroll; background: #f7f7f7; }
button { background: #0275d8; color: white; border: none; cursor: pointer; }
button:hover { background: #025aa5; }
</style>
</head>
<body>
<img src="logo.png" alt="AI Logo" width="100" height="36">
<h2> Dr Kumaravel Govindharasu AI  (UTAS - Ibri)</h2>

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

</body>
</html>
"""

chat_history = ""

def get_response(user_input):
    user_input = user_input.lower()
    if user_input in knowledge_base:
        return knowledge_base[user_input]
    for key, value in knowledge_base.items():
        for word in key.split():
            if word in user_input:
                return value
    return "I don't know the answer. Please teach me!"

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history
    show_password = False
    if request.method == "POST":
        action = request.form["action"]
        if action == "ask":
            msg = request.form["message"]
            ans = get_response(msg)
            chat_history += f"You: {msg}<br>Bot: {ans}<br><br>"
        elif action == "teach_request":
            show_password = True
        elif action == "teach":
            pwd = request.form["password"]
            teach_data = request.form["teach_data"]
            if pwd != TEACH_PASSWORD:
                chat_history += "Bot: ❌ Incorrect password!<br><br>"
            else:
                if "=" in teach_data:
                    q, a = teach_data.split("=", 1)
                    knowledge_base[q.strip().lower()] = a.strip()
                    chat_history += "Bot: ✔ I learned the new answer!<br><br>"
                else:
                    chat_history += "Bot: Use correct format → question = answer<br><br>"
    return render_template_string(html, chat=chat_history, show_password=show_password)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
