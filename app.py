from api.user import app
from config.setting import SERVER_PORT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
