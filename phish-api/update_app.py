import os

app_path = "app.py"
with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports and DB initialization
imports_addition = """
import sqlite3
from datetime import datetime
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT NOT NULL,
            type TEXT NOT NULL,
            result TEXT NOT NULL,
            score INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = [i for i in text if i.isalnum()]
    text = [i for i in y if i not in stopwords.words('english') and i not in string.punctuation]
    y = [ps.stem(i) for i in text]
    return " ".join(y)
"""

model_load_addition = """
try:
    tfidf = pickle.load(open('../sms-email-spam-classifier-main/vectorizer.pkl','rb'))
    email_model = pickle.load(open('../sms-email-spam-classifier-main/model.pkl','rb'))
except Exception as e:
    print("Email model not loaded:", e)
    tfidf = None
    email_model = None
"""

content = content.replace("import pickle", "import pickle\n" + imports_addition)
content = content.replace("model = pickle.load(open('SVM_Model.pkl', 'rb'))", "model = pickle.load(open('SVM_Model.pkl', 'rb'))\n" + model_load_addition)

routes_old = """@app.route('/',methods=["GET","POST"])
def home():
    return render_template("index.html")

@app.route('/post',methods=['POST'])
def predict():
  url=request.form['URL']
  dataPhish=0
  if checkCSV(url)==0:
    dataPhish=0
  else:
    dataPhish=1
  if dataPhish==0:
    return "0"
  else:
    features=featureExtraction(url)
  if features.count(0)==15 or features.count(0)==14:
    prediction=0
  else:
    prediction = model.predict([features])
  if prediction==1 and dataPhish==1:
    return "-1"
  else:
    return "1"
if __name__ == "__main__":
    app.run(debug=True)"""

routes_new = """
@app.route('/')
def home():
    conn = get_db_connection()
    scans = conn.execute('SELECT * FROM scans ORDER BY timestamp DESC LIMIT 5').fetchall()
    total_scans = conn.execute('SELECT COUNT(*) FROM scans').fetchone()[0]
    threats = conn.execute('SELECT COUNT(*) FROM scans WHERE result != "Safe"').fetchone()[0]
    safe_items = conn.execute('SELECT COUNT(*) FROM scans WHERE result = "Safe"').fetchone()[0]
    
    malicious = conn.execute('SELECT COUNT(*) FROM scans WHERE result = "Malicious"').fetchone()[0]
    suspicious = conn.execute('SELECT COUNT(*) FROM scans WHERE result = "Suspicious"').fetchone()[0]
    conn.close()
    
    return render_template("dashboard.html", active_page="dashboard", 
                           scans=scans, total_scans=total_scans, 
                           threats=threats, safe_items=safe_items,
                           malicious=malicious, suspicious=suspicious)

@app.route('/scan-email')
def scan_email_page():
    return render_template("scan_email.html", active_page="scan_email")

@app.route('/scan-url')
def scan_url_page():
    return render_template("scan_url.html", active_page="scan_url")

@app.route('/threat-history')
def threat_history():
    conn = get_db_connection()
    scans = conn.execute('SELECT * FROM scans ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template("threat_history.html", active_page="history", scans=scans)

@app.route('/reports')
def reports():
    return render_template("placeholder.html", active_page="reports", title="Reports")

@app.route('/real-time-protection')
def real_time():
    return render_template("placeholder.html", active_page="real_time", title="Real-time Protection")

@app.route('/settings')
def settings():
    return render_template("placeholder.html", active_page="settings", title="Settings")

@app.route('/api-docs')
def api_docs():
    return render_template("placeholder.html", active_page="api_docs", title="API Documentation")

@app.route('/help-support')
def help_support():
    return render_template("placeholder.html", active_page="help", title="Help & Support")

@app.route('/scan_email_api', methods=['POST'])
def scan_email_api():
    email_content = request.form.get('content', '')
    if not email_content or email_model is None:
        return "error"
        
    transformed = transform_text(email_content)
    vector_input = tfidf.transform([transformed])
    result = email_model.predict(vector_input)[0]
    
    res_text = "Malicious" if result == 1 else "Safe"
    score = 95 if result == 1 else 5
    
    conn = get_db_connection()
    conn.execute('INSERT INTO scans (target, type, result, score) VALUES (?, ?, ?, ?)',
                 (email_content[:50] + "...", 'Email', res_text, score))
    conn.commit()
    conn.close()
    return str(result)

@app.route('/post',methods=['POST'])
def predict():
  url=request.form['URL']
  dataPhish=0
  if checkCSV(url)==0:
    dataPhish=0
  else:
    dataPhish=1
  if dataPhish==0:
    res = "0"
    res_text = "Safe"
  else:
    features=featureExtraction(url)
    if features.count(0)==15 or features.count(0)==14:
      prediction=0
    else:
      prediction = model.predict([features])
      
    if prediction==1 and dataPhish==1:
      res = "-1"
      res_text = "Malicious"
    else:
      res = "1"
      res_text = "Suspicious"
      
  score = 90 if res == "-1" else (50 if res == "1" else 10)
  conn = get_db_connection()
  conn.execute('INSERT INTO scans (target, type, result, score) VALUES (?, ?, ?, ?)',
               (url, 'URL', res_text, score))
  conn.commit()
  conn.close()
  return res

if __name__ == "__main__":
    app.run(debug=True)
"""

if routes_old in content:
    content = content.replace(routes_old, routes_new)
else:
    print("Warning: Old routes block not perfectly matched.")
    
with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
