import logging
import json
import time
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AmbientEmergencyGuardian:
    """
    Model 3: Ambient Emergency Guardian.
    Constantly listens for emergency keywords ("help", "bachao", "bhao", "kapaathu").
    Upon detecting an emergency word, it bypasses the standard pipeline and
    immediately sends an alert containing the pregnant woman's location and 
    emergency context directly to a "driver panel" (ambulance/transport dispatch).
    """
    
    def __init__(self):
        self.model_name = "MaternaCare-EmergencyGuardian-v1"
        self.emergency_keywords = [
            "help", "bachao", "bhao", "kapaathu", "emergency", 
            "save me", "ambulance", "bleeding heavily", "fainted"
        ]
        logger.info(f"Initialized {self.model_name} with keywords: {self.emergency_keywords}")

    def check_for_emergency(self, text: str, location: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Analyzes the incoming text for emergency keywords.
        Returns a dictionary indicating if an emergency was detected and the alert payload.
        Only triggers if emergency words are used repeatedly (to prevent false alarms from medical questions).
        """
        text_lower = text.lower()
        detected_keywords = []
        total_occurrences = 0
        
        for kw in self.emergency_keywords:
            # Count how many times the keyword appears in the text
            count = text_lower.count(kw)
            if count > 0:
                detected_keywords.append(kw)
                total_occurrences += count
                
        # Trigger ONLY if the user is shouting it repeatedly (>= 2 times) 
        # or uses multiple different emergency words (e.g. "help", "ambulance")
        if total_occurrences >= 2:
            logger.warning(f"EMERGENCY KEYWORDS DETECTED (Repeatedly): {detected_keywords} (Total: {total_occurrences})")
            return self._trigger_driver_dispatch(detected_keywords, location, text)
        
        return {
            "emergency_detected": False,
            "status": "safe"
        }

    def _trigger_driver_dispatch(self, keywords: list, location: Optional[Dict[str, float]], original_text: str) -> Dict[str, Any]:
        """
        Simulates bypassing the main pipeline and directly dispatching to the driver panel.
        """
        # In a real scenario, this would make an HTTP POST to the driver's app backend or SMS gateway.
        dispatch_payload = {
            "emergency_id": f"EMG-{int(time.time())}",
            "timestamp": time.time(),
            "patient_status": "CRITICAL - AMBIENT ALERT",
            "detected_triggers": keywords,
            "original_audio_transcript": original_text,
            "location": location or {"lat": "UNKNOWN", "lng": "UNKNOWN"},
            "dispatch_status": "DRIVER_NOTIFIED_DIRECTLY"
        }
        
        logger.critical(f"DISPATCHING AMBULANCE DIRECTLY: {json.dumps(dispatch_payload)}")
        
        return {
            "emergency_detected": True,
            "dispatch_payload": dispatch_payload,
            "message": "Emergency detected. Driver panel notified immediately."
        }

emergency_guardian = AmbientEmergencyGuardian()
