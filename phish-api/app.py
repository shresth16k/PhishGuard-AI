import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

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

from urllib.parse import urlparse,urlencode
import ipaddress
import re
from bs4 import BeautifulSoup
import urllib
import urllib.request
from datetime import datetime
import requests
import numpy as np
import whois
import tldextract
import string
import datetime
from dateutil.relativedelta import relativedelta
from csv import reader
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
model = pickle.load(open('SVM_Model.pkl', 'rb'))

try:
    tfidf = pickle.load(open('vectorizer.pkl','rb'))
    email_model = pickle.load(open('email_model.pkl','rb'))
except Exception as e:
    print("Email model not loaded:", e)
    tfidf = None
    email_model = None


# 2.Checks for IP address in URL (Have_IP)
def havingIP(url):
  index = url.find("://")
  split_url = url[index+3:]
  index = split_url.find("/")
  split_url = split_url[:index]
  split_url = split_url.replace(".", "")
  counter_hex = 0
  for i in split_url:
    if i in string.hexdigits:
      counter_hex +=1
  total_len = len(split_url)
  having_IP_Address = 0
  if counter_hex >= total_len:
    having_IP_Address = 1
  return having_IP_Address

# 3.Checks the presence of @ in URL (Have_At)
sc=['@','~','`','!', '$','%','&']
def haveAtSign(url):
  flag=0
  for i in range(len(sc)):
    if sc[i] in url:
      at = 1
      flag=1
      break
  if flag==0:
    at = 0
  return at

# 4.Finding the length of URL and categorizing (URL_Length)
def getLength(url):
  if len(url) < 54:
    length = 0
  else:
    length = 1
  return length

# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth

# 6.Checking for redirection '//' in the url (Redirection)
def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0

# 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
def httpDomain(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0

#listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0

# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate



# 11.DNS Record availability (DNS_Record)
# obtained in the featureExtraction function itself

# 12.Web traffic (Web_Traffic)
def web_traffic(url):
    try:
      extract_res = tldextract.extract(url)
      url_ref = extract_res.domain + "." + extract_res.suffix
      html_content = requests.get("https://www.alexa.com/siteinfo/" + url_ref).text
      soup = BeautifulSoup(html_content, "lxml")
      value = str(soup.find('div', {'class': "rankmini-rank"}))[42:].split("\n")[0].replace(",", "")
      if not value.isdigit():
        return 1
      value = int(value)
      if value < 100000:
        return 0
      else:
        return 1
    except:
        return 1

# 13.Survival time of domain: The difference between termination time and creation time (Domain_Age)
def domainAge(url):
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain + "." + extract_res.suffix
  try:
    whois_res = whois.whois(url)
    if datetime.datetime.now() > whois_res["creation_date"][0] + relativedelta(months=+6):
      return 0
    else:
      return 1
  except:
    return 1

# 14.End time of domain: The difference between termination time and current time (Domain_End)
def domainEnd(domain_name):
  expiration_date = domain_name.expiration_date
  if isinstance(expiration_date,str):
      try:
        expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
      except:
        end=1
  if (expiration_date is None):
      end=1
  elif (type(expiration_date) is list):
      today = datetime.datetime.now()
      domainDate = abs((expiration_date[0] - today).days)
      if ((domainDate/30) < 6):
        end = 1
      else:
        end=0
  else:
      today = datetime.datetime.now()
      domainDate = abs((expiration_date - today).days)
      if ((domainDate/30) < 6):
        end = 1
      else:
        end=0
  return end

# 15. IFrame Redirection (iFrame)
def iframe(response):
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return 0
      else:
          return 1

# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response):
  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return 1
    else:
      return 0

# 18.Checks the number of forwardings (Web_Forwards)
def forwarding(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1

#16. Extra feature checks url exists in popular websites data
def checkCSV(url):
  flag=0
  try:
    checkURL=urlparse(url).netloc
  except:
    return 1
  with open('Web_Scrapped_websites.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        if row[0]==checkURL:
            flag=0
            break
        else:
            flag=1
  if flag==0:
      return 0
  else:
      return 1

def featureExtraction(url):

  features = []
  #Address bar based features (10)
  #features.append(getDomain(url))
  features.append(havingIP(url))
  features.append(haveAtSign(url))
  features.append(getLength(url))
  features.append(getDepth(url))
  features.append(redirection(url))
  features.append(httpDomain(url))
  features.append(tinyURL(url))
  features.append(prefixSuffix(url))

  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(dns)
  features.append(web_traffic(url))
  features.append(1 if dns == 1 else domainAge(url))
  features.append(1 if dns == 1 else domainEnd(domain_name))

  # HTML & Javascript based features
  try:
    response = requests.get(url)
  except:
    response = ""

  features.append(iframe(response))
  features.append(mouseOver(response))
  features.append(forwarding(response))

  return features


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

