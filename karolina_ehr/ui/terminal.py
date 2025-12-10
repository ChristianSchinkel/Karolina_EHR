"""
Terminal User Interface for Karolina EHR.

Provides a text-based interface for interacting with the EHR system.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from karolina_ehr.models import (
    User, Nurse, Doctor, Patient, SOAPNote, WorkSchedule, UserRole
)
from karolina_ehr.services import (
    LocalizationService, GDPRService, NIS2Service,
    ICD11Service, ATCService, DRGService, SNOMEDService
)


class TerminalUI:
    """Main terminal user interface."""
    
    def __init__(self):
        self.console = Console()
        self.locale_service = LocalizationService(locale="en")
        self.gdpr_service = GDPRService()
        self.nis2_service = NIS2Service()
        self.current_user: Optional[User] = None
        
        # In-memory storage (in production, this would be a database)
        self.users: List[User] = []
        self.patients: List[Patient] = []
        self.soap_notes: List[SOAPNote] = []
        self.schedules: List[WorkSchedule] = []
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample users for demonstration."""
        # Create sample nurse
        nurse = Nurse(
            username="nurse1",
            license_number="N12345",
            department="Emergency"
        )
        self.users.append(nurse)
        
        # Create sample doctor
        doctor = Doctor(
            username="dr_smith",
            license_number="D67890",
            specialization="Internal Medicine"
        )
        self.users.append(doctor)
        
        # Create sample patient
        patient = Patient(
            username="patient1",
            personal_id="19900101-1234",
            consent_given=True,
            consent_date=datetime.now()
        )
        self.users.append(patient)
        self.patients.append(patient)
    
    def run(self):
        """Main application loop."""
        self.show_welcome()
        self.select_language()
        
        if self.login():
            while True:
                choice = self.show_main_menu()
                
                if choice == "1":
                    self.patient_management()
                elif choice == "2":
                    self.soap_notes_management()
                elif choice == "3":
                    self.work_schedule_management()
                elif choice == "4":
                    self.settings()
                elif choice == "5":
                    self.logout()
                    if not self.login():
                        break
                elif choice == "6":
                    self.console.print("\n[yellow]Thank you for using Karolina EHR![/yellow]")
                    break
    
    def show_welcome(self):
        """Display welcome screen."""
        self.console.clear()
        welcome_panel = Panel(
            "[bold cyan]Karolina Electronic Health Record System[/bold cyan]\n\n"
            "[green]GDPR & NIS2 Compliant[/green]\n"
            "[blue]Supporting ICD-11, ATC, DRG, and SNOMED-CT[/blue]",
            title="Welcome",
            border_style="cyan"
        )
        self.console.print(welcome_panel)
        self.console.print()
    
    def select_language(self):
        """Allow user to select language."""
        self.console.print("\n[bold]Select Language / Välj språk / Sprache wählen:[/bold]")
        self.console.print("1. English")
        self.console.print("2. Svenska (Swedish)")
        self.console.print("3. Deutsch (German)")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3"], default="1")
        
        locale_map = {"1": "en", "2": "sv", "3": "de"}
        self.locale_service.set_locale(locale_map[choice])
        
        self.console.print(f"\n[green]✓ {self.locale_service.get('language_' + locale_map[choice])} selected[/green]")
    
    def login(self) -> bool:
        """Handle user login."""
        self.console.print(f"\n[bold]{self.locale_service.get('login')}[/bold]")
        
        username = Prompt.ask(self.locale_service.get('username'))
        
        # Find user (simplified - no password in this demo)
        user = next((u for u in self.users if u.username == username), None)
        
        if user:
            self.current_user = user
            self.console.print(f"[green]✓ {self.locale_service.get('login')} successful![/green]")
            self.console.print(f"[cyan]{self.locale_service.get('role')}: {user.role.value}[/cyan]")
            
            # Log login event
            self.gdpr_service.log_access(
                user_id=user.id,
                action="login",
                resource_type="system",
                resource_id="main"
            )
            
            return True
        else:
            self.console.print("[red]✗ Invalid credentials[/red]")
            return False
    
    def logout(self):
        """Handle user logout."""
        if self.current_user:
            self.gdpr_service.log_access(
                user_id=self.current_user.id,
                action="logout",
                resource_type="system",
                resource_id="main"
            )
            self.current_user = None
        self.console.print(f"[yellow]{self.locale_service.get('menu_logout')} successful[/yellow]")
    
    def show_main_menu(self) -> str:
        """Display main menu and get user choice."""
        self.console.print(f"\n[bold cyan]{self.locale_service.get('menu_main')}[/bold cyan]")
        self.console.print(f"1. {self.locale_service.get('menu_patient_management')}")
        self.console.print(f"2. {self.locale_service.get('menu_soap_notes')}")
        self.console.print(f"3. {self.locale_service.get('menu_work_schedule')}")
        self.console.print(f"4. {self.locale_service.get('menu_settings')}")
        self.console.print(f"5. {self.locale_service.get('menu_logout')}")
        self.console.print(f"6. {self.locale_service.get('menu_exit')}")
        
        return Prompt.ask("Choice", choices=["1", "2", "3", "4", "5", "6"])
    
    def patient_management(self):
        """Handle patient management."""
        if not self.nis2_service.validate_access(
            self.current_user.role.value, "patient", "read"
        ):
            self.console.print(f"[red]{self.locale_service.get('error_access_denied')}[/red]")
            return
        
        self.console.print(f"\n[bold]{self.locale_service.get('menu_patient_management')}[/bold]")
        self.console.print(f"1. {self.locale_service.get('patient_list')}")
        self.console.print(f"2. {self.locale_service.get('patient_add')}")
        self.console.print(f"3. {self.locale_service.get('back')}")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3"])
        
        if choice == "1":
            self.list_patients()
        elif choice == "2":
            self.add_patient()
    
    def list_patients(self):
        """Display list of patients."""
        table = Table(title=self.locale_service.get('patient_list'))
        table.add_column("ID", style="cyan")
        table.add_column(self.locale_service.get('username'), style="magenta")
        table.add_column(self.locale_service.get('consent_given'), style="green")
        
        for patient in self.patients:
            consent_status = "✓" if patient.consent_given else "✗"
            table.add_row(patient.id[:8], patient.username, consent_status)
        
        self.console.print(table)
        
        # Log access
        self.gdpr_service.log_access(
            user_id=self.current_user.id,
            action="list",
            resource_type="patient",
            resource_id="all"
        )
    
    def add_patient(self):
        """Add a new patient."""
        if not self.nis2_service.validate_access(
            self.current_user.role.value, "patient", "write"
        ):
            self.console.print(f"[red]{self.locale_service.get('error_access_denied')}[/red]")
            return
        
        self.console.print(f"\n[bold]{self.locale_service.get('patient_add')}[/bold]")
        
        username = Prompt.ask(self.locale_service.get('username'))
        personal_id = Prompt.ask("Personal ID")
        consent = Confirm.ask(self.locale_service.get('consent_required'))
        
        patient = Patient(
            username=username,
            personal_id=personal_id,
            consent_given=consent,
            consent_date=datetime.now() if consent else None
        )
        
        self.patients.append(patient)
        self.users.append(patient)
        
        self.console.print(f"[green]✓ {self.locale_service.get('success_saved')}[/green]")
        
        # Log creation
        self.gdpr_service.log_access(
            user_id=self.current_user.id,
            action="create",
            resource_type="patient",
            resource_id=patient.id
        )
    
    def soap_notes_management(self):
        """Handle SOAP notes management."""
        if not self.nis2_service.validate_access(
            self.current_user.role.value, "soap_note", "read"
        ):
            self.console.print(f"[red]{self.locale_service.get('error_access_denied')}[/red]")
            return
        
        self.console.print(f"\n[bold]{self.locale_service.get('menu_soap_notes')}[/bold]")
        self.console.print(f"1. {self.locale_service.get('soap_create')}")
        self.console.print(f"2. {self.locale_service.get('soap_view')}")
        self.console.print(f"3. {self.locale_service.get('back')}")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3"])
        
        if choice == "1":
            self.create_soap_note()
        elif choice == "2":
            self.view_soap_notes()
    
    def create_soap_note(self):
        """Create a new SOAP note."""
        if not self.nis2_service.validate_access(
            self.current_user.role.value, "soap_note", "write"
        ):
            self.console.print(f"[red]{self.locale_service.get('error_access_denied')}[/red]")
            return
        
        self.console.print(f"\n[bold]{self.locale_service.get('soap_create')}[/bold]")
        
        # Select patient
        if not self.patients:
            self.console.print("[yellow]No patients available[/yellow]")
            return
        
        self.console.print("\nSelect Patient:")
        for i, patient in enumerate(self.patients, 1):
            self.console.print(f"{i}. {patient.username}")
        
        patient_choice = Prompt.ask("Patient number", choices=[str(i) for i in range(1, len(self.patients) + 1)])
        selected_patient = self.patients[int(patient_choice) - 1]
        
        # SOAP components
        subjective = Prompt.ask(f"{self.locale_service.get('soap_subjective')}")
        objective = Prompt.ask(f"{self.locale_service.get('soap_objective')}")
        assessment = Prompt.ask(f"{self.locale_service.get('soap_assessment')}")
        plan = Prompt.ask(f"{self.locale_service.get('soap_plan')}")
        
        # Optional medical codes
        self.console.print("\n[dim]Optional: Add medical codes (press Enter to skip)[/dim]")
        icd11 = Prompt.ask(f"{self.locale_service.get('icd11_code')}", default="")
        atc = Prompt.ask(f"{self.locale_service.get('atc_code')}", default="")
        drg = Prompt.ask(f"{self.locale_service.get('drg_code')}", default="")
        snomed = Prompt.ask(f"{self.locale_service.get('snomed_code')}", default="")
        
        soap_note = SOAPNote(
            patient_id=selected_patient.id,
            author_id=self.current_user.id,
            subjective=subjective,
            objective=objective,
            assessment=assessment,
            plan=plan,
            icd11_codes=[icd11] if icd11 else [],
            atc_codes=[atc] if atc else [],
            drg_code=drg if drg else None,
            snomed_codes=[snomed] if snomed else []
        )
        
        self.soap_notes.append(soap_note)
        
        self.console.print(f"\n[green]✓ {self.locale_service.get('success_saved')}[/green]")
        
        # Show validation of codes
        if icd11 and ICD11Service.validate_code(icd11):
            desc = ICD11Service.get_description(icd11)
            if desc:
                self.console.print(f"[cyan]ICD-11: {desc}[/cyan]")
        
        if atc and ATCService.validate_code(atc):
            desc = ATCService.get_description(atc)
            if desc:
                self.console.print(f"[cyan]ATC: {desc}[/cyan]")
        
        # Log creation
        self.gdpr_service.log_access(
            user_id=self.current_user.id,
            action="create",
            resource_type="soap_note",
            resource_id=soap_note.id,
            details=f"For patient {selected_patient.id}"
        )
    
    def view_soap_notes(self):
        """View SOAP notes."""
        if not self.soap_notes:
            self.console.print("[yellow]No SOAP notes available[/yellow]")
            return
        
        table = Table(title=self.locale_service.get('soap_view'))
        table.add_column("ID", style="cyan")
        table.add_column("Patient", style="magenta")
        table.add_column("Date", style="green")
        table.add_column("Assessment", style="yellow")
        
        for note in self.soap_notes:
            patient = next((p for p in self.patients if p.id == note.patient_id), None)
            patient_name = patient.username if patient else "Unknown"
            
            table.add_row(
                note.id[:8],
                patient_name,
                note.created_at.strftime("%Y-%m-%d"),
                note.assessment[:30] + "..." if len(note.assessment) > 30 else note.assessment
            )
        
        self.console.print(table)
        
        # Log access
        self.gdpr_service.log_access(
            user_id=self.current_user.id,
            action="view",
            resource_type="soap_note",
            resource_id="all"
        )
    
    def work_schedule_management(self):
        """Handle work schedule management."""
        if not self.nis2_service.validate_access(
            self.current_user.role.value, "schedule", "read"
        ):
            self.console.print(f"[red]{self.locale_service.get('error_access_denied')}[/red]")
            return
        
        self.console.print(f"\n[bold]{self.locale_service.get('menu_work_schedule')}[/bold]")
        self.console.print(f"1. {self.locale_service.get('schedule_view')}")
        self.console.print(f"2. {self.locale_service.get('schedule_add')}")
        self.console.print(f"3. {self.locale_service.get('back')}")
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3"])
        
        if choice == "1":
            self.view_schedule()
        elif choice == "2":
            self.add_schedule()
    
    def view_schedule(self):
        """View work schedule."""
        if not self.schedules:
            self.console.print("[yellow]No schedules available[/yellow]")
            return
        
        table = Table(title=self.locale_service.get('schedule_view'))
        table.add_column("Staff", style="cyan")
        table.add_column("Date", style="magenta")
        table.add_column("Shift", style="green")
        table.add_column("Department", style="yellow")
        
        for schedule in self.schedules:
            staff = next((u for u in self.users if u.id == schedule.staff_id), None)
            staff_name = staff.username if staff else "Unknown"
            
            table.add_row(
                staff_name,
                schedule.start_time.strftime("%Y-%m-%d"),
                schedule.shift_type,
                schedule.department
            )
        
        self.console.print(table)
    
    def add_schedule(self):
        """Add a work schedule entry."""
        if not self.nis2_service.validate_access(
            self.current_user.role.value, "schedule", "write"
        ):
            self.console.print(f"[red]{self.locale_service.get('error_access_denied')}[/red]")
            return
        
        self.console.print(f"\n[bold]{self.locale_service.get('schedule_add')}[/bold]")
        
        department = Prompt.ask("Department")
        shift_type = Prompt.ask("Shift type", choices=["day", "night", "evening"])
        
        # Calculate end time based on shift type (8 hours for simplicity)
        from datetime import timedelta
        start = datetime.now()
        end = start + timedelta(hours=8)
        
        schedule = WorkSchedule(
            staff_id=self.current_user.id,
            department=department,
            shift_type=shift_type,
            start_time=start,
            end_time=end
        )
        
        self.schedules.append(schedule)
        
        self.console.print(f"[green]✓ {self.locale_service.get('success_saved')}[/green]")
        
        # Log creation
        self.gdpr_service.log_access(
            user_id=self.current_user.id,
            action="create",
            resource_type="schedule",
            resource_id=schedule.id
        )
    
    def settings(self):
        """Handle settings."""
        self.console.print(f"\n[bold]{self.locale_service.get('menu_settings')}[/bold]")
        self.console.print("1. Change Language")
        self.console.print(f"2. {self.locale_service.get('back')}")
        
        choice = Prompt.ask("Choice", choices=["1", "2"])
        
        if choice == "1":
            self.select_language()
