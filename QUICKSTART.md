# Quick Start Guide - Karolina EHR

Get started with the Karolina Electronic Health Record system in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/ChristianSchinkel/Karolina_EHR.git
cd Karolina_EHR

# Install dependencies
pip install -r requirements.txt
```

## Quick Demo

See all features in action without any interaction:

```bash
python demo.py
```

This will display:
- User management examples
- SOAP clinical documentation
- Medical coding validation (ICD-11, ATC, DRG, SNOMED-CT)
- Work schedules
- Security features
- Multi-language support

## Run Tests

Verify everything is working:

```bash
python test_system.py
```

Expected output: **10 passed, 0 failed**

## Interactive Application

Launch the full terminal application:

```bash
python main.py
```

### First Time Setup

1. **Choose Language**: 
   - 1 = English
   - 2 = Swedish
   - 3 = German

2. **Login** with demo account:
   - **Nurse**: `nurse1`
   - **Doctor**: `dr_smith`
   - **Patient**: `patient1`

### Quick Walkthrough

After logging in as `dr_smith` (doctor):

#### 1. View Patients
```
Main Menu → 1 (Patient Management) → 1 (Patient List)
```

#### 2. Create SOAP Note
```
Main Menu → 2 (SOAP Notes) → 1 (Create SOAP Note)
```

Example values:
- Patient: Select from list
- Subjective: "Patient reports fever and cough"
- Objective: "Temperature 38.5°C, HR 90"
- Assessment: "Upper respiratory infection"
- Plan: "Rest, fluids, paracetamol"
- ICD-11: `386661006` (Fever)
- ATC: `N02BE01` (Paracetamol)

#### 3. View Work Schedule
```
Main Menu → 3 (Work Schedule) → 1 (View Schedule)
```

#### 4. Change Language
```
Main Menu → 4 (Settings) → 1 (Change Language)
```

## Key Features

### Medical Coding

The system validates medical codes:

| Standard | Example Code | Description |
|----------|-------------|-------------|
| ICD-11 | `BA00` | Essential hypertension |
| ATC | `N02BE01` | Paracetamol |
| DRG | `291` | Heart Failure & Shock |
| SNOMED-CT | `386661006` | Fever |

### Compliance

**GDPR**: All data access is logged in `karolina_ehr/data/audit.log`

**NIS2**: Role-based access control with security logging in `karolina_ehr/data/security.log`

### Languages

Switch between:
- 🇬🇧 English
- 🇸🇪 Swedish
- 🇩🇪 German

All interface text is translated.

## Common Tasks

### Add a New Patient

1. Login as nurse or doctor
2. Main Menu → 1 → 2
3. Enter patient details
4. Confirm consent

### Create Clinical Note

1. Login as nurse or doctor
2. Main Menu → 2 → 1
3. Select patient
4. Fill in SOAP sections
5. Add medical codes (optional)

### View Audit Logs

```bash
cat karolina_ehr/data/audit.log
```

Each entry shows:
- Timestamp
- User ID
- Action performed
- Resource accessed

## Project Structure

```
Karolina_EHR/
├── main.py              # Start here
├── demo.py              # Feature demo
├── test_system.py       # Test suite
├── karolina_ehr/
│   ├── models/          # User, Patient, SOAP, Schedule
│   ├── services/        # Medical codes, Security, i18n
│   ├── ui/              # Terminal interface
│   └── locales/         # Translations (en, sv, de)
└── README.md            # Full documentation
```

## Troubleshooting

**Q: Import errors?**
```bash
pip install -r requirements.txt
```

**Q: Permission denied?**
- Check user role (patients have limited access)
- Verify in NIS2 access control matrix

**Q: Language not changing?**
- Changes apply immediately
- Check locale files exist in `karolina_ehr/locales/`

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- See [USAGE_GUIDE.md](USAGE_GUIDE.md) for complete feature guide
- Run `python demo.py` to see all features

## Support

For issues or questions, please open an issue on GitHub.

---

**Ready to start?** Run: `python main.py`
