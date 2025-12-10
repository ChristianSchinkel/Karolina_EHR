# Karolina EHR - Usage Guide

## Getting Started

This guide will help you understand and use the Karolina Electronic Health Record system.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Select your language** (English, Swedish, or German)

4. **Login** with a demo account

## Demo Accounts

The system comes with three pre-configured demo accounts:

| Username | Role | Description |
|----------|------|-------------|
| `nurse1` | Nurse | Can manage patients, create SOAP notes, view schedules |
| `dr_smith` | Doctor | Full access to patient records and SOAP notes |
| `patient1` | Patient | Can view own medical records (limited access) |

## Features Walkthrough

### 1. Patient Management

**Access**: Nurses, Doctors, Admins

#### Viewing Patients
1. From main menu, select `1` (Patient Management)
2. Select `1` (Patient List)
3. View all registered patients with consent status

#### Adding a Patient
1. From main menu, select `1` (Patient Management)
2. Select `2` (Add New Patient)
3. Enter patient details:
   - Username
   - Personal ID (e.g., "19900101-1234")
   - Consent confirmation (y/n)
4. Patient is created with GDPR audit log entry

**GDPR Note**: Patient consent is tracked. All access is logged for compliance.

### 2. SOAP Notes

**Access**: Nurses, Doctors

SOAP notes follow the standard clinical documentation format:
- **S**ubjective: Patient's description of symptoms
- **O**bjective: Observable data (vitals, tests, examination)
- **A**ssessment: Clinical diagnosis/impression
- **P**lan: Treatment plan and follow-up

#### Creating a SOAP Note
1. From main menu, select `2` (SOAP Notes)
2. Select `1` (Create SOAP Note)
3. Choose a patient from the list
4. Enter SOAP components:
   - Subjective: "Patient complains of headache for 2 days"
   - Objective: "Blood pressure 140/90, temperature 37.2°C"
   - Assessment: "Tension headache"
   - Plan: "Prescribe paracetamol, follow-up in 1 week"
5. Optionally add medical codes:
   - ICD-11: `25064002` (Headache)
   - ATC: `N02BE01` (Paracetamol)
   - DRG: Leave blank or add appropriate code
   - SNOMED-CT: `25064002` (Headache)

#### Viewing SOAP Notes
1. From main menu, select `2` (SOAP Notes)
2. Select `2` (View SOAP Notes)
3. Browse all clinical notes with patient info and dates

**Medical Coding**: The system validates codes and shows descriptions when available.

### 3. Work Schedule

**Access**: All staff members

#### Viewing Schedule
1. From main menu, select `3` (Work Schedule)
2. Select `1` (View Schedule)
3. See all scheduled shifts with staff, dates, and departments

#### Adding a Shift
1. From main menu, select `3` (Work Schedule)
2. Select `2` (Add Shift)
3. Enter shift details:
   - Department: "Emergency", "ICU", "Surgery", etc.
   - Shift type: "day", "night", or "evening"
4. Shift is created for current user

**Note**: In a production system, administrators could assign shifts to any staff member.

### 4. Settings

#### Changing Language
1. From main menu, select `4` (Settings)
2. Select `1` (Change Language)
3. Choose from English, Swedish, or German
4. All interface text updates immediately

## Medical Coding Standards

### ICD-11 (Diagnosis Codes)

Sample codes available in the system:

| Code | Description |
|------|-------------|
| 1A00 | Cholera |
| 1B10 | Intestinal infections due to E. coli |
| 1C62.0 | COVID-19 |
| 8A62 | Diabetes mellitus, type 2 |
| BA00 | Essential hypertension |
| 9B71.0Z | Depression |

Format: Alphanumeric, typically 4+ characters

### ATC Codes (Medications)

Sample codes available in the system:

| Code | Description |
|------|-------------|
| A02BC01 | Omeprazole - Proton pump inhibitor |
| C09AA01 | Captopril - ACE inhibitor |
| N02BE01 | Paracetamol - Analgesic/Antipyretic |
| J01CA04 | Amoxicillin - Penicillin antibiotic |
| A10BA02 | Metformin - Antidiabetic drug |
| C07AB02 | Metoprolol - Beta blocker |

Format: Letter-Number-Letter-Letter-Number-Number (7 characters)

### DRG Codes (Diagnosis Related Groups)

Sample codes available in the system:

| Code | Description |
|------|-------------|
| 001 | Heart Transplant or Implant of Heart Assist System |
| 190 | Chronic Obstructive Pulmonary Disease |
| 291 | Heart Failure & Shock |
| 470 | Major Joint Replacement or Reattachment of Lower Extremity |
| 683 | Renal Failure |

