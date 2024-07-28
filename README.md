# Rule Engine

## Overview

This project is a rule engine that allows for creating, combining, and evaluating rules using Abstract Syntax Trees (AST). It supports evaluating conditions based on user data and can combine multiple rules into a single AST for more complex evaluations.

## Features

- Create rules from strings and convert them into AST.
- Combine multiple rules into a single AST.
- Evaluate ASTs against user data.
- Convert ASTs to and from JSON format.
- Customizable rule evaluation with support for common comparison operators.

## Prerequisites

Before setting up the environment, ensure you have the following installed:

- Python 3.12
- pip (Python package installer)

## Setup

```bash
# Clone the Repository
git clone https://github.com/your-username/rule-engine.git
cd rule-engine

# Create a Virtual Environment
python -m venv venv

# Activate the Virtual Environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Run the Development Server
python manage.py runserver

# Run Tests
python manage.py test
