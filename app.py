import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# ===============================
# CORS origin’lerini env’den oku
# Environment Variable olarak:
#   CORS_ORIGINS="https://halil.com.tr,https://www.halil.com.tr"
# atayacaksınız
# ===============================
allowed_origins = os.environ.get("CORS_ORIGINS", "")
allowed_list = [o.strip() for o in allowed_origins.split(",") if o.strip()]
CORS(app, origins=allowed_list)


def check_url(url):
    try:
        response = requests.get(url, allow_redirects=False, timeout=10)
        status = response.status_code

        # 301 sabit redirect
        if status == 301:
            return {
                "url": url,
                "redirect_to": response.headers.get("Location", url),
                "status": 301,
                "note": "Çözüm İçin Danış"
            }
        # Diğer 3xx’ler
        elif 300 <= status < 400:
            return {
                "url": url,
                "redirect_to": response.headers.get("Location", url),
                "status": status,
                "note": "Yönlendirme"
            }
        # 200 OK ya da diğer kodlar
        else:
            return {
                "url": url,
                "redirect_to": url,
                "status": status,
                "note": "" if status == 200 else "Çözüm İçin Danış"
            }
    except Exception:
        return {
            "url": url,
            "redirect_to": url,
            "status": "Erişilemedi",
            "note": "Çözüm İçin Danış"
        }


@app.route("/", methods=["GET"])
def health_check():
    return "HTTP Status Checker Proxy is up and running!"


@app.route("/api/check-urls", methods=["POST"])
def check_urls():
    data = request.get_json(force=True)
    urls = data.get("urls", [])
    # En fazla 100 URL ile sınırla
    results = [check_url(u) for u in urls[:100]]
    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # production ortamı için debug=False
    debug_mode = os.environ.get("FLASK_ENV", "") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