Format: 3-digit numeric code

### SNOMED-CT (Clinical Terms)

Sample codes available in the system:

| Code | Description |
|------|-------------|
| 386661006 | Fever |
| 25064002 | Headache |
| 49727002 | Cough |
| 271807003 | Rash |
| 13791008 | Asthma |
| 38341003 | Hypertensive disorder |

Format: 6+ digit numeric code

## Security & Compliance

### GDPR Features

1. **Audit Logging**
   - All data access is logged to `karolina_ehr/data/audit.log`
   - Logs include: timestamp, user, action, resource type, resource ID
   - Example: `{"timestamp": "2025-12-10T12:00:00", "user_id": "...", "action": "read", ...}`

2. **Consent Management**
   - Patient consent is tracked and required
   - Consent date is recorded
   - Access can be restricted based on consent status

3. **Data Minimization**
   - Only necessary fields are collected
   - Personal data is encrypted when stored

4. **Right to be Forgotten**
   - System supports patient data deletion
   - All deletions are logged

### NIS2 Features

1. **Role-Based Access Control**
   - Nurses: Read/Write patients and SOAP notes
   - Doctors: Full access to medical records
   - Patients: Read-only access to own data
   - Admins: Full system access

2. **Security Event Logging**
   - Failed access attempts are logged to `karolina_ehr/data/security.log`
   - Security events include severity levels
   - Unauthorized access attempts are tracked

3. **Access Validation**
   - Every action is validated against user permissions
   - Denied access is logged and reported

## Multilingual Support

### Available Languages

1. **English (en)**
   - Default language
   - Full interface support

2. **Swedish (sv)**
   - Svensk översättning
   - Komplett gränssnittsstöd

3. **German (de)**
   - Deutsche Übersetzung
   - Vollständige Schnittstellenunterstützung

### Translation Files

Located in `karolina_ehr/locales/`:
- `en/messages.json` - English
- `sv/messages.json` - Swedish
- `de/messages.json` - German

## Data Storage

### Current Implementation

The demo uses in-memory storage for simplicity. Data is not persisted between sessions.

### Production Implementation

For production use, you would need to:

1. **Database Integration**
   - PostgreSQL, MySQL, or similar RDBMS
   - Encrypted storage for sensitive fields
   - Regular backups

2. **Authentication**
   - Password hashing (bcrypt, argon2)
   - Two-factor authentication
   - Session management

3. **External API Integration**
   - Real ICD-11 API
   - Real ATC database
   - Real SNOMED-CT terminology server

4. **Audit & Compliance**
   - Log rotation and archival
   - Compliance reporting tools
   - Data retention policies

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure you're running from the repository root
   - Check that all dependencies are installed: `pip install -r requirements.txt`

2. **Permission Denied**
   - Log in with appropriate role for the action
   - Nurses cannot delete records
   - Patients have read-only access

3. **Language Not Changing**
   - Language changes apply immediately
   - Check that the locale file exists

4. **Logs Not Created**
   - Logs are created in `karolina_ehr/data/` directory
   - Directory is created automatically on first access

## Best Practices

1. **Patient Privacy**
   - Always obtain consent before accessing patient data
   - Log out when finished with a session
   - Do not share login credentials

2. **Clinical Documentation**
   - Complete all SOAP sections thoroughly
   - Add appropriate medical codes
   - Review entries before saving

3. **Work Scheduling**
   - Keep schedules up to date
   - Coordinate with department leads
   - Note any schedule conflicts

4. **Data Entry**
   - Use standard medical terminology
   - Double-check patient identification
   - Verify medical codes before submission

## Extension Ideas

For educational purposes, consider extending the system with:

1. **Additional Features**
   - Laboratory results integration
   - Prescription management
   - Appointment scheduling
   - Medical imaging references

2. **Enhanced Security**
   - Two-factor authentication
   - Session timeout
   - IP restriction
   - Audit report generation

3. **Improved Workflows**
   - Patient admission/discharge
   - Ward transfers
   - Emergency alerts
   - Staff communication

4. **Analytics & Reporting**
   - Patient statistics
   - Department workload
   - Medication usage reports
   - Compliance dashboards

## Support & Contribution

This is an educational project. For questions or improvements:

1. Open an issue on GitHub
2. Submit a pull request
3. Contact the development team

## Legal Notice

This software is for educational purposes only. It is NOT certified for production use in healthcare settings. Real-world implementation requires:

- Medical device certification
- HIPAA/GDPR compliance audit
- Security penetration testing
- Professional validation
- Legal review

---

**Last Updated**: December 2025  
**Version**: 0.1.0
