# Rule Engine Application 🌟
<hr/>

## Overview
This is a simple 3-tier rule engine application that determines user eligibility based on attributes like age, department, income, and experience. The system uses an **Abstract Syntax Tree (AST)** to represent conditional rules and allows for dynamic creation, combination, and modification of these rules.

## Features 🚀
- **Create Rule**: Allows users to create complex rules based on specified attributes.
- **Combine Rules**: Combines multiple rules into a single AST for evaluation.
- **Evaluate Rule**: Evaluates the given data against the rules and returns whether the user is eligible.
- **Error Handling (Bonus)**: Provides meaningful error messages for invalid rule strings and data formats.

## Project Structure 📁

```graphql
app/
├── api.py             # Provides API functions to interact with the rule engine
├── ast.py             # Defines the AST data structure
├── database.py        # Handles database initialization and operations
├── rules.py           # Implements rule creation, combination, and evaluation logic
├── static/            # Contains static files (CSS, JavaScript)
│   ├── css/
│   │   └── style.css  # CSS styles for the UI
│   └── js/
│       └── script.js  # JavaScript for dynamic interactions
└── templates/         # HTML templates for the UI
    └── index.html     # Main UI template

tests/
├── test_rules.py      # Unit tests for rule creation, combination, and evaluation
└── test_api.py        # Unit tests for the API functions

requirements.txt        # Lists the dependencies
main.py                 # The entry point of the application
README.md               # Documentation file
```


## Design Choices 💡
- **3-tier Architecture**: Separates the UI, API, and backend logic for better maintainability and scalability.
- **Abstract Syntax Tree (AST)**: Allows dynamic creation, combination, and modification of rules.
- **Error Handling**: Comprehensive error handling ensures robustness by addressing invalid input formats.
- **UI Design**: A clean and user-friendly interface provides dynamic feedback for rule evaluation results.

<hr/>

## Instructions 📚

### Prerequisites 🛠️
- Python 3.6 or higher
- Flask
- SQLite (for database)

### Build and Install
1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
2. **Initialize the virtual environment**:
   ```bash
   venv/Scripts/activate  # For Windows
    # OR
   source venv/bin/activate  # For macOS/Linux
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Initalize the database:**
   ```bash
   python -c "from app.database import initialize_database; initialize_database()"
   ```
5. **Run the application:**
   ```
   python main.py
   ```
   Open your web browser and go to http://127.0.0.1:5000/.
<hr/>

## Testing the Application 🧪
### Sample Tests to Try on UI

Creating a Rule:
- Input the following rule in the "Create Rule" text box and press the "Create Rule" button:
  ```bash
  ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
  ```
  - ✔️ If successful, it will display a message indicating that the rule was created, along with the generated AST.

Input a Query to Evaluate:
- Input the following JSON in the "Data (JSON format)" text area:
  ```bash
  {
    "age": 50,
    "department": "Sales",
    "salary": 60000,
    "experience": 10
  }
  ```
    - ✔️ If successful, it will display a message indicating that the rule was created, along with the generated AST.

## Predefined Test Cases 🔍
Run the unit tests to validate functionality:
   ```bash
   python -W ignore::DeprecationWarning -m unittest discover
   ```

<hr/>
