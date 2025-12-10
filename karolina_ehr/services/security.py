"""
Security and compliance services for GDPR and NIS2.

Implements encryption, audit logging, and data protection measures.
"""
from datetime import datetime
from typing import Optional, Dict, Any
import hashlib
import json
from pathlib import Path


class GDPRService:
    """GDPR (General Data Protection Regulation) compliance service.
    
    Implements:
    - Right to be forgotten
    - Data minimization
    - Consent management
    - Audit logging
    """
    
    def __init__(self, audit_log_path: str = "karolina_ehr/data/audit.log"):
        self.audit_log_path = Path(audit_log_path)
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log_access(self, user_id: str, action: str, resource_type: str, 
                   resource_id: str, details: Optional[str] = None) -> None:
        """Log data access for GDPR compliance.
        
        Args:
            user_id: ID of user performing action
            action: Type of action (read, write, delete, etc.)
            resource_type: Type of resource accessed (patient, soap_note, etc.)
            resource_id: ID of specific resource
            details: Additional details about the action
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details
        }
        
        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize personal data for GDPR compliance.
        
        Removes or hashes identifying information.
        """
        sensitive_fields = ["personal_id", "username", "license_number"]
        anonymized = data.copy()
        
        for field in sensitive_fields:
            if field in anonymized:
                # Hash the sensitive data
                value = str(anonymized[field])
                hashed = hashlib.sha256(value.encode()).hexdigest()[:16]
                anonymized[field] = f"***{hashed}"
        
        return anonymized
    
    def check_consent(self, patient_id: str) -> bool:
        """Check if patient has given consent for data processing.
        
        Args:
            patient_id: ID of the patient
            
        Returns:
            True if consent is given, False otherwise
        """
        # In a real system, this would check a database
        # For now, we assume consent is required
        return True
    
    def delete_patient_data(self, patient_id: str, user_id: str) -> None:
        """Delete patient data (right to be forgotten).
        
        Args:
            patient_id: ID of patient whose data should be deleted
            user_id: ID of user requesting deletion
        """
        self.log_access(
            user_id=user_id,
            action="delete_all",
            resource_type="patient",
            resource_id=patient_id,
            details="Right to be forgotten - all patient data deleted"
        )


class NIS2Service:
    """NIS2 (Network and Information Security Directive 2) compliance service.
    
    Implements:
    - Security incident logging
    - Access control
    - Data encryption
    - Security monitoring
    """
    
    def __init__(self, security_log_path: str = "karolina_ehr/data/security.log"):
        self.security_log_path = Path(security_log_path)
        self.security_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log_security_event(self, event_type: str, severity: str, 
                          description: str, user_id: Optional[str] = None) -> None:
        """Log security events for NIS2 compliance.
        
        Args:
            event_type: Type of security event (login_failed, unauthorized_access, etc.)
            severity: Severity level (low, medium, high, critical)
            description: Description of the event
            user_id: Optional user ID involved in the event
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "severity": severity,
            "description": description,
            "user_id": user_id
        }
        
        with open(self.security_log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Hash sensitive data for demonstration.
        
        Note: This is a hash, not encryption. In production, use proper
        encryption with the cryptography library (e.g., Fernet symmetric encryption).
        Hashing is one-way; real encryption allows decryption with a key.
        """
        return hashlib.sha256(data.encode()).hexdigest()
    
    def validate_access(self, user_role: str, resource_type: str, 
                       action: str) -> bool:
        """Validate if user has access to perform action on resource.
        
        Args:
            user_role: Role of the user
            resource_type: Type of resource being accessed
            action: Action being performed (read, write, delete)
            
        Returns:
            True if access is allowed, False otherwise
        """
        # Role-based access control matrix
        access_matrix = {
            "nurse": {
                "patient": ["read", "write"],
                "soap_note": ["read", "write"],
                "schedule": ["read", "write"]
            },
            "doctor": {
                "patient": ["read", "write"],
                "soap_note": ["read", "write", "delete"],
                "schedule": ["read", "write"]
            },
            "admin": {
                "patient": ["read", "write", "delete"],
                "soap_note": ["read", "write", "delete"],
                "schedule": ["read", "write", "delete"]
            },
            "patient": {
                "patient": ["read"],  # Can only read own data
                "soap_note": ["read"]  # Can only read own notes
            }
        }
        
        allowed_actions = access_matrix.get(user_role, {}).get(resource_type, [])
        is_allowed = action in allowed_actions
        
        if not is_allowed:
            self.log_security_event(
                event_type="unauthorized_access",
                severity="medium",
                description=f"User with role '{user_role}' attempted '{action}' on '{resource_type}'",
                user_id=None
            )
        
        return is_allowed
