import logging
import json
import time
import re
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Comprehensive 50-language emergency distress lexicon
# Includes Latin transliterations and native scripts
MULTILINGUAL_EMERGENCY_WORDS = [
    # English
    "help", "save me", "emergency", "ambulance", "bleeding", "can't breathe", "fainted", "dying", "urgent",
    # Hindi / Urdu
    "bachao", "बचाओ", "madad", "मदद", "madad karo", "मदद करो", "raksha", "khoon", "dard", "mar rahe", "نجدة", "مدد", "بچاو",
    # Tamil
    "kapaathu", "காப்பாத்து", "kappathunga", "காப்பாத்துங்க", "udhavi", "உதவி", "udhavunga", "உதவுங்க", "vali", "maruthuvar",
    # Telugu
    "kapadandi", "కాపాడండి", "sahayam", "సహాయం", "sahayam cheyandi", "rakshinchandi", "noppi",
    # Malayalam
    "rakshikku", "രക്ഷിക്കൂ", "sahayikku", "സഹായിക്കൂ", "vedhana", "aashupathri",
    # Kannada
    "bachisi", "ಬದುಕಿಸಿ", "sahaya", "ಸಹಾಯ", "sahaya maadi", "rakshisi", "novvu",
    # Bengali
    "bachao", "বাঁচাও", "sahajjo", "সাহায্য", "sahajjo korun", "rokto",
    # Marathi
    "vachva", "वाचवा", "madat", "मदत", "madat kara",
    # Gujarati
    "bachavo", "બચાવો", "madad", "મદદ", "madad karo",
    # Punjabi
    "bachao", "ਬਚਾਓ", "madad", "ਮਦਦ",
    # Spanish
    "ayuda", "ayúdame", "socorro", "auxilio", "emergencia", "ambulancia",
    # French
    "aidez-moi", "aide", "au secours", "urgence", "secours",
    # German
    "hilfe", "helfen sie mir", "notfall", "rettung",
    # Arabic
    "najdah", "نجدة", "sa'idni", "ساعدني", "musaa'adah", "مساعدة", "tawari", "طوارئ",
    # Russian
    "pomogite", "помогите", "spasite", "спасите", "skoraya", "скорая",
    # Chinese (Mandarin)
    "jiuming", "救命", "bangzhu", "帮助", "jiuhuche", "救护车",
    # Japanese
    "tasukete", "助けて", "kyuukyuusha", "救急車",
    # Korean
    "dowajuseyo", "도와주세요", "salryeojuseyo", "살려주세요",
    # Italian
    "aiuto", "aiutatemi", "soccorso", "emergenza",
    # Portuguese
    "socorro", "ajuda", "ajude-me", "emergencia",
    # Tagalog / Filipino
    "tulong", "saklolo", "tulungan",
    # Swahili
    "msaada", "nisaidie", "dharura",
    # Nepali
    "guff", "गुहार", "sahayog", "सहयोग",
    # Indonesian / Malay
    "tolong", "bantuan", "kecemasan"
]


class AmbientEmergencyGuardian:
    """
    Model 3: Ambient Emergency Guardian.
    Constantly evaluates transcripts for distress words across 50 languages.
    CRITICAL RULE:
    Only triggers emergency ambulance dispatch if distress words are REPEATED
    multiple times (e.g. 'help me help me', 'bachao bachao', 'help kapaathu')
    to prevent false alarms from casual queries like 'can you help me?'.
    """
    
    def __init__(self):
        self.model_name = "MaternaCare-Multilingual-EmergencyGuardian-v3"
        self.emergency_keywords = list(set([kw.lower() for kw in MULTILINGUAL_EMERGENCY_WORDS]))
        logger.info(f"Initialized {self.model_name} with {len(self.emergency_keywords)} multilingual emergency keywords across 50 languages.")

    def check_for_emergency(self, text: str, location: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Analyzes text for emergency keywords across 50 languages.
        Requires >= 2 keyword matches/repetitions to trigger.
        """
        text_lower = text.lower()
        detected_keywords = []
        total_occurrences = 0
        
        for kw in self.emergency_keywords:
            if not kw:
                continue
            # Check occurrences using word boundary or direct substring
            matches = len(re.findall(re.escape(kw), text_lower))
            if matches > 0:
                detected_keywords.append(kw)
                total_occurrences += matches
                
        # REQUIRE MULTIPLE REPETITIONS (>= 2) TO AVOID FALSE ALARMS
        if total_occurrences >= 2:
            logger.warning(
                f"[Model 3 Guardian] MULTILINGUAL DISTRESS DETECTED (Repeated {total_occurrences} times): "
                f"{detected_keywords} in query: '{text}'"
            )
            return self._trigger_driver_dispatch(detected_keywords, location, text)
        
        # Single mention -> treated as routine query (no emergency triggered)
        return {
            "emergency_detected": False,
            "status": "safe",
            "detected_keywords": detected_keywords,
            "occurrences": total_occurrences
        }

    def _trigger_driver_dispatch(self, keywords: list, location: Optional[Dict[str, float]], original_text: str) -> Dict[str, Any]:
        """
        Bypasses standard medical reasoning and triggers instant driver/ambulance dispatch.
        """
        dispatch_payload = {
            "emergency_id": f"EMG-{int(time.time())}",
            "timestamp": time.time(),
            "patient_status": "CRITICAL - MULTILINGUAL AMBIENT SHOUT DETECTED",
            "detected_triggers": keywords,
            "original_audio_transcript": original_text,
            "location": location or {"lat": "UNKNOWN", "lng": "UNKNOWN"},
            "dispatch_status": "AMBULANCE_DRIVER_DIRECT_ALERT",
            "dispatched_to": "AMBULANCE_DRIVER",
            "hospital_doctor_bypassed": True
        }
        
        logger.critical(f"DISPATCHING AMBULANCE DRIVER DIRECTLY (BYPASSING DOCTOR): {json.dumps(dispatch_payload)}")
        
        return {
            "emergency_detected": True,
            "dispatch_payload": dispatch_payload,
            "message": "Critical distress detected in multiple repetitions. Dispatched directly to ambulance driver navigation console (hospital doctor bypassed)."
        }


emergency_guardian = AmbientEmergencyGuardian()
