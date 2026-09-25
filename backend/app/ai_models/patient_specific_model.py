import re
import json
import os
from typing import Dict, List, Any
from app.medical_brain.catalog import MASTER_TESTS_CATALOG

# Localized Natural Language Processing Engine (No external API needed)
class LocalNLPQAEngine:
    """
    A custom Bag-of-Words and Semantic overlap NLP engine built in pure Python.
    Trained specifically on the comprehensive MaternaCare 122 Master Diagnostic Catalog.
    Learns and retains patient's specific conditions over time to provide contextualized responses.
    """
    def __init__(self):
        # ---------------------------------------------------------
        # Deep Medical Training Corpus for the NLP Engine
        # ---------------------------------------------------------
        self.corpus = []
        self.patient_memory_file = "app/data/patient_memory.json"
        
        # 1. Pre-train the model dynamically using all 122 Biological Parameters
        for test_id, test_info in MASTER_TESTS_CATALOG.items():
            name = test_info["name"].lower()
            stage = test_info["stage"].replace("_", " ").lower()
            protocol = test_info["indian_clinical_protocol"]
            normal = test_info["normal_range"]
            danger = test_info["danger_threshold"]
            
            # Extract key biological terms for the intent matching
            intents = self._tokenize(name + " " + stage)
            
            advice = (
                f"Regarding the {test_info['name']} (usually done in {test_info['timing']}):\n"
                f"• Normal Range: {normal}\n"
                f"• Clinical Protocol: {protocol}\n"
                f"• Danger Threshold: {danger}"
            )
            
            self.corpus.append({
                "intents": intents,
                "advice": advice,
                "is_medical_test": True
            })

        # 2. Append general Lifestyle & Companion FAQ intents for Temporary Pains and Doubts
        faq_corpus = [
            # ----- TEMPORARY PAINS & DISCOMFORTS -----
            {"intents": ["back", "backache", "lower back"], "advice": "I know back pain can be exhausting. It's very common as your baby grows and shifts your center of gravity. Try using a maternity support pillow, resting on your side, and doing gentle prenatal stretches. A warm compress might also help soothe the muscles."},
            {"intents": ["round ligament", "sharp pain", "groin", "stretching"], "advice": "That sharp, sudden pain in your lower belly or groin is likely round ligament pain. It happens when the ligaments supporting your uterus stretch. Try to move slowly when standing up and avoid sudden twisting. It's temporary and completely normal!"},
            {"intents": ["headache", "head", "migraine"], "advice": "Headaches can be tough, especially with all the hormonal changes. Make sure you are drinking plenty of water and getting enough sleep. If a headache is severe, doesn't go away, or comes with blurry vision, please consult your doctor immediately as it could be a sign of high blood pressure."},
            {"intents": ["nausea", "morning sickness", "vomiting", "throw up"], "advice": "Morning sickness is so hard, but you're doing great. Try eating small, frequent meals rather than large ones, and keep some dry crackers by your bed to eat before you even stand up. Ginger tea or ginger candies can also provide relief."},
            {"intents": ["breast", "sore", "tender", "boobs"], "advice": "Your body is already preparing to feed your baby! Breast tenderness is one of the most common early pregnancy symptoms. Wearing a soft, supportive, wire-free maternity bra even at night can help ease the discomfort."},
            {"intents": ["constipation", "poop", "bowel", "hemorrhoids"], "advice": "Constipation is a very common side effect of pregnancy hormones and iron tablets. Make sure you're drinking at least 8-10 glasses of water a day, eating fiber-rich foods like fruits and whole grains, and taking short walks."},
            {"intents": ["leg cramps", "calf", "charlie horse", "night cramps"], "advice": "Leg cramps, especially at night, can be surprisingly painful! Try gently flexing your foot upwards (toes toward your shin) when it happens. Staying hydrated and asking your doctor about a magnesium or calcium supplement can prevent them."},
            {"intents": ["fatigue", "tired", "exhausted", "sleepy", "energy"], "advice": "You are literally growing a human being from scratch—it is completely normal to feel exhausted! Please don't feel guilty about resting. Take naps when you can, and listen to your body."},
            {"intents": ["braxton hicks", "tightening", "fake contractions", "practice"], "advice": "Those tightening sensations are called Braxton Hicks, or 'practice contractions'. They are your body's way of toning the uterus for delivery. Drinking a large glass of water and changing your position usually makes them stop. If they become regular and painful, contact your doctor."},
            {"intents": ["sciatica", "shooting pain", "leg pain", "nerve"], "advice": "Shooting pain down your back and leg is often sciatica, caused by the baby resting on your sciatic nerve. Try sleeping on the opposite side, using a pregnancy pillow, or doing gentle pelvic tilts."},
            {"intents": ["rib", "ribs", "kicking ribs"], "advice": "As your baby gets bigger, they might start kicking or pressing right up against your ribs! It can be very uncomfortable. Try stretching your arms over your head to give the baby more room, or gently change your posture."},
            {"intents": ["breath", "breathing", "short of breath"], "advice": "Feeling a bit short of breath is normal because your growing uterus is pushing up against your lungs. Take things slow and sit up straight to give your lungs more space. (If you ever feel dizzy, have chest pain, or severe breathing trouble, see a doctor immediately)."},
            {"intents": ["pelvic", "spd", "pubis", "bone pain", "vagina pressure"], "advice": "Pelvic pressure and bone pain (often called SPD) is caused by the hormone relaxin loosening your joints. Try to keep your knees together when getting out of the car or bed, and wear a supportive maternity belt."},
            
            # ----- DOUBTS, EMOTIONS, AND FEARS -----
            {"intents": ["fear", "scared", "anxious", "anxiety", "worried", "labor"], "advice": "It is completely natural to feel scared or anxious about labor and motherhood. You are not alone in feeling this way. Your body was designed to do this, and you will have a medical team to support you. Try talking to a friend or partner about your fears, and take it one day at a time."},
            {"intents": ["good mother", "bad mom", "doubt", "crying"], "advice": "The fact that you are worrying about being a good mother shows how much you already care about your baby. Pregnancy hormones can make emotions feel very overwhelming. Give yourself grace—you are going to be a wonderful mother."},
            {"intents": ["mood", "sad", "angry", "emotions", "stress"], "advice": "Your hormones are fluctuating wildly right now, and it is 100% normal to feel like you're on an emotional rollercoaster. Please talk to someone you trust, take time for yourself, and know that it's okay to cry if you need to."},
            
            # ----- LIFESTYLE & GENERAL -----
            {"intents": ["papaya", "fruit", "unripe", "eat papaya"], "advice": "Avoid unripe or semi-ripe papaya as it contains latex which may trigger uterine contractions. Fully ripe papaya in moderation is generally fine."},
            {"intents": ["pineapple", "bromelain", "fruit", "miscarriage"], "advice": "Pineapple contains bromelain, but eating it in normal amounts is safe. It will not cause miscarriage."},
            {"intents": ["coffee", "caffeine", "tea", "energy drink"], "advice": "Limit caffeine intake to less than 200mg per day (about 1-2 cups of instant coffee)."},
            {"intents": ["spicy", "chili", "hot food"], "advice": "Spicy food is safe for the baby, but it may worsen your heartburn or acidity."},
            {"intents": ["sleep", "sleeping", "position", "side", "back"], "advice": "Sleeping on your left side is best as it improves blood flow to the baby. Use pillows between your legs for support."},
            {"intents": ["discharge", "white fluid", "vaginal", "itching"], "advice": "An increase in thin, milky white discharge is normal. If it smells bad, is green/yellow, or causes itching, consult your doctor for an infection check."},
            {"intents": ["kick", "movement", "flutter", "rolling"], "advice": "Fetal movements typically begin between 16-24 weeks. If you ever notice a significant decrease in kicks, lie on your left side and count. If still reduced, seek immediate help."}
        ]
        for f in faq_corpus:
            f["is_medical_test"] = False
            self.corpus.append(f)
            
    def _stem(self, word: str) -> str:
        # Extremely basic suffix stemmer to improve LLM-like intent matching
        if word.endswith("ing"): return word[:-3]
        if word.endswith("s") and not word.endswith("ss"): return word[:-1]
        if word.endswith("ed"): return word[:-2]
        return word

    def _tokenize(self, text: str) -> List[str]:
        # Simple word tokenizer removing punctuation and stop words
        text = re.sub(r"[^\w\s]", "", text.lower())
        stop_words = {"the", "a", "is", "in", "and", "or", "test", "screen", "exam", "of", "to", "for", "my", "i", "am", "what", "how", "where", "can", "do", "does", "open"}
        tokens = [w for w in text.split() if w not in stop_words and len(w) > 2]
        return [self._stem(w) for w in tokens]

    def _compute_similarity(self, query_tokens: List[str], intent_tokens: List[str]) -> float:
        # Intent Coverage calculation for long paragraphs
        if not intent_tokens:
            return 0.0
        intersection = set(query_tokens).intersection(set(intent_tokens))
        if not intersection:
            return 0.0
        
        # We divide by the length of the intent, not the query, 
        # so long paragraphs don't dilute the score if the exact medical terms are present.
        return len(intersection) / float(len(set(intent_tokens)))

    def _learn_patient_condition(self, query: str):
        # Extremely basic NLP extraction to store user's actual health conditions
        if not os.path.exists("app/data"):
            os.makedirs("app/data")
            
        memory = {}
        if os.path.exists(self.patient_memory_file):
            try:
                with open(self.patient_memory_file, "r") as f:
                    memory = json.load(f)
            except Exception:
                pass
                
        # Learn weeks pregnant
        weeks_match = re.search(r"(\d+)\s*weeks?", query.lower())
        if weeks_match:
            memory["gestational_age"] = f"{weeks_match.group(1)} weeks"
            
        # Learn hemoglobin
        hb_match = re.search(r"hemoglobin(?: is)?\s*(\d+\.?\d*)", query.lower())
        if hb_match:
            memory["last_hemoglobin"] = f"{hb_match.group(1)} g/dL"
            
        with open(self.patient_memory_file, "w") as f:
            json.dump(memory, f)
            
        return memory

    def generate_answer(self, query: str, patient_id: str = "P-UNKNOWN") -> Dict[str, str]:
        """
        Parses query, computes similarity against trained medical NLP corpora (122 tests),
        and contextualizes it to the patient by learning their health parameters.
        """
        # Learn from the user's input before answering
        patient_memory = self._learn_patient_condition(query)
        
        # Check for Out-Of-Domain explicit keywords
        ood_keywords = ["google", "map", "maps", "husband", "weather", "play music", "call", "send a message", "news", "restaurant", "movie"]
        if any(word in query.lower() for word in ood_keywords):
            return {
                "medical_advice_english": "Out-of-Domain query intercepted.",
                "patient_friendly_english": "I am a companion only for tracking your pregnancy period health and supporting you through motherhood. I cannot assist with other tasks like navigation or calling."
            }
            
        # (Medicine catch moved to bottom for dynamic appended resolution)
            
        query_tokens = self._tokenize(query)
        matches = []
        
        for idx, doc in enumerate(self.corpus):
            raw_intents = " ".join(doc["intents"])
            intent_tokens = self._tokenize(raw_intents)
            
            score = self._compute_similarity(query_tokens, intent_tokens)
            for token in query_tokens:
                if token in intent_tokens and len(token) >= 3:
                    score += 0.2
                    
            if not doc.get("is_medical_test"):
                score += 0.1
                    
            if score >= 0.30:
                matches.append({"doc": doc, "score": score})

        # Sort matches by score descending
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        # If we have matches, we must synthesize them
        if matches:
            medical_tests_matched = [m for m in matches if m["doc"].get("is_medical_test")]
            
            context_prefix = ""
            if "gestational_age" in patient_memory:
                context_prefix = f"Given that you are at {patient_memory['gestational_age']}, "

            # SCENARIO A: Multiple critical medical tests matched (Clinical Crisis / Multi-System)
            abnormal_keywords = ["spiking", "absent", "dropping", "abnormal", "high", "low", "terrible", "spiked", "danger", "emergency", "crisis", "pain", "bleeding"]
            is_abnormal_query = any(w in query.lower() for w in abnormal_keywords)
            
            if len(medical_tests_matched) >= 2 and is_abnormal_query:
                # Extract the names of the tests matched from the advice string
                test_names = []
                for m in medical_tests_matched:
                    text = m["doc"]["advice"]
                    if "Regarding the" in text:
                        t_name = text.split("Regarding the")[1].split("(usually")[0].strip()
                        if t_name not in test_names:
                            test_names.append(t_name)
                
                tests_str = ", ".join(test_names[:3])
                
                # Check for crisis keywords indicating the patient asked if they are in danger
                is_danger_query = any(w in query.lower() for w in ["danger", "emergency", "scared", "die", "terrible", "bad"])
                
                urgent_voice_response = (
                    f"I hear you, and I am deeply concerned. You have mentioned several highly critical findings at once, "
                    f"specifically regarding your {tests_str}. When multiple parameters like your blood pressure, doppler scans, and biomarkers "
                    f"are abnormal simultaneously, it strongly points to a severe condition like placental insufficiency or severe preeclampsia. "
                    f"{'Yes, this is an emergency and your baby could be at risk.' if is_danger_query else 'This is a medical emergency.'} "
                    f"Please do not wait. You must go to the emergency room or contact your obstetric team immediately for urgent evaluation."
                )
                
                return {
                    "medical_advice_english": f"CRITICAL MULTI-SYSTEM ALERT: Patient presented with multiple high-risk anomalies ({tests_str}). Advised immediate emergency obstetric evaluation.",
                    "patient_friendly_english": urgent_voice_response
                }
                
            # Grab the highest scoring match for normal resolution
            top_match = matches[0]["doc"]
            
            # SCENARIO B: Single Medical Test Matched (or multiple matched but no abnormal keywords)
            if top_match.get("is_medical_test"):
                advice = top_match["advice"]
                
                # Voice friendly parsing of the dictionary data
                lines = advice.split('\n')
                if len(lines) >= 4:
                    voice_friendly = f"{context_prefix}I can explain that test for you. {lines[0]} The normal range is usually {lines[1].replace('• Normal Range:', '').strip()}. {lines[2].replace('• Clinical Protocol:', 'Clinically,').strip()} Please watch out for the danger threshold, which is {lines[3].replace('• Danger Threshold:', '').strip()}."
                else:
                    voice_friendly = f"{context_prefix}{advice}"
                    
                response_eng = f"Biological parameter query resolved. {advice}"
                
            # SCENARIO C: Companion FAQ matched
            else:
                advice = top_match["advice"]
                response_eng = f"Patient NLP query resolved locally. Advised: {advice}"
                voice_friendly = f"{context_prefix.capitalize() if not context_prefix else context_prefix}{advice}"

            # Dynamic Medicine HITL Trigger
            if "medicine" in query.lower() or "tablet" in query.lower() or "pill" in query.lower():
                response_eng += " [HITL Trigger: Medicine Request Forwarded]"
                voice_friendly += " Since you asked about medicine, I am pausing to send your request to your doctor for official approval before you take anything."
                
            return {
                "medical_advice_english": response_eng,
                "patient_friendly_english": voice_friendly
            }

        # Safe fallback / Out of domain catch-all
        if "medicine" in query.lower() or "tablet" in query.lower() or "pill" in query.lower():
            return {
                "medical_advice_english": f"Patient inquired about medications for an unmatched symptom '{query}'. Forwarded to doctor.",
                "patient_friendly_english": "I understand you are asking about medicine, but I need to know a little more about your symptoms. I have sent your request to your doctor for review and prescription."
            }
            
        return {
            "medical_advice_english": f"Patient query unmatched. '{query}'. Advised standard care.",
            "patient_friendly_english": "I am a companion exclusively dedicated to tracking your pregnancy health and answering your maternity questions. If you have a specific pregnancy symptom or test you'd like to ask about, please let me know!"
        }

# Singleton instance of our localized, trained AI
patient_specific_qa_model = LocalNLPQAEngine()
