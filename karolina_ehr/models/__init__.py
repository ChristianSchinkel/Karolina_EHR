"""
Core models for Karolina EHR System.
Implements base classes for users and clinical data.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid


class UserRole(Enum):
    """User roles in the EHR system."""
    NURSE = "nurse"
    DOCTOR = "doctor"
    ADMIN = "admin"
    PATIENT = "patient"


@dataclass
class User:
    """Base class for all users in the system.
    
    GDPR Compliance: Personal data is minimized and encrypted when stored.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    role: UserRole = UserRole.PATIENT
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Ensure role is UserRole enum."""
        if isinstance(self.role, str):
            self.role = UserRole(self.role)


@dataclass
class Nurse(User):
    """Nurse user with specific permissions."""
    license_number: str = ""
    department: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.role = UserRole.NURSE


@dataclass
class Doctor(User):
    """Doctor user with specific permissions."""
    license_number: str = ""
    specialization: str = ""
    
    def __post_init__(self):
        super().__post_init__()
        self.role = UserRole.DOCTOR


@dataclass
class Patient(User):
    """Patient user.
    
    GDPR Compliance: Patient data includes consent tracking.
    """
    personal_id: str = ""  # Personal identification number (encrypted)
    date_of_birth: Optional[datetime] = None
    consent_given: bool = False
    consent_date: Optional[datetime] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.role = UserRole.PATIENT


@dataclass
class SOAPNote:
    """SOAP format for clinical documentation.
    
    S - Subjective: Patient's description of the problem
    O - Objective: Observable and measurable data
    A - Assessment: Diagnosis or clinical impression
    P - Plan: Treatment plan and follow-up
    
    Integrates with ICD-11, ATC, DRG, and SNOMED-CT codes.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    author_id: str = ""  # Nurse or Doctor who created the note
    created_at: datetime = field(default_factory=datetime.now)
    
    # SOAP components
    subjective: str = ""  # Patient's complaints and symptoms
    objective: str = ""  # Vital signs, lab results, physical exam
    assessment: str = ""  # Clinical diagnosis
    plan: str = ""  # Treatment plan
    
    # Medical coding
    icd11_codes: List[str] = field(default_factory=list)  # ICD-11 diagnosis codes
    atc_codes: List[str] = field(default_factory=list)  # ATC medication codes
    drg_code: Optional[str] = None  # Diagnosis Related Group code
    snomed_codes: List[str] = field(default_factory=list)  # SNOMED-CT clinical terms
    
    # Audit trail for GDPR/NIS2 compliance
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None


@dataclass
class WorkSchedule:
    """Work schedule for hospital staff.
    
    Implements workpass schedule functionality.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    staff_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = field(default_factory=datetime.now)
    department: str = ""
    shift_type: str = "day"  # day, night, evening
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
