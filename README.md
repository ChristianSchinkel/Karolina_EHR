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

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### First-Time Setup

1. **Language Selection**: Choose your preferred language (English, Swedish, or German)
2. **Login**: Use one of the demo accounts:
   - Username: `nurse1` (Nurse role)
   - Username: `dr_smith` (Doctor role)
   - Username: `patient1` (Patient role)

### Main Menu Options

1. **Patient Management**
   - View patient list
   - Add new patients
   - Manage patient consent

2. **SOAP Notes**
   - Create clinical documentation
   - View existing notes
   - Add medical codes (ICD-11, ATC, DRG, SNOMED-CT)

3. **Work Schedule**
   - View staff schedules
   - Add shift assignments
   - Manage department assignments

4. **Settings**
   - Change language
   - Configure preferences

## Project Structure

```
Karolina_EHR/
├── karolina_ehr/
│   ├── __init__.py
│   ├── models/
│   │   └── __init__.py          # User, Patient, Nurse, Doctor, SOAPNote, WorkSchedule
│   ├── services/
│   │   ├── __init__.py
│   │   ├── terminology.py       # ICD-11, ATC, DRG, SNOMED-CT services
│   │   ├── security.py          # GDPR and NIS2 compliance
│   │   └── localization.py      # Multi-language support
│   ├── ui/
│   │   ├── __init__.py
│   │   └── terminal.py          # Terminal user interface
│   ├── locales/
│   │   ├── en/messages.json     # English translations
│   │   ├── sv/messages.json     # Swedish translations
│   │   └── de/messages.json     # German translations
│   └── data/                    # Audit logs and data storage
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── LICENSE                      # MIT License
```

## Medical Coding Examples

### ICD-11 Codes
- `1A00`: Cholera
- `1C62.0`: COVID-19
- `8A62`: Diabetes mellitus, type 2
- `BA00`: Essential hypertension

### ATC Codes
- `A02BC01`: Omeprazole (Proton pump inhibitor)
- `N02BE01`: Paracetamol (Analgesic/Antipyretic)
- `J01CA04`: Amoxicillin (Penicillin antibiotic)
- `A10BA02`: Metformin (Antidiabetic drug)

### SNOMED-CT Codes
- `386661006`: Fever
- `25064002`: Headache
- `49727002`: Cough
- `13791008`: Asthma

## Security Features

### GDPR Compliance
- **Audit Logging**: All data access is logged with timestamps and user information
- **Data Encryption**: Sensitive personal data is encrypted
- **Consent Management**: Patient consent tracking and validation
- **Data Anonymization**: Personal data can be anonymized for analytics

### NIS2 Compliance
- **Role-Based Access Control**: Granular permissions based on user roles
- **Security Event Logging**: All security events are logged and monitored
- **Access Validation**: Every action is validated against user permissions
- **Incident Response**: Security incidents are logged with severity levels

## Data Privacy

This system implements privacy-by-design principles:
- Minimal data collection
- Purpose limitation
- Storage limitation
- Integrity and confidentiality
- Accountability

All audit logs are stored in `karolina_ehr/data/audit.log` and security logs in `karolina_ehr/data/security.log`.

## Development

### Adding New Features

The system is designed to be extensible:

1. **New User Roles**: Extend the `User` base class in `models/__init__.py`
2. **New Medical Codes**: Add to the respective service in `services/terminology.py`
3. **New Translations**: Update all three language files in `locales/`
4. **New Features**: Follow the existing architectural patterns

### Testing

The system includes sample data for demonstration purposes. In a production environment, you would:
- Implement proper authentication (passwords, 2FA)
- Connect to a real database instead of in-memory storage
- Integrate with actual medical terminology APIs
- Implement data backup and recovery
- Add comprehensive unit and integration tests

## Contributing

This is an educational project. Contributions should maintain:
- GDPR and NIS2 compliance
- Medical coding standards (ICD-11, ATC, DRG, SNOMED-CT)
- Multi-language support
- Code quality and documentation

## License

MIT License - see LICENSE file for details.

## Disclaimer

This is an educational project developed by students at Karolinska Institutet. It is NOT intended for production use in real healthcare settings without proper certification, validation, and compliance verification.

## Acknowledgments

- Karolinska Institutet Joint Masters Program in Health Informatics
- WHO for ICD-11 and ATC standards
- SNOMED International for SNOMED-CT
- European Union for GDPR and NIS2 frameworks

## Support

For questions or issues, please open an issue on GitHub.

---

**Version**: 0.1.0  
**Last Updated**: December 2025
