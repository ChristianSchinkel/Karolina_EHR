#!/usr/bin/env python3
"""
Demo script showing Karolina EHR System capabilities.

This script demonstrates all major features without requiring user interaction.
"""

from datetime import datetime, timedelta
from karolina_ehr.models import Nurse, Doctor, Patient, SOAPNote, WorkSchedule
from karolina_ehr.services import (
    ICD11Service, ATCService, DRGService, SNOMEDService,
    GDPRService, NIS2Service, LocalizationService
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


def main():
    """Run the demo."""
    console = Console()
    
    # Welcome banner
    console.print()
    banner = Panel(
        "[bold cyan]Karolina Electronic Health Record System[/bold cyan]\n\n"
        "[green]✓ GDPR Compliant with Audit Logging[/green]\n"
        "[green]✓ NIS2 Compliant with Role-Based Access Control[/green]\n"
        "[blue]✓ ICD-11, ATC, DRG, SNOMED-CT Support[/blue]\n"
        "[yellow]✓ Multi-language: English, Swedish, German[/yellow]",
        title="Demo",
        border_style="cyan"
    )
    console.print(banner)
    
    # Initialize services
    gdpr = GDPRService()
    nis2 = NIS2Service()
    
    # Demo 1: User Management
    console.print("\n[bold magenta]1. User Management[/bold magenta]")
    nurse = Nurse(username="anna_svensson", license_number="N12345", department="Emergency")
    doctor = Doctor(username="dr_larsson", license_number="D67890", specialization="Internal Medicine")
    patient = Patient(
        username="erik_johansson",
        personal_id="19850615-1234",
        consent_given=True,
        consent_date=datetime.now()
    )
    
    table = Table(title="Hospital Staff & Patients")
    table.add_column("Username", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Details", style="green")
    
    table.add_row(nurse.username, nurse.role.value, f"Dept: {nurse.department}")
    table.add_row(doctor.username, doctor.role.value, f"Spec: {doctor.specialization}")
    table.add_row(patient.username, patient.role.value, f"Consent: {'✓' if patient.consent_given else '✗'}")
    
    console.print(table)
    
    # Demo 2: SOAP Note with Medical Codes
    console.print("\n[bold magenta]2. SOAP Clinical Documentation[/bold magenta]")
    
    soap = SOAPNote(
        patient_id=patient.id,
        author_id=doctor.id,
        subjective="Patient reports persistent headache for 3 days, worse in morning",
        objective="BP 145/95 mmHg, HR 82 bpm, Temp 37.1°C, Alert and oriented",
        assessment="Tension headache with mild hypertension",
        plan="Prescribe paracetamol 500mg PRN, lifestyle counseling, follow-up in 2 weeks",
        icd11_codes=["25064002", "BA00"],  # Headache, Hypertension
        atc_codes=["N02BE01"],  # Paracetamol
        drg_code="291",  # Heart Failure & Shock (example)
        snomed_codes=["25064002", "38341003"]  # Headache, Hypertensive disorder
    )
    
    console.print(Panel(
        f"[cyan]Patient:[/cyan] {patient.username}\n"
        f"[cyan]Author:[/cyan] {doctor.username}\n\n"
        f"[yellow]S:[/yellow] {soap.subjective}\n"
        f"[yellow]O:[/yellow] {soap.objective}\n"
        f"[yellow]A:[/yellow] {soap.assessment}\n"
        f"[yellow]P:[/yellow] {soap.plan}",
        title="SOAP Note",
        border_style="green"
    ))
    
    # Log SOAP note creation
    gdpr.log_access(
        user_id=doctor.id,
        action="create",
        resource_type="soap_note",
        resource_id=soap.id,
        details=f"SOAP note for patient {patient.username}"
    )
    
    # Demo 3: Medical Coding
    console.print("\n[bold magenta]3. Medical Terminology Validation[/bold magenta]")
    
    coding_table = Table(title="Medical Codes in SOAP Note")
    coding_table.add_column("Standard", style="cyan")
    coding_table.add_column("Code", style="yellow")
    coding_table.add_column("Description", style="green")
    coding_table.add_column("Valid", style="magenta")
    
    # ICD-11
    for code in soap.icd11_codes:
        valid = "✓" if ICD11Service.validate_code(code) else "✗"
        desc = ICD11Service.get_description(code) or "N/A"
        coding_table.add_row("ICD-11", code, desc, valid)
    
    # ATC
    for code in soap.atc_codes:
        valid = "✓" if ATCService.validate_code(code) else "✗"
        desc = ATCService.get_description(code) or "N/A"
        coding_table.add_row("ATC", code, desc, valid)
    
    # DRG
    if soap.drg_code:
        valid = "✓" if DRGService.validate_code(soap.drg_code) else "✗"
        desc = DRGService.get_description(soap.drg_code) or "N/A"
        coding_table.add_row("DRG", soap.drg_code, desc, valid)
    
    # SNOMED
    for code in soap.snomed_codes:
        valid = "✓" if SNOMEDService.validate_code(code) else "✗"
        desc = SNOMEDService.get_description(code) or "N/A"
        coding_table.add_row("SNOMED-CT", code, desc, valid)
    
    console.print(coding_table)
    
    # Demo 4: Work Schedule
    console.print("\n[bold magenta]4. Work Schedule Management[/bold magenta]")
    
    schedules = [
        WorkSchedule(
            staff_id=nurse.id,
            start_time=datetime.now().replace(hour=7, minute=0),
            end_time=datetime.now().replace(hour=15, minute=0),
            department="Emergency",
            shift_type="day"
        ),
        WorkSchedule(
            staff_id=doctor.id,
            start_time=datetime.now().replace(hour=8, minute=0),
            end_time=datetime.now().replace(hour=17, minute=0),
            department="Internal Medicine",
            shift_type="day"
        )
    ]
    
    schedule_table = Table(title="Today's Schedule")
    schedule_table.add_column("Staff", style="cyan")
    schedule_table.add_column("Department", style="yellow")
    schedule_table.add_column("Shift", style="green")
    schedule_table.add_column("Hours", style="magenta")
    
    for schedule in schedules:
        staff_name = nurse.username if schedule.staff_id == nurse.id else doctor.username
        hours = f"{schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}"
        schedule_table.add_row(staff_name, schedule.department, schedule.shift_type, hours)
    
    console.print(schedule_table)
    
    # Demo 5: Security & Access Control
    console.print("\n[bold magenta]5. NIS2 Security & Access Control[/bold magenta]")
    
    security_table = Table(title="Role-Based Access Control")
    security_table.add_column("Role", style="cyan")
    security_table.add_column("Resource", style="yellow")
    security_table.add_column("Action", style="green")
    security_table.add_column("Allowed", style="magenta")
    
    access_checks = [
        ("doctor", "soap_note", "write", True),
        ("nurse", "soap_note", "write", True),
        ("patient", "soap_note", "write", False),
        ("nurse", "patient", "delete", False),
        ("doctor", "patient", "read", True),
        ("patient", "patient", "read", True),
    ]
    
    for role, resource, action, expected in access_checks:
        allowed = nis2.validate_access(role, resource, action)
        status = "✓" if allowed else "✗"
        security_table.add_row(role, resource, action, status)
    
    console.print(security_table)
    
    # Demo 6: Localization
    console.print("\n[bold magenta]6. Multi-Language Support[/bold magenta]")
    
    lang_table = Table(title="Localization Examples")
    lang_table.add_column("Language", style="cyan")
    lang_table.add_column("Welcome Message", style="green")
    
    for lang_code, lang_name in [("en", "English"), ("sv", "Swedish"), ("de", "German")]:
        locale = LocalizationService(lang_code)
        welcome = locale.get("welcome")
        lang_table.add_row(lang_name, welcome)
    
    console.print(lang_table)
    
    # Demo 7: GDPR Compliance
    console.print("\n[bold magenta]7. GDPR Compliance Features[/bold magenta]")
    
    console.print(Panel(
        "[green]✓[/green] All data access logged to audit trail\n"
        "[green]✓[/green] Patient consent tracked and validated\n"
        "[green]✓[/green] Personal data can be anonymized\n"
        "[green]✓[/green] Right to be forgotten supported\n"
        "[green]✓[/green] Data minimization principles applied",
        title="GDPR Features",
        border_style="green"
    ))
    
    # Summary
    console.print("\n[bold cyan]" + "="*60 + "[/bold cyan]")
    console.print("[bold green]✓ Demo Complete![/bold green]")
    console.print("\n[dim]This demo showcased:[/dim]")
    console.print("  • User management (Nurses, Doctors, Patients)")
    console.print("  • SOAP clinical documentation")
    console.print("  • Medical coding (ICD-11, ATC, DRG, SNOMED-CT)")
    console.print("  • Work schedule management")
    console.print("  • Security & access control (NIS2)")
    console.print("  • Multi-language support (EN, SV, DE)")
    console.print("  • GDPR compliance features")
    console.print("\n[yellow]To run the interactive application:[/yellow]")
    console.print("  [cyan]python main.py[/cyan]")
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")


if __name__ == "__main__":
    main()
