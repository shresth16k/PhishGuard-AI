<div align="center">
  <img src="icons/logo.png" alt="PhishGuard AI Logo" width="200">
</div>

<p><strong>-: AI-enabled Phishing link Detection and Alert System :-</strong></p>
<h1>Table of content </h1>
<ul>
<li>Introduction.</li>
<li>Installation.</li>
<li>Directory Tree.</li>
<li>Terminology used.</li>
<li>Result.</li>
<li>Conclusion.</li>
</ul>
<h2>INTRODUCTION</h2>
<p>
With the increasing number of crimes, the crime detection tools have also increased at an alarming rate. On the 3rd of March, the economic times of India mentioned that:
                About 30 crore people are vulnerable to phishing attacks in India, of which 5 lakh potentially fall prey to scamsters. That's why we came up with the idea of <strong>PhishGuard AI</strong>. It is a Phishing Links Detection and Alert system designed to help individuals and organizations protect themselves from phishing attacks. Phishing attacks are a common and growing threat to personal and business security, and they can result in the loss of sensitive information, financial loss, and other consequences. By developing a solution that can detect and alert users of potential phishing attacks across various digital channels, we can provide an additional layer of security and protection. Ultimately, the goal of developing a solution like this is to empower individuals and organizations to protect themselves from phishing attacks and minimize the risk of data breaches, financial loss, and other negative consequences.
<br><br>
<strong>Developed by:</strong> Shresth Kesarwani
  
  <br>
  <h3>UI Proof & Screenshots</h3>
  <div style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
    <img src="assets/dashboard.png" alt="Dashboard UI" width="800">
    <img src="assets/scan_url.png" alt="Scan URL UI" width="800">
    <img src="assets/scan_email.png" alt="Scan Email UI" width="800">
  </div>

</p>
<h2>Installation</h2>
<ol>
  <li> Clone the repository or download the zip file and extract it.</li>
  <li> Open a terminal and navigate to the <code>phish-api</code> directory.</li> 
  <li> Install the required Python dependencies by running <code>pip install -r requirements.txt</code>.</li>
  <li> Start the Flask application by running <code>python app.py</code>.</li>
  <li> Open your web browser and navigate to <code>http://127.0.0.1:5000</code> to view the PhishGuard AI dashboard.</li>
</ol>

<h2>Directory tree</h2>
<p>
  
  ```bash
  ├── frontend
  │   ├── icons
  │   │   ├── 128x128.png
  │   │   ├── 16x16.png
  │   │   ├── 32x32.png
  │   │   ├── 48x48.png
  │   │   └── url_list.pdf
  │   ├── js
  │   │   ├── jquery.js
  │   │   └── plugin_ui.js
  │   ├── main.js
  │   ├── manifest.json
  │   ├── plugin_ui.css
  │   ├── plugin_ui.html
  │   ├── README.md
  │   ├── style.css
  │   ├── tempstorage.json
  │   └── test.html
  ├── LICENSE
  ├── phish-api
  │   ├── app.py
  │   ├── app.yaml
  │   ├── Procfile
  │   ├── __pycache__
  │   │   ├── app.cpython-310.pyc
  │   │   └── app.cpython-38.pyc
  │   ├── README.md
  │   ├── requirements.txt
  │   ├── SVM_Model.pkl
  │   └── Web_Scrapped_websites.csv
  ├── README.md
  └── sms-email-spam-classifier-main
      ├── app.py
      ├── model.pkl
      ├── nltk.txt
      ├── Procfile
      ├── requirements.txt
      ├── setup.sh
      ├── sms-spam-detection.ipynb
      ├── spam.csv
      └── vectorizer.pkl
  ```
</p>

<h3>Terminology Used</h3>
<p><ul>
<li>Support Vector Machine (SVM)-<br>Support vector machines (SVMs) is used for the classification of both linear and nonlinear data.</li>

<li>Decision Tree-<br>A decision tree is a directed, acyclic graph with
two types of nodes, namely; internal nodes that represents a test and terminal node holds a class label.</li>

<li>K-Nearest Neighbour-<br>These are distance-based comparisons that intrinsically assign equal weights to each attribute.</li>
<li>Rotation Forest (RoF)-<br> Rotation Forest (RoF) is an ensemble classifier in which the training data is created by randomly
splitting the feature set into K subsets and Principal.</li>
  <li>Component Analysis (PCA) is applied to each subset for any base classifier.</li>

<li>Random Forests (RF)-<br>Random Forests can be built in tandem with random attribute selection using bagging. Random Forests follow an ensemble approach to learning, that is a divide and
  conquer approach for improving performance.</li>
</ul></p>

<h3>Result </h3>
<p>Accuracy of various model used for Phishing detection</p>
<table>
  <tr>
    <th></th>
    <th>Algorithm</th>
    <th>Accuracy</th>
    <th>Precision</th>
    <th>Accuracy_max_ft_3000</th>
   
  </tr>
  <tr>
     <td>0</td>
     <td>KN</td>
     <td>  0.905222 </td>
     <td> 1.000000  </td>
     <td>  0.905222 </td>
  </tr>
   <tr>
     <td>1</td>
     <td>  NB </td>
     <td>  0.978723 </td>
     <td>  1.000000 </td>
     <td> 0.971954</td>
     
  </tr>
   <tr>
     <td>2</td>
     <td> ETC	</td>
     <td>  0.979691  </td>
     <td> 0.991453</td>
     <td>0.979691</td>
   
  </tr>
   <tr>
     <td>3</td>
     <td> RF</td>
     <td> 0.975822 </td>
     <td>0.990826</td>
     <td>0.975822  </td>
    
  </tr>
  <tr>
     <td>4</td>
     <td> SVC</td>
     <td> 0.971954</td>
     <td>  0.974138</td>
     <td> 0.974855</td>
    
  </tr>
   <tr>
     <td>5</td>
     <td> AdaBoost</td>
     <td>0.961315</td>
     <td>0.954128 </td>
     <td> 0.961315</td>
    
  </tr>
   <tr>
     <td>6</td>
     <td> xgb </td>
     <td> 0.968085 </td>
     <td>0.950413</td>
     <td> 0.968085</td>
    
  </tr>
   <tr>
     <td>7</td>
     <td>   LR </td>
     <td> 0.967118 </td>
     <td>0.940000  </td>
     <td> 0.956480</td>
    
  </tr>
  
   <tr>
     <td>8</td>
     <td> GBDT</td>
     <td>  0.946809   </td>
     <td> 0.931373 </td>
     <td>  0.959381</td>
    
  </tr>
   <tr>
     <td>9</td>
     <td>BgC </td>
     <td>0.959381</td>
     <td> 0.861538 </td>
     <td> 0.959381 </td>
    
  </tr>
   <tr>
     <td>10</td>
     <td> DT</td>
     <td>  0.932302</td>
     <td> 0.838095</td>
     <td>0.931335</td>
    
  </tr>
  
 </table>
 <h3>Conclusion</h3>
 <p>The final takeaway from this project is to explore various machine learning models, perform Exploratory Data Analysis on phishing dataset and understanding their features.
Gradient Boosting Classifier correctly classify URL up to 95.6% respective classes and hence reduces the chance of malicious attachments.</p>
