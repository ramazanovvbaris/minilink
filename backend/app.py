from flask import Flask, request, redirect, jsonify, render_template_string
import redis
import random
import string

app = Flask(__name__)

# Redis-ə qoşul
r = redis.Redis(host='redis-service', port=6379, decode_responses=True)

# Qısa kod yarat
def qisa_kod_yarat():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def ana_sehife():
    return open('/app/index.html').read() 
    
# URL qısalt
@app.route('/qisalt', methods=['POST'])
def qisalt():
    url = request.form['url']
    kod = qisa_kod_yarat()
    r.set(kod, url)
    return f'''
    <h1>✅ Qısaldıldı!</h1>
    <p>Orijinal: {url}</p>
    <p>Qısa link: <a href="/{kod}">/{kod}</a></p>
    <a href="/">Geri qayıt</a>
    '''

# Qısa linkə keç
@app.route('/<kod>')
def yonlendir(kod):
    url = r.get(kod)
    if url:
        return redirect(url)
    return '<h1>❌ Link tapılmadı!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/health')
def health():
    return 'OK', 200