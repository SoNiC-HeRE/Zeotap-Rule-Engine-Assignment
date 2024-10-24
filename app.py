# app.py
from app import create_app

# Create an instance of the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application in debug mode if this script is executed directly
    app.run(debug=True)