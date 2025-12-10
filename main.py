"""
Karolina Electronic Health Record System

A terminal-based EHR application compliant with GDPR and NIS2.
Supports ICD-11, ATC, DRG, and SNOMED-CT medical coding standards.
Available in Swedish, English, and German.

Usage:
    python main.py
"""
from karolina_ehr.ui.terminal import TerminalUI


def main():
    """Main entry point for Karolina EHR application."""
    app = TerminalUI()
    app.run()


if __name__ == "__main__":
    main()
