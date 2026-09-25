import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Protocol-aligned clinical knowledge base for maternal & neonatal continuity
CLINICAL_PROTOCOLS = {
    "PREECLAMPSIA_SIGNS": {
        "keywords": ["headache", "blurred vision", "eye pain", "spots", "epigastric", "upper abdomen pain", "swelling", "edema", "high bp", "सिरदर्द", "धुंधला", "बीपी", "सूजन"],
        "risk_category": "PREECLAMPSIA",
        "concern_level": "CLINICAL_REVIEW_RECOMMENDED",
        "clinical_rationale": "Symptoms consistent with elevated cerebral or end-organ perfusion risk in pregnancy (>20 weeks). Clinical evaluation of BP and urinalysis required.",
        "who_guideline": "WHO Recommendations for Prevention and Treatment of Pre-eclampsia and Eclampsia"
    },
    "REDUCED_FETAL_MOVEMENT": {
        "keywords": ["movement", "kicks", "not moving", "baby quiet", "less kick", "हलचल", "किक", "बच्चा हिल नहीं रहा"],
        "risk_category": "FETAL_WELLBEING",
        "concern_level": "URGENT_EMERGENCY",
        "clinical_rationale": "Subjective reduction in fetal movement requires immediate fetal cardiotocography (CTG) and obstetrical ultrasound assessment.",
        "who_guideline": "WHO Antenatal Care for a Positive Pregnancy Experience"
    },
    "VAGINAL_BLEEDING": {
        "keywords": ["bleeding", "blood", "spotting", "discharge red", "खून", "रक्तस्राव"],
        "risk_category": "ANTEPARTUM_OR_POSTPARTUM_HEMORRHAGE",
        "concern_level": "URGENT_EMERGENCY",
        "clinical_rationale": "Any vaginal bleeding during pregnancy or excessive lochia postpartum warrants urgent clinical examination.",
        "who_guideline": "WHO Guidelines for the Management of Postpartum Haemorrhage and Bleeding"
    },
    "NEONATAL_DANGER_SIGNS": {
        "keywords": ["baby cold", "baby fever", "not drinking milk", "not feeding", "lethargic", "yellow skin", "jaundice", "fast breathing", "दूध नहीं पी रहा", "पीलिया", "सांस तेज"],
        "risk_category": "NEONATAL_SEPSIS_OR_JAUNDICE",
        "concern_level": "URGENT_EMERGENCY",
        "clinical_rationale": "Neonatal danger signs (poor suckling, hypothermia/fever, tachypnea, jaundice extending to abdomen/limbs) indicate potential neonatal sepsis or hyperbilirubinemia.",
        "who_guideline": "WHO Integrated Management of Childhood Illness (IMCI)"
    },
    "ROUTINE_NUTRITION_CARE": {
        "keywords": ["diet", "food", "iron", "calcium", "supplement", "vomiting", "nausea", "खाना", "उल्टी", "आयरन"],
        "risk_category": "ROUTINE_ANTENATAL_CARE",
        "concern_level": "ROUTINE",
        "clinical_rationale": "Standard antenatal nutritional advice, adherence to daily Iron-Folic Acid (IFA) and Calcium supplementation.",
        "who_guideline": "WHO Recommendations on Antenatal Care: Nutritional Interventions"
    }
}

