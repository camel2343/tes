from flask import Flask, request, redirect, url_for
import json
import os

app = Flask(__name__)

# JSON dosyasının yolu
JSON_FILE = 'soz.json'

# JSON dosyasından verileri yükle
def load_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Geçersiz JSON formatı. Boş bir sözlük döndürülüyor.")
            return {}
    return {}

# Verileri JSON dosyasına yaz
def save_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Geçici veri tabanı (sözlük yapısında tutuyoruz)
sozluk = load_data()

CSS_STYLE = '''
<style>
    body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; padding: 20px; }
    h1 { color: #333; font-size: 2.5em; }
    h2 { color: #555; font-size: 1.8em; }
    ul { list-style-type: none; padding: 0; }
    li { background: #fff; margin: 10px; padding: 15px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
    a { text-decoration: none; color: #007BFF; font-weight: bold; }
    a:hover { text-decoration: underline; color: #0056b3; }
    form { margin-top: 20px; }
    input, button { padding: 10px; margin: 5px; border-radius: 5px; border: 1px solid #ccc; }
    input { width: 300px; }
    button { background-color: #007BFF; color: white; cursor: pointer; }
    button:hover { background-color: #0056b3; }
    .header { background-color: #f8f9fa; padding: 10px; border-bottom: 1px solid #ccc; }
</style>
'''

@app.route('/')
def index():
    basliklar = "".join(f'<li><a href="/baslik/{baslik}">{baslik}</a></li>' for baslik in sozluk.keys())
    return f'{CSS_STYLE}<div class="header"><h1>Ulusöz Sözlük</h1></div><form action="/yeni_baslik" method="POST"><input type="text" name="baslik" placeholder="Yeni başlık ekleyin" required><button type="submit">Ekle</button></form><h2>Başlıklar</h2><ul>{basliklar}</ul>'

@app.route('/baslik/<string:baslik>')
def baslik_sayfasi(baslik):
    entryler = "".join(f'<li>{entry}</li>' for entry in sozluk.get(baslik, []))
    return f'{CSS_STYLE}<div class="header"><h1>Ulusöz Sözlük - {baslik}</h1></div><ul>{entryler}</ul><form action="/yeni_entry/{baslik}" method="POST"><input type="text" name="entry" placeholder="Yeni entry ekleyin" required><button type="submit">Ekle</button></form><br><a href="/">Ana Sayfa</a>'

@app.route('/yeni_baslik', methods=['POST'])
def yeni_baslik():
    baslik = request.form.get('baslik')
    if baslik and baslik not in sozluk:
        sozluk[baslik] = []
        save_data(sozluk)  # Verileri JSON dosyasına kaydet
    return redirect(url_for('index'))

@app.route('/yeni_entry/<string:baslik>', methods=['POST'])
def yeni_entry(baslik):
    entry = request.form.get('entry')
    if baslik in sozluk and entry:
        sozluk[baslik].append(entry)
        save_data(sozluk)  # Verileri JSON dosyasına kaydet
    return redirect(url_for('baslik_sayfasi', baslik=baslik))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
