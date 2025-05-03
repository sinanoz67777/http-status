from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, origins=["https://www.batuhandurmaz.com"])

def check_url(url):
    try:
        response = requests.get(url, allow_redirects=False, timeout=10)
        if response.status_code == 301:
            return {
                "url": url,
                "redirect_to": response.headers.get('Location', url),
                "status": 301,
                "note": "Çözüm İçin Danış"
            }
        elif response.status_code in range(300, 399):
            return {
                "url": url,
                "redirect_to": response.headers.get('Location', url),
                "status": response.status_code,
                "note": "Yönlendirme"
            }
        else:
            return {
                "url": url,
                "redirect_to": url,
                "status": response.status_code,
                "note": "" if response.status_code == 200 else "Çözüm İçin Danış"
            }
    except:
        return {
            "url": url,
            "redirect_to": url,
            "status": "Erişilemedi",
            "note": "Çözüm İçin Danış"
        }

@app.route("/api/check-urls", methods=["POST"])
def check_urls():
    data = request.json
    urls = data.get("urls", [])
    results = [check_url(url) for url in urls[:100]]
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