# Multilingual empathetic, patient-friendly guidance messages
PATIENT_FRIENDLY_TEMPLATES = {
    "PREECLAMPSIA_SIGNS": {
        "en": "We noticed you mentioned headache, changes in your vision, or swelling. In pregnancy, these can be signs that your body needs a quick check-up. Please visit your nearest health centre or speak to your doctor or ANM right away to check your blood pressure and urine. In the meantime, rest comfortably in a quiet room.",
        "hi": "नमस्ते। आपने सिरदर्द या आंखों के आगे धुंधलापन महसूस होने की बात कही है। गर्भावस्था में यह रक्तचाप (बीपी) बढ़ने का संकेत हो सकता है। कृपया तुरंत अपनी नजदीकी आशा दीदी, एएनएम या अस्पताल जाकर अपने बीपी और पेशाब की जांच करवाएं। शांत स्थान पर आराम करें और तुरंत डॉक्टर से संपर्क करें।",
        "ta": "வணக்கம். தலைவலி அல்லது பார்வை மங்கலாக இருப்பதாக நீங்கள் குறிப்பிட்டுள்ளீர்கள். கர்ப்ப காலத்தில் இது ரத்த அழுத்தம் அதிகரிப்பதற்கான அறிகுறியாக இருக்கலாம். தயவுசெய்து உடனடியாக அருகிலுள்ள சுகாதார நிலையம் அல்லது மருத்துவரை அணுகவும்.",
        "te": "నమస్కారం. మీరు తలనొప్పి లేదా కంటిచూపు మసకబారడం గురించి పేర్కొన్నారు. గర్భధారణ సమయంలో ఇది రక్తపోటు పెరుగుదలకు సంకేతం కావచ్చు. దయచేసి వెంటనే మీ దగ్గరలోని ఆసుపత్రి లేదా వైద్యుడిని సంప్రదించండి.",
        "kn": "ನಮಸ್ಕಾರ. ನೀವು ತಲೆನೋವು ಅಥವಾ ದೃಷ್ಟಿ ಮಂದವಾಗುವುದನ್ನು ತಿಳಿಸಿದ್ದೀರಿ. ಗರ್ಭಾವಸ್ಥೆಯಲ್ಲಿ ಇದು ರಕ್ತದೊತ್ತಡ ಹೆಚ್ಚಳದ ಸಂಕೇತವಾಗಿರಬಹುದು. ದಯವಿಟ್ಟು ತಕ್ಷಣವೇ ನಿಮ್ಮ ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆ ಅಥವಾ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ.",
        "bn": "নমস্কার। আপনি মাথাব্যথা বা ঝাপসা দৃষ্টির কথা উল্লেখ করেছেন। গর্ভাবস্থায় এটি রক্তচাপ বৃদ্ধির লক্ষণ হতে পারে। অনুগ্রহ করে অবিলম্বে আপনার নিকটস্থ স্বাস্থ্যকেন্দ্র বা ডাক্তারের সাথে যোগাযোগ করুন।",
        "mr": "नमस्कार. तुम्ही डोकेदुखी किंवा अंधुक दिसण्याबाबत सांगितले आहे. गरोदरपणात हे रक्तदाब वाढण्याचे लक्षण असू शकते. कृपया त्वरित जवळच्या आरोग्य केंद्रात किंवा डॉक्टरांशी संपर्क साधा.",
        "es": "Hemos detectado síntomas de dolor de cabeza o visión borrosa. En el embarazo, esto requiere una revisión médica inmediata para comprobar la presión arterial. Por favor, acuda a su centro de salud más cercano.",
        "fr": "Vous avez mentionné des maux de tête ou des troubles visuels. Pendant la grossesse, cela nécessite un contrôle rapide de la tension artérielle. Veuillez consulter immédiatement un professionnel de santé.",
        "sw": "Umeeleza kuhusu maumivu ya kichwa au matatizo ya kuona. Wakati wa ujauzito, hii inaweza kuwa dalili ya shinikizo la damu. Tafadhali muone mtoa huduma wa afya mara moja."
    },
    "REDUCED_FETAL_MOVEMENT": {
        "en": "You mentioned feeling fewer movements or kicks from your baby. Any change in baby movement is very important. Please lie down on your left side for an hour in a quiet space and concentrate on your baby. If you still do not feel clear movements, go to your maternity hospital immediately for a quick heartbeat check.",
        "hi": "आपने बच्चे की हलचल कम होने की बात कही है। बच्चे की गतिविधि बहुत महत्वपूर्ण है। कृपया तुरंत बाईं करवट लेकर लेटें और ध्यान दें। यदि हलचल साफ महसूस न हो, तो बिना देर किए तुरंत अस्पताल जाएं ताकि बच्चे की धड़कन जांची जा सके।",
        "ta": "குழந்தையின் அசைவு குறைவாக இருப்பதாக நீங்கள் கூறினீர்கள். உடனே இடது பக்கமாக படுத்து கவனியுங்கள். அசைவு தெரியவில்லை என்றால் உடனே மருத்துவமனைக்குச் செல்லுங்கள்.",
        "te": "శిశువు కదలికలు తగ్గినట్లు మీరు చెప్పారు. దయచేసి వెంటనే ఎడమ వైపు తిరిగి పడుకోండి. కదలికలు లేకపోతే వెంటనే ఆసుపత్రికి వెళ్ళండి.",
        "kn": "ಮಗುವಿನ ಚಲನೆ ಕಡಿಮೆಯಾಗಿದೆ ಎಂದು ತಿಳಿಸಿದ್ದೀರಿ. ದಯವಿಟ್ಟು ಎಡ ಮಗ್ಗುಲಾಗಿ ಮಲಗಿ ಗಮನಿಸಿ. ತಕ್ಷಣ ಆಸ್ಪತ್ರೆಗೆ ಭೇಟಿ ನೀಡಿ.",
        "bn": "আপনি শিশুর নড়াচড়া কমে যাওয়ার কথা বলেছেন। অনুগ্রহ করে অবিলম্বে বাম কাত হয়ে শুয়ে লক্ষ্য করুন এবং অবিলম্বে হাসপাতালে যান।",
        "mr": "तुम्ही बाळाची हालचाल कमी झाल्याचे सांगितले आहे. कृपया त्वरित डाव्या कुशीवर झोपून लक्ष द्या आणि तात्काळ दवाखान्यात जा.",
        "es": "Ha notado menos movimientos del bebé. Acuéstese de lado izquierdo. Si no percibe movimientos, acuda inmediatamente a urgencias obstétricas.",
        "fr": "Vous remarquez une diminution des mouvements de bébé. Allongez-vous sur le côté gauche. Si cela persiste, rendez-vous immédiatement à la maternité.",
        "sw": "Umebaini mtoto hachezi vizuri. Lala kwa upande wa kushoto. Ikiwa hakuna mabadiliko, nenda hospitali mara moja."
    },
    "VAGINAL_BLEEDING": {
        "en": "Any vaginal bleeding or unusual discharge requires immediate in-person clinical assessment. Please do not wait. Contact your doctor, midwife, or visit the nearest emergency maternity facility immediately.",
        "hi": "गर्भावस्था या प्रसव के बाद किसी भी प्रकार का रक्तस्राव (ब्लीडिंग) होने पर तुरंत चिकित्सकीय जांच जरूरी है। कृपया बिल्कुल भी इंतजार न करें और तुरंत नजदीकी अस्पताल पहुंचे।",
        "ta": "எந்தவித ரத்தப்போக்கும் அவசர மருத்துவ கவனிப்பு தேவைப்படும். உடனடியாக மருத்துவமனைக்கு செல்லவும்.",
        "te": "ఎలాంటి రక్తస్రావమైనా వెంటనే అత్యవసర వైద్య పరీక్ష అవసరం. ఆలస్యం చేయకుండా ఆసుపత్రికి వెళ్ళండి.",
        "kn": "ಯಾವುದೇ ರಕ್ತಸ್ರಾವವಾದರೂ ತಕ್ಷಣ ವೈದ್ಯಕೀಯ ತಪಾಸಣೆ ಅತ್ಯಗತ್ಯ. ತಕ್ಷಣ ಆಸ್ಪತ್ರೆಗೆ ತೆರಳಿ.",
        "bn": "যেকোনো রক্তপাতের ক্ষেত্রে অবিলম্বে জরুরি চিকিৎসার প্রয়োজন। অবিলম্বে হাসপাতালে যোগাযোগ করুন।",
        "mr": "कोणत्याही प्रकारचा रक्तस्राव झाल्यास त्वरित वैद्यकीय तपासणी आवश्यक आहे. तात्काळ रुग्णालयात जा.",
        "es": "Cualquier sangrado vaginal requiere evaluación clínica urgente e inmediata. Acuda a urgencias obstétricas.",
        "fr": "Tout saignement vaginal nécessite une évaluation médicale immédiate aux urgences de la maternité.",
        "sw": "Kutokwa na damu kunahitaji uchunguzi wa haraka wa daktari. Nenda hospitali mara moja."
    },
    "NEONATAL_DANGER_SIGNS": {
        "en": "Newborn babies require careful observation. If your baby is not feeding well, feels unusually cold or hot, breathes very fast, or appears yellow, please take your baby to the hospital or SNCU immediately.",
        "hi": "नवजात शिशु के स्वास्थ्य में विशेष सावधानी चाहिए। यदि शिशु दूध नहीं पी पा रहा है, शरीर ठंडा या बहुत गर्म है, सांस तेज चल रही है या पीलापन दिख रहा है, तो तुरंत डॉक्टर या शिशु अस्पताल (SNCU) लेकर जाएं।",
        "ta": "பச்சிளம் குழந்தை பால் குடிக்கவில்லை என்றாலோ, சோர்வாக இருந்தாலோ உடனே குழந்தைகள் மருத்துவரிடம் காட்டவும்.",
        "te": "నవజాత శిశువు పాలు తాగకపోతే లేదా నీరసంగా ఉంటే వెంటనే శిశువైద్యుడిని సంప్రదించండి.",
        "kn": "ನವಜಾತ ಶಿಶು ಹಾಲು ಕುಡಿಯದಿದ್ದರೆ ಅಥವಾ ಜ್ವರವಿದ್ದರೆ ತಕ್ಷಣ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ.",
        "bn": "নবজাতক শিশু যদি দুধ না খায় বা অসুস্থ মনে হয়, তবে অবিলম্বে শিশু বিশেষজ্ঞের কাছে নিয়ে যান।",
        "mr": "नवजात बाळ दूध पीत नसेल किंवा ताप असेल तर त्वरित बालरोगतज्ज्ञांकडे घेऊन जा.",
        "es": "Los recién nacidos con dificultad para alimentarse, fiebre o respiración rápida deben ser evaluados de urgencia por pediatría.",
        "fr": "Un nouveau-né qui refuse de téter ou respira vite doit être vu en urgence par un pédiatre.",
        "sw": "Mtoto mchanga asiyenyonya vizuri au mwenye homa anapaswa kupelekwa hospitali mara moja."
    },
    "ROUTINE_NUTRITION_CARE": {
        "en": "For a healthy pregnancy, continue eating iron-rich foods like green leafy vegetables, lentils, and fresh fruits. Remember to take your daily Iron and Calcium tablets as advised by your healthcare provider, and stay well hydrated.",
        "hi": "स्वस्थ गर्भावस्था के लिए हरी पत्तेदार सब्जियां, दालें, दूध और मौसमी फल खाएं। अपनी आशा दीदी या डॉक्टर द्वारा दी गई आयरन और कैल्शियम की गोलियां नियमित लें और पर्याप्त पानी पिएं।",
        "ta": "ஆரோக்கியமான கர்ப்பத்திற்கு கீரைகள், பருப்பு வகைகள் மற்றும் பழங்களை உட்கொள்ளுங்கள். இரும்புச்சத்து மாத்திரைகளை தவறாமல் எடுத்துக்கொள்ளுங்கள்.",
        "te": "ఆరోగ్యకరమైన గర్భధారణ కోసం ఆకుకూరలు, పండ్లు తీసుకోండి. ఐరన్ మరియు కాల్షియం మాత్రలు రోజూ వేసుకోండి.",
        "kn": "ಆರೋಗ್ಯಕರ ಗರ್ಭಾವಸ್ಥೆಗಾಗಿ ಸೊಪ್ಪು, ಕಾಳುಗಳು ಮತ್ತು ಹಣ್ಣುಗಳನ್ನು ಸೇವಿಸಿ. ಐರನ್ ಮತ್ತು ಕ್ಯಾಲ್ಸಿಯಂ ಮಾತ್ರೆಗಳನ್ನು ತಪ್ಪದೇ ಸೇವಿಸಿ.",
        "bn": "সুস্থ গর্ভাবস্থার জন্য শাকসবজি, ডাল ও পুষ্টিকর খাবার খান। নিয়মিত আয়রন ও ক্যালসিয়াম ওষুধ গ্রহণ করুন।",
        "mr": "निरोगी गरोदरपणासाठी हिरव्या पालेभाज्या, डाळी आणि फळे खा. डॉक्टरांनी दिलेल्या आयर्न आणि कॅल्शियमच्या गोळ्या वेळेवर घ्या.",
        "es": "Mantenga una dieta equilibrada con alimentos ricos en hierro y continúe con sus suplementos prenatales.",
        "fr": "Maintenez une alimentation équilibrée riche en fer et prenez vos suppléments prescrits.",
        "sw": "Kula vyakula vyenye madini ya chuma kama mboga za majani na unywe vidonge vyako vya virutubisho kila siku."
    }
}


