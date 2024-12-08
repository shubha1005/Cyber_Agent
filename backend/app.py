from flask import Flask
from tool1.app import tool1
from tool2.app import tool2

app = Flask(__name__)

# Register blueprints
app.register_blueprint(tool1, url_prefix='/tool1')  # Accessible at /tool1
app.register_blueprint(tool2, url_prefix='/tool2')  # Accessible at /tool2

if __name__ == "__main__":
    app.run(debug=True)
