from flask import Flask, request, render_template_string, jsonify
from krr_engine import assess
app = Flask(__name__)

HTML = '''<!doctype html><html><head><meta charset="utf-8"><title>Smart Wellness Advisor</title>
<style>body{font-family:Arial;padding:20px} label{display:block;margin:8px 0} input,select{padding:6px;width:240px}
.btn{margin-top:12px;padding:8px 12px}</style></head><body>
<h2>Smart Wellness Advisor (Demo)</h2>
<form method="post" action="/assess">
  <label>Age: <input name="age" type="number" value="30" required></label>
  <label>BMI: <input name="bmi" step="0.1" value="25.0" required></label>
  <label>Sleep hours: <input name="sleep_hours" step="0.1" value="7.0" required></label>
  <label>Activity level:
    <select name="activity_level">
      <option value="low">low</option><option value="moderate" selected>moderate</option><option value="high">high</option>
    </select>
  </label>
  <label>Water intake (L): <input name="water_intake_l" step="0.1" value="1.8" required></label>
  <label>Sugar intake:
    <select name="sugar_intake"><option value="low" selected>low</option><option value="high">high</option></select>
  </label>
  <label>Stress level:
    <select name="stress_level"><option value="low" selected>low</option><option value="medium">medium</option><option value="high">high</option></select>
  </label>
  <button class="btn" type="submit">Assess</button>
</form>
{% if result %}
  <hr>
  <h3>Result</h3>
  <p><strong>ML prediction:</strong> {{ result['ml_label'] }} (probs: {{ result['ml_probs'] }})</p>
  <p><strong>Final label after rules:</strong> {{ result['final_label'] }}</p>
  <p><strong>Recommendations:</strong></p>
  <ul>{% for r in result['recommendations'] %}<li>{{ r }}</li>{% endfor %}</ul>
{% endif %}
</body></html>'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML)

@app.route('/assess', methods=['POST'])
def assess_form():
    data = {k: request.form.get(k) for k in ['age','bmi','sleep_hours','activity_level','water_intake_l','sugar_intake','stress_level']}
    data['age']=int(data['age']); data['bmi']=float(data['bmi']); data['sleep_hours']=float(data['sleep_hours']); data['water_intake_l']=float(data['water_intake_l'])
    result = assess(data)
    return render_template_string(HTML, result=result)

@app.route('/api/assess', methods=['POST'])
def api_assess():
    payload = request.get_json(force=True)
    for k in ['age','bmi','sleep_hours','water_intake_l','activity_level','sugar_intake','stress_level']:
        if k not in payload:
            payload[k] = { 'age':30,'bmi':25.0,'sleep_hours':7.0,'water_intake_l':1.8 }.get(k, 'low')
    res = assess(payload)
    return jsonify(res)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
