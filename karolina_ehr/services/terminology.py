"""
Medical terminology services for ICD-11, ATC, DRG, and SNOMED-CT.

These services provide validation and lookup for medical codes.
In a production system, these would connect to external databases or APIs.
"""
from typing import Optional, Dict, List


class ICD11Service:
    """ICD-11 (International Classification of Diseases, 11th Revision) service.
    
    Provides diagnosis coding according to WHO ICD-11 standard.
    """
    
    # Sample ICD-11 codes for demonstration
    SAMPLE_CODES = {
        "1A00": "Cholera",
        "1B10": "Intestinal infections due to Escherichia coli",
        "1C62.0": "COVID-19",
        "8A62": "Diabetes mellitus, type 2",
        "BA00": "Essential hypertension",
        "9B71.0Z": "Depression",
    }
    
    @staticmethod
    def validate_code(code: str) -> bool:
        """Validate if an ICD-11 code is properly formatted."""
        if not code:
            return False
        # ICD-11 codes typically follow patterns like: 1A00, 8A62, BA00, etc.
        return len(code) >= 4 and code[0].isalnum()
    
    @staticmethod
    def get_description(code: str) -> Optional[str]:
        """Get description for an ICD-11 code."""
        return ICD11Service.SAMPLE_CODES.get(code)
    
    @staticmethod
    def search(query: str) -> List[Dict[str, str]]:
        """Search ICD-11 codes by description."""
        results = []
        query_lower = query.lower()
        for code, desc in ICD11Service.SAMPLE_CODES.items():
            if query_lower in desc.lower():
                results.append({"code": code, "description": desc})
        return results


class ATCService:
    """ATC (Anatomical Therapeutic Chemical) classification service.
    
    Provides drug coding according to WHO ATC standard.
    """
    
    # Sample ATC codes for demonstration
    SAMPLE_CODES = {
        "A02BC01": "Omeprazole - Proton pump inhibitor",
        "C09AA01": "Captopril - ACE inhibitor",
        "N02BE01": "Paracetamol - Analgesic/Antipyretic",
        "J01CA04": "Amoxicillin - Penicillin antibiotic",
        "A10BA02": "Metformin - Antidiabetic drug",
        "C07AB02": "Metoprolol - Beta blocker",
    }
    
    @staticmethod
    def validate_code(code: str) -> bool:
        """Validate if an ATC code is properly formatted.
        
        ATC format: Letter-2Digits-2Letters-2Digits (e.g., A10BA02)
        """
        if not code or len(code) != 7:
            return False
        # Pattern: Letter-Number-Number-Letter-Letter-Number-Number
        return (code[0].isalpha() and 
                code[1:3].isdigit() and 
                code[3:5].isalpha() and 
                code[5:7].isdigit())
    
    @staticmethod
    def get_description(code: str) -> Optional[str]:
        """Get description for an ATC code."""
        return ATCService.SAMPLE_CODES.get(code)
    
    @staticmethod
    def search(query: str) -> List[Dict[str, str]]:
        """Search ATC codes by drug name or description."""
        results = []
        query_lower = query.lower()
        for code, desc in ATCService.SAMPLE_CODES.items():
            if query_lower in desc.lower():
                results.append({"code": code, "description": desc})
        return results


class DRGService:
    """DRG (Diagnosis Related Group) service.
    
    Provides DRG coding for hospital billing and resource allocation.
    """
    
    # Sample DRG codes for demonstration
    SAMPLE_CODES = {
        "001": "Heart Transplant or Implant of Heart Assist System",
        "190": "Chronic Obstructive Pulmonary Disease",
        "291": "Heart Failure & Shock",
        "470": "Major Joint Replacement or Reattachment of Lower Extremity",
        "683": "Renal Failure",
    }
    
    @staticmethod
    def validate_code(code: str) -> bool:
        """Validate if a DRG code is properly formatted."""
        return code.isdigit() and len(code) == 3
    
    @staticmethod
    def get_description(code: str) -> Optional[str]:
        """Get description for a DRG code."""
        return DRGService.SAMPLE_CODES.get(code)


class SNOMEDService:
    """SNOMED-CT (Systematized Nomenclature of Medicine - Clinical Terms) service.
    
    Provides clinical terminology coding.
    """
    
    # Sample SNOMED-CT codes for demonstration
    SAMPLE_CODES = {
        "386661006": "Fever",
        "25064002": "Headache",
        "49727002": "Cough",
        "271807003": "Rash",
        "13791008": "Asthma",
        "38341003": "Hypertensive disorder",
    }
    
    @staticmethod
    def validate_code(code: str) -> bool:
        """Validate if a SNOMED-CT code is properly formatted."""
        return code.isdigit() and len(code) >= 6
    
    @staticmethod
    def get_description(code: str) -> Optional[str]:
        """Get description for a SNOMED-CT code."""
        return SNOMEDService.SAMPLE_CODES.get(code)
    
    @staticmethod
    def search(query: str) -> List[Dict[str, str]]:
        """Search SNOMED-CT codes by clinical term."""
        results = []
        query_lower = query.lower()
        for code, desc in SNOMEDService.SAMPLE_CODES.items():
            if query_lower in desc.lower():
                results.append({"code": code, "description": desc})
        return results
