#!/usr/bin/env python3
"""
Automated test suite for Karolina EHR System.

This script verifies all major components and features.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from karolina_ehr.models import Nurse, Doctor, Patient, SOAPNote, WorkSchedule, UserRole
from karolina_ehr.services import (
    ICD11Service, ATCService, DRGService, SNOMEDService,
    GDPRService, NIS2Service, LocalizationService
)


def test_user_models():
    """Test user model creation and role assignment."""
    print("Testing User Models...")
    
    nurse = Nurse(username="test_nurse", license_number="N123", department="Emergency")
    assert nurse.role == UserRole.NURSE, "Nurse role should be set correctly"
    
    doctor = Doctor(username="test_doctor", license_number="D456", specialization="Cardiology")
    assert doctor.role == UserRole.DOCTOR, "Doctor role should be set correctly"
    
    patient = Patient(username="test_patient", personal_id="123456", consent_given=True)
    assert patient.role == UserRole.PATIENT, "Patient role should be set correctly"
    assert patient.consent_given == True, "Patient consent should be tracked"
    
    print("  ✓ User models work correctly")


def test_soap_notes():
    """Test SOAP note creation with medical codes."""
    print("Testing SOAP Notes...")
    
    patient_id = "patient-123"
    doctor_id = "doctor-456"
    
    soap = SOAPNote(
        patient_id=patient_id,
        author_id=doctor_id,
        subjective="Patient reports headache",
        objective="BP 120/80, temp normal",
        assessment="Tension headache",
        plan="Rest and hydration",
        icd11_codes=["25064002"],
        atc_codes=["N02BE01"],
        drg_code="190",
        snomed_codes=["25064002"]
    )
    
    assert soap.patient_id == patient_id, "SOAP note should link to patient"
    assert soap.author_id == doctor_id, "SOAP note should link to author"
    assert len(soap.icd11_codes) > 0, "SOAP note should contain ICD-11 codes"
    
    print("  ✓ SOAP notes work correctly")


def test_work_schedule():
    """Test work schedule creation."""
    print("Testing Work Schedules...")
    
    start = datetime.now()
    end = start + timedelta(hours=8)
    
    schedule = WorkSchedule(
        staff_id="nurse-123",
        start_time=start,
        end_time=end,
        department="Emergency",
        shift_type="day"
    )
    
    assert schedule.staff_id == "nurse-123", "Schedule should link to staff"
    assert schedule.shift_type == "day", "Shift type should be set"
    assert schedule.end_time > schedule.start_time, "End time should be after start time"
    
    print("  ✓ Work schedules work correctly")


def test_icd11_service():
    """Test ICD-11 service."""
    print("Testing ICD-11 Service...")
    
    # Valid code
    assert ICD11Service.validate_code("BA00") == True, "BA00 should be valid"
    assert ICD11Service.validate_code("1C62.0") == True, "1C62.0 should be valid"
    
    # Invalid code
    assert ICD11Service.validate_code("") == False, "Empty string should be invalid"
    assert ICD11Service.validate_code("X") == False, "Too short code should be invalid"
    
    # Description lookup
    desc = ICD11Service.get_description("BA00")
    assert desc == "Essential hypertension", "Should return correct description"
    
    print("  ✓ ICD-11 service works correctly")


def test_atc_service():
    """Test ATC service."""
    print("Testing ATC Service...")
    
    # Valid codes
    assert ATCService.validate_code("A10BA02") == True, "A10BA02 should be valid"
    assert ATCService.validate_code("N02BE01") == True, "N02BE01 should be valid"
    
    # Invalid codes
    assert ATCService.validate_code("") == False, "Empty string should be invalid"
    assert ATCService.validate_code("ABC1234") == False, "Wrong pattern should be invalid"
    assert ATCService.validate_code("A10BA0") == False, "Too short should be invalid"
    assert ATCService.validate_code("1A0BA02") == False, "Starting with number should be invalid"
    
    # Description lookup
    desc = ATCService.get_description("N02BE01")
    assert "Paracetamol" in desc, "Should return correct description"
    
    print("  ✓ ATC service works correctly")


def test_drg_service():
    """Test DRG service."""
    print("Testing DRG Service...")
    
    # Valid code
    assert DRGService.validate_code("001") == True, "001 should be valid"
    assert DRGService.validate_code("190") == True, "190 should be valid"
    
    # Invalid codes
    assert DRGService.validate_code("") == False, "Empty string should be invalid"
    assert DRGService.validate_code("1") == False, "Too short should be invalid"
    assert DRGService.validate_code("ABC") == False, "Non-numeric should be invalid"
    
    # Description lookup
    desc = DRGService.get_description("190")
    assert desc == "Chronic Obstructive Pulmonary Disease", "Should return correct description"
    
    print("  ✓ DRG service works correctly")


def test_snomed_service():
    """Test SNOMED-CT service."""
    print("Testing SNOMED-CT Service...")
    
    # Valid codes
    assert SNOMEDService.validate_code("386661006") == True, "386661006 should be valid"
    assert SNOMEDService.validate_code("25064002") == True, "25064002 should be valid"
    
    # Invalid codes
    assert SNOMEDService.validate_code("") == False, "Empty string should be invalid"
    assert SNOMEDService.validate_code("123") == False, "Too short should be invalid"
    assert SNOMEDService.validate_code("ABC123") == False, "Non-numeric should be invalid"
    
    # Description lookup
    desc = SNOMEDService.get_description("386661006")
    assert desc == "Fever", "Should return correct description"
    
    print("  ✓ SNOMED-CT service works correctly")


def test_gdpr_service():
    """Test GDPR compliance service."""
    print("Testing GDPR Service...")
    
    gdpr = GDPRService(audit_log_path="/tmp/test_audit.log")
    
    # Test audit logging
    gdpr.log_access(
        user_id="user-123",
        action="read",
        resource_type="patient",
        resource_id="patient-456",
        details="Viewing patient record"
    )
    
    # Verify log was created
    assert Path("/tmp/test_audit.log").exists(), "Audit log should be created"
    
    # Test data anonymization
    data = {"personal_id": "123456", "username": "john_doe", "license_number": "ABC123"}
    anonymized = gdpr.anonymize_data(data)
    assert "***" in anonymized["personal_id"], "Personal ID should be anonymized"
    
    print("  ✓ GDPR service works correctly")


def test_nis2_service():
    """Test NIS2 security service."""
    print("Testing NIS2 Service...")
    
    nis2 = NIS2Service(security_log_path="/tmp/test_security.log")
    
    # Test access validation
    assert nis2.validate_access("doctor", "patient", "read") == True, "Doctor should read patients"
    assert nis2.validate_access("doctor", "soap_note", "write") == True, "Doctor should write SOAP notes"
    assert nis2.validate_access("patient", "soap_note", "write") == False, "Patient should not write SOAP notes"
    assert nis2.validate_access("nurse", "patient", "delete") == False, "Nurse should not delete patients"
    
    # Test security logging
    nis2.log_security_event(
        event_type="login_success",
        severity="low",
        description="User logged in successfully",
        user_id="user-123"
    )
    
    # Verify log was created
    assert Path("/tmp/test_security.log").exists(), "Security log should be created"
    
    print("  ✓ NIS2 service works correctly")


def test_localization_service():
    """Test localization service."""
    print("Testing Localization Service...")
    
    # Test English
    locale_en = LocalizationService("en")
    assert "Welcome" in locale_en.get("welcome"), "Should return English text"
    
    # Test Swedish
    locale_sv = LocalizationService("sv")
    assert "Välkommen" in locale_sv.get("welcome"), "Should return Swedish text"
    
    # Test German
    locale_de = LocalizationService("de")
    assert "Willkommen" in locale_de.get("welcome"), "Should return German text"
    
    # Test changing locale
    locale = LocalizationService("en")
    locale.set_locale("sv")
    assert "Välkommen" in locale.get("welcome"), "Locale should change"
    
    # Test format strings
    locale_en = LocalizationService("en")
    # Test missing key returns key itself
    assert locale_en.get("nonexistent_key") == "nonexistent_key", "Missing key should return key"
    
    print("  ✓ Localization service works correctly")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Karolina EHR System - Automated Test Suite")
    print("="*60 + "\n")
    
    tests = [
        test_user_models,
        test_soap_notes,
        test_work_schedule,
        test_icd11_service,
        test_atc_service,
        test_drg_service,
        test_snomed_service,
        test_gdpr_service,
        test_nis2_service,
        test_localization_service,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    if failed == 0:
        print("✓ All tests passed! The Karolina EHR system is working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
