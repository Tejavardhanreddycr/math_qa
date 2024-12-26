# Math_QA

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/🦜_LangChain-Latest-2F6FD2.svg?style=flat)](https://www.langchain.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" alt="FlaskAPI" width="300"/>
  <br/>
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit" width="300"/>
</div>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

Math_QA is a dual-interface application that provides both a web-based UI and API service for solving mathematical and logical problems. It leverages the Groq API and LangChain framework to provide advanced reasoning capabilities.

The project consists of two main components:
1. A Flask-based REST API (`app.py`) with rate limiting and robust error handling
2. A Streamlit-based web application (`st_app.py`) with an interactive user interface

## Features

### Core Features
- 🧮 **Math Problem Solving**
  - Solves complex mathematical equations
  - Provides step-by-step explanations
  - Handles word problems
  
- 🤔 **Logic and Reasoning**
  - Analyzes logical problems
  - Provides detailed explanations
  - Uses Wikipedia for additional context

### Technical Features
- 🔒 **Security**
  - API key authentication
  - Rate limiting (10 requests/minute)
  - Input validation
  
- 🛠️ **Robustness**
  - Comprehensive error handling
  - Request validation
  - Detailed error messages

## Project Structure
```
math_qa/
├── app.py              # Flask API implementation
├── st_app.py          # Streamlit web interface
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Requirements
- Python 3.8+
- Groq API key
- Dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/math_qa.git
cd math_qa
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Get a Groq API key from [Groq's website](https://www.groq.com)

2. For the Flask API:
   - Set your Groq API key in the request header or query parameter

3. For the Streamlit app:
   - Enter your Groq API key in the sidebar

## Usage

### Running the Flask API
```bash
python app.py
```
The API will be available at `http://localhost:5000`

### Running the Streamlit App
```bash
streamlit run st_app.py
```
The web interface will be available at `http://localhost:8501`

## API Documentation

### POST /solve_question
Solves a mathematical or logical question.

**Request**
```json
{
  "question": "What is the sum of 123 and 456?"
}
```

**Parameters**
- `groq_api_key` (query parameter): Your Groq API key

**Response**
```json
{
  "answer": "The sum of 123 and 456 is 579..."
}
```

### GET /health
Health check endpoint.

**Response**
```json
{
  "status": "healthy",
  "message": "Welcome to the Text to Math Problem Solver API"
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
