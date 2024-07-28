# Rule Engine

## Overview

This project is a rule engine that allows for creating, combining, and evaluating rules using Abstract Syntax Trees (AST). It supports evaluating conditions based on user data and can combine multiple rules into a single AST for more complex evaluations.

## Features

- Create rules from strings and convert them into AST.
- Combine multiple rules into a single AST.
- Evaluate ASTs against user data.
- Convert ASTs to and from JSON format.
- Customizable rule evaluation with support for common comparison operators.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Example Usage](#example-usage)
- [Contributing](#contributing)

# Prerequisites

Before setting up the environment, ensure you have the following installed:

- Python 3.8 or later
- pip (Python package installer)

# Setup

```bash
# Clone the Repository
https://github.com/hiteshkumar8642/RuleEngine.git
cd rule-engine

# Create a Virtual Environment
python -m venv venv

# Activate the Virtual Environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```
# Installation
pip install -r requirements.txt

# Running the Application
python manage.py runserver

# Running Tests
python manage.py test

# Example Usage

# Create a Rule
```bash
from ast import create_rule
rule_string = 'age > 30 AND department = \"Sales\"'
ast = create_rule(rule_string)
import json
print(json.dumps(ast.to_dict(), indent=2))
```

# Combine Rules
```bash
from ast import combine_rules
rules = [
    'age > 30 AND department = \"Sales\"',
    'salary > 50000 OR experience > 5'
]
combined_ast = combine_rules(rules)
import json
print(json.dumps(combined_ast, indent=2))
```

# Evaluate Rules
```bash
from ast import evaluate_ast
user_data = {
    'age': 32,
    'department': 'Sales',
    'salary': 60000,
    'experience': 6
}
ast = {'type': 'operator', 'value': 'AND', 'left': {'type': 'operand', 'value': 'age > 30'}, 'right': {'type': 'operand', 'value': 'salary > 50000'}}
result = evaluate_ast(ast, user_data)
print(result)
```

## Contributing
```bash
#Fork the Repository
#Click the "Fork" button at the top right of the repository page.

#Clone Your Fork
https://github.com/hiteshkumar8642/RuleEngine.git

#Create a New Branch
git checkout -b feature/my-new-feature

#Make Changes
#Implement your changes or bug fixes.

#Commit Changes
git add .
git commit -m "Add a new feature or fix a bug"

#Push to GitHub
git push origin feature/my-new-feature

#Create a Pull Request
#Open a pull request from your branch to the main repository’s main branch.
```
