"""
Localization service for Swedish, English, and German.

Provides translation support for the EHR system.
"""
from typing import Dict, Optional
import json
from pathlib import Path


class LocalizationService:
    """Manages translations for multiple languages."""
    
    def __init__(self, locale: str = "en"):
        """Initialize localization service.
        
        Args:
            locale: Language code (en, sv, de)
        """
        self.locale = locale
        self.translations: Dict[str, Dict[str, str]] = {}
        self.load_translations()
    
    def load_translations(self) -> None:
        """Load translations from locale files."""
        locales_dir = Path("karolina_ehr/locales")
        
        for lang in ["en", "sv", "de"]:
            locale_file = locales_dir / lang / "messages.json"
            if locale_file.exists():
                with open(locale_file, "r", encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)
            else:
                self.translations[lang] = {}
    
    def get(self, key: str, **kwargs) -> str:
        """Get translated string for current locale.
        
        Args:
            key: Translation key
            **kwargs: Format arguments for string interpolation
            
        Returns:
            Translated string, or key if translation not found
        """
        translation = self.translations.get(self.locale, {}).get(key, key)
        
        if kwargs:
            try:
                return translation.format(**kwargs)
            except KeyError:
                return translation
        
        return translation
    
    def set_locale(self, locale: str) -> None:
        """Change current locale.
        
        Args:
            locale: Language code (en, sv, de)
        """
        if locale in ["en", "sv", "de"]:
            self.locale = locale
    
    def get_available_locales(self) -> list:
        """Get list of available locales."""
        return ["en", "sv", "de"]
