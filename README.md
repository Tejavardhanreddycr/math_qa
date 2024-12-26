# Math_QA

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0%2B-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/🦜_LangChain-Latest-2F6FD2.svg?style=flat)](https://www.langchain.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)

<div align="center">
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI" width="300"/>
  <br/>
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit" width="300"/>
</div>


## Table of  Contents

- [Overview](#Overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)


## Overview

Mathematical Question answering is a dual-interface application that provides you a streamlit web based app and api as a service with problem solving capability.It leverages the Groq API and Langchain framework to provide the reasoning capabilities.

The project consists of two main components:
1. A Fast api-based REST Apis (`app.py`)
2. A streamit-based web app (`st_app.py`)


## Features

- 🧮 Math Solver
  - Math Problem Solver
  - Logic and Reasoning

- 🔧 Technical Features
  - RESTful API with FastAPI
  - Interactive web UI with Streamlit

- 🔒 Security Features
  - API key authentication
  - Input validation
  - CORS support
  - SSL/TLS support


## Project Structure

```
math_qa/
├── app.py                   # Fast API application
├── st_app.py                # Streamlit Web-application
├── requirements.txt         # Project Dependencies
├── .env                     # environment file
├── .gitignore               # Git ignore file   
└── Readme.md                # Readme file
```


## Requirements

- Python 3.8 +
- Groq API key ([Get here](https://groq.com))
- Required packages in requirements.txt


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/math_qa.git
   cd math_qa
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your credentials:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```


## Configurationn

The application can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| GROQ_API_KEY | Groq API Key | Required |


## Usage

## Fast API Application
1. Start the API server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

2. Access endpoints:
   - API documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health
   - Summarization endpoint: http://localhost:8000/math_qa

### Streamlit Application

1. Start the web interface:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Open in browser:
   - http://localhost:8501


## API Documentation

### Endpoints

#### POST /summarize
Generates content summary.

Request:
```json
{
  "groq_api_key": "string",
  "question": "string"
}
```

Response:
```json
{
  "answer": "string"
}
```


## Deployment

### Docker Deployment

1. Build image:
   ```bash
   docker build -t math_qa .
   ```

2. Run container:
   ```bash
   docker run -p 8000:8000 mqth_qa
   ```

### Cloud Deployment

Deployment guides available for:
- AWS 
- Google Cloud 
- Azure
- IBM cloud

See official deployment documentation for details.


## Contributing

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>Made with FastAPI, Streamlit, and LangChain</p>
  <p>© 2024 CR Teja Vardhan Reddy. All rights reserved.</p>
</div>
