# Karolina EHR - Electronic Health Record System

This is a collaboration between students at Karolinska Institutet in Stockholm to create an EHR with basic functionality using the tools we've been equipped with while studying at the Joint Masters Program in Health Informatics.

## Overview

Karolina EHR is a terminal-based Electronic Health Record application designed for hospitals and healthcare facilities. The system is built with compliance, security, and international standards at its core.

**🚀 New to Karolina EHR? Check out the [Quick Start Guide](QUICKSTART.md) to get started in 5 minutes!**

## Features

### Core Functionality
- **User Management**: Support for nurses, doctors, patients, and administrative staff
- **SOAP Notes**: Clinical documentation using SOAP format (Subjective, Objective, Assessment, Plan)
- **Work Schedule**: Workpass schedule management for hospital staff
- **Patient Management**: Comprehensive patient data management

### Medical Standards Integration
- **ICD-11**: International Classification of Diseases (11th Revision) for diagnosis coding
- **ATC Codes**: Anatomical Therapeutic Chemical classification for medications
- **DRG**: Diagnosis Related Groups for hospital billing and resource allocation
- **SNOMED-CT**: Clinical terminology for healthcare documentation

### Compliance & Security
- **GDPR Compliant**: 
  - Data minimization
  - Consent management
  - Right to be forgotten
  - Comprehensive audit logging
  - Data anonymization

- **NIS2 Compliant**:
  - Security event logging
  - Role-based access control
  - Data encryption
  - Incident monitoring

### Localization
Multi-language support for international use:
- 🇬🇧 English
- 🇸🇪 Swedish (Svenska)
- 🇩🇪 German (Deutsch)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ChristianSchinkel/Karolina_EHR.git
cd Karolina_EHR
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Usage

Run the application:
```bash
karolina-ehr
```

Or run directly with Python:
```bash
python -m karolina_ehr.main
```

## Development

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=karolina_ehr --cov-report=html
```

### Project Structure

```
Karolina_EHR/
├── src/
│   └── karolina_ehr/     # Main package directory
│       ├── __init__.py   # Package initialization
│       └── main.py       # Application entry point
├── tests/                # Test directory
│   ├── __init__.py
│   └── test_basic.py     # Basic tests
├── pyproject.toml        # Project configuration and metadata
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── README.md            # This file
├── LICENSE              # License file
└── .gitignore          # Git ignore rules
```

## Contributing

This is a student project at Karolinska Institutet. Contributions are welcome from team members.

## License

See LICENSE file for details.
