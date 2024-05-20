import os
from trivia import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8888))
    app.run(debug=True, port=port)