class MedicalPregnancyIntelligenceModel:
    """
    Maternal & Neonatal Pregnancy Knowledge Intelligence Engine.
    Strictly follows clinical ethics:
    - Never claims to diagnose.
    - Standardizes clinical concern phrasing: 'Potentially concerning pattern detected — clinical review recommended.'
    - Provides human-in-the-loop triage flags and plain-language patient explanations.
    """

    def __init__(self, model_version: str = "maternacare-clinical-kg-v1.0"):
        self.model_version = model_version
        logger.info(f"Initialized Medical Pregnancy Intelligence Model: {self.model_version}")

    def analyze_clinical_query(
        self,
        query_text: str,
        language: str = "en",
        patient_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate text query against clinical protocols, patient longitudinal context, and WHO guidelines.
        """
        query_lower = query_text.lower()
        matched_protocol_key = "ROUTINE_NUTRITION_CARE"
        highest_severity = "ROUTINE"
        clinical_review_recommended = False
        potential_risk_flags = []
        clinical_findings = []

        # Check against protocol knowledge base
        for key, protocol in CLINICAL_PROTOCOLS.items():
            for kw in protocol["keywords"]:
                if kw in query_lower:
                    matched_protocol_key = key
                    highest_severity = protocol["concern_level"]
                    if protocol["concern_level"] in ["CLINICAL_REVIEW_RECOMMENDED", "URGENT_EMERGENCY"]:
                        clinical_review_recommended = True
                        potential_risk_flags.append(protocol["risk_category"])
                        clinical_findings.append({
                            "symptom_or_sign": kw,
                            "concern_level": protocol["concern_level"],
                            "recommendation": protocol["clinical_rationale"]
                        })
                    break
            if clinical_review_recommended and highest_severity == "URGENT_EMERGENCY":
                break

        # Grounding with patient's longitudinal history if provided
        history_note = ""
        if patient_context:
            ga = patient_context.get("gestational_age")
            if ga:
                history_note += f" [Gestational Age: {ga} weeks]"
            prev_pre = patient_context.get("previous_preeclampsia")
            if prev_pre and matched_protocol_key == "PREECLAMPSIA_SIGNS":
                potential_risk_flags.append("HIGH_RISK_OBSTETRIC_HISTORY_PREECLAMPSIA")
                clinical_review_recommended = True

        # Generate standard clinical summary for healthcare professionals
        if clinical_review_recommended:
            medical_advice_text = (
                f"Potentially concerning pattern detected — clinical review recommended. "
                f"Protocol flagged: {matched_protocol_key}.{history_note} "
                f"Rationale: {CLINICAL_PROTOCOLS[matched_protocol_key]['clinical_rationale']} "
                f"Governed under: {CLINICAL_PROTOCOLS[matched_protocol_key]['who_guideline']}."
            )
        else:
            medical_advice_text = (
                f"Routine clinical query detected.{history_note} "
                f"Rationale: {CLINICAL_PROTOCOLS[matched_protocol_key]['clinical_rationale']} "
                f"Governed under: {CLINICAL_PROTOCOLS[matched_protocol_key]['who_guideline']}."
            )

        # Generate culturally sensitive plain language response for the patient
        lang_key = language if language in PATIENT_FRIENDLY_TEMPLATES.get(matched_protocol_key, {}) else "en"
        patient_friendly_text = PATIENT_FRIENDLY_TEMPLATES[matched_protocol_key].get(
            lang_key, PATIENT_FRIENDLY_TEMPLATES[matched_protocol_key]["en"]
        )

        suggested_actions = []
        if highest_severity == "URGENT_EMERGENCY":
            suggested_actions = [
                "Immediate referral or transfer to nearest emergency obstetric/neonatal care facility",
                "Perform urgent vital check: BP, Maternal Pulse, SpO2, FHR",
                "Notify attending obstetrician/pediatrician on call"
            ]
        elif highest_severity == "CLINICAL_REVIEW_RECOMMENDED":
            suggested_actions = [
                "Schedule priority clinical review within 24 hours",
                "Measure blood pressure in sitting position using calibrated sphygmomanometer",
                "Perform dipstick urinalysis for proteinuria",
                "Educate patient on warning signs and danger signs"
            ]
        else:
            suggested_actions = [
                "Continue routine antenatal/postpartum visits according to schedule",
                "Maintain adequate hydration and balanced nutrition",
                "Adhere to daily micronutrient supplementation (IFA, Calcium)"
            ]

        return {
            "query_evaluated": query_text,
            "detected_protocol": matched_protocol_key,
            "concern_level": highest_severity,
            "clinical_review_recommended": clinical_review_recommended,
            "potential_risk_flags": list(set(potential_risk_flags)),
            "medical_advice_text": medical_advice_text,
            "patient_friendly_text": patient_friendly_text,
            "clinical_findings": clinical_findings,
            "suggested_actions": suggested_actions,
            "model_version": self.model_version
        }


# Singleton instance
pregnancy_knowledge_model = MedicalPregnancyIntelligenceModel()
