# 200-Question Bank for MedChain Patient AI Assistant grouped into 7 Categories
from typing import List, Dict, Any

QUESTIONS: List[Dict[str, Any]] = [
    # Category 1: Patient Profile & Context (Q1 - Q28)
    {"id": 1, "category": "Patient Profile & Context", "question_text": "What is my full name, age, sex, and preferred language for medical explanations?", "requires_records": True},
    {"id": 2, "category": "Patient Profile & Context", "question_text": "What is my primary reason for using the MedChain system today?", "requires_records": False},
    {"id": 3, "category": "Patient Profile & Context", "question_text": "What is my main health concern or question right now?", "requires_records": False},
    {"id": 4, "category": "Patient Profile & Context", "question_text": "How do I choose between a simple explanation, a detailed medical explanation, or both?", "requires_records": False},
    {"id": 5, "category": "Patient Profile & Context", "question_text": "Who is my primary care doctor or usual treating physician in the system?", "requires_records": True},
    {"id": 6, "category": "Patient Profile & Context", "question_text": "Which specialists am I currently seeing, and for what conditions?", "requires_records": True},
    {"id": 7, "category": "Patient Profile & Context", "question_text": "What hospital, clinic, or health system do I usually visit?", "requires_records": True},
    {"id": 8, "category": "Patient Profile & Context", "question_text": "What is my emergency contact and my relationship to them?", "requires_records": True},
    {"id": 9, "category": "Patient Profile & Context", "question_text": "What are my communication preferences, such as phone, email, or app notifications?", "requires_records": True},
    {"id": 10, "category": "Patient Profile & Context", "question_text": "Do my records show any accessibility needs, like visual, hearing, or mobility support?", "requires_records": True},
    {"id": 11, "category": "Patient Profile & Context", "question_text": "When did I first register on MedChain?", "requires_records": True},
    {"id": 12, "category": "Patient Profile & Context", "question_text": "What is my current insurance or primary billing method?", "requires_records": True},
    {"id": 13, "category": "Patient Profile & Context", "question_text": "Who is authorized to view my medical profile?", "requires_records": True},
    {"id": 14, "category": "Patient Profile & Context", "question_text": "What clinic location is my profile associated with?", "requires_records": True},
    {"id": 15, "category": "Patient Profile & Context", "question_text": "Who is my secondary emergency contact?", "requires_records": True},
    {"id": 16, "category": "Patient Profile & Context", "question_text": "Are my basic demographic details updated in the system?", "requires_records": True},
    {"id": 17, "category": "Patient Profile & Context", "question_text": "How do I request a correction to my profile data?", "requires_records": False},
    {"id": 18, "category": "Patient Profile & Context", "question_text": "Can I set a preferred pronoun for my care team?", "requires_records": False},
    {"id": 19, "category": "Patient Profile & Context", "question_text": "How can I translate my medical summaries into Spanish or other languages?", "requires_records": False},
    {"id": 20, "category": "Patient Profile & Context", "question_text": "What steps are required to update my contact information?", "requires_records": False},
    {"id": 21, "category": "Patient Profile & Context", "question_text": "Is my height and weight recorded in my profile?", "requires_records": True},
    {"id": 22, "category": "Patient Profile & Context", "question_text": "Does my profile list my date of birth?", "requires_records": True},
    {"id": 23, "category": "Patient Profile & Context", "question_text": "Is there a record of my primary language preference?", "requires_records": True},
    {"id": 24, "category": "Patient Profile & Context", "question_text": "How can I contact my primary provider through the app?", "requires_records": False},
    {"id": 25, "category": "Patient Profile & Context", "question_text": "What is the name of the clinic where my records are kept?", "requires_records": True},
    {"id": 26, "category": "Patient Profile & Context", "question_text": "Can I list multiple phone numbers in my profile?", "requires_records": False},
    {"id": 27, "category": "Patient Profile & Context", "question_text": "Who should be contacted in case of a medical emergency?", "requires_records": True},
    {"id": 28, "category": "Patient Profile & Context", "question_text": "Where can I view my registered user profile details?", "requires_records": True},

    # Category 2: Symptoms & Chief Complaint (Q29 - Q56)
    {"id": 29, "category": "Symptoms & Chief Complaint", "question_text": "What symptoms is the patient currently experiencing?", "requires_records": False},
    {"id": 30, "category": "Symptoms & Chief Complaint", "question_text": "When did the current symptoms start?", "requires_records": False},
    {"id": 31, "category": "Symptoms & Chief Complaint", "question_text": "Did the symptoms begin suddenly or gradually?", "requires_records": False},
    {"id": 32, "category": "Symptoms & Chief Complaint", "question_text": "Are the symptoms getting better, worse, or staying the same?", "requires_records": False},
    {"id": 33, "category": "Symptoms & Chief Complaint", "question_text": "How severe are the symptoms on a scale from 0 to 10?", "requires_records": False},
    {"id": 34, "category": "Symptoms & Chief Complaint", "question_text": "Where exactly is the symptom located, if applicable?", "requires_records": False},
    {"id": 35, "category": "Symptoms & Chief Complaint", "question_text": "Does the symptom spread or radiate to another area?", "requires_records": False},
    {"id": 36, "category": "Symptoms & Chief Complaint", "question_text": "What makes the symptoms better or worse?", "requires_records": False},
    {"id": 37, "category": "Symptoms & Chief Complaint", "question_text": "Have I experienced these symptoms before in my record history?", "requires_records": True},
    {"id": 38, "category": "Symptoms & Chief Complaint", "question_text": "Are there other accompanying symptoms, like fever, chills, or nausea?", "requires_records": False},
    {"id": 39, "category": "Symptoms & Chief Complaint", "question_text": "What does a sudden onset of chest pain indicate?", "requires_records": False},
    {"id": 40, "category": "Symptoms & Chief Complaint", "question_text": "What are the common warning signs of a stroke?", "requires_records": False},
    {"id": 41, "category": "Symptoms & Chief Complaint", "question_text": "How can I tell if my headache is a migraine or something else?", "requires_records": False},
    {"id": 42, "category": "Symptoms & Chief Complaint", "question_text": "What causes sudden short-term dizziness when standing up?", "requires_records": False},
    {"id": 43, "category": "Symptoms & Chief Complaint", "question_text": "When should a persistent cough be evaluated by a doctor?", "requires_records": False},
    {"id": 44, "category": "Symptoms & Chief Complaint", "question_text": "What are common signs of infection in a skin wound?", "requires_records": False},
    {"id": 45, "category": "Symptoms & Chief Complaint", "question_text": "How does dehydration affect symptoms of fatigue?", "requires_records": False},
    {"id": 46, "category": "Symptoms & Chief Complaint", "question_text": "What causes muscle cramps and how can they be relieved?", "requires_records": False},
    {"id": 47, "category": "Symptoms & Chief Complaint", "question_text": "What should I do if I experience sudden shortness of breath?", "requires_records": False},
    {"id": 48, "category": "Symptoms & Chief Complaint", "question_text": "How does stress manifest as physical symptoms?", "requires_records": False},
    {"id": 49, "category": "Symptoms & Chief Complaint", "question_text": "How long should a mild fever last before seeing a doctor?", "requires_records": False},
    {"id": 50, "category": "Symptoms & Chief Complaint", "question_text": "What are common triggers for acid reflux symptoms?", "requires_records": False},
    {"id": 51, "category": "Symptoms & Chief Complaint", "question_text": "Is joint stiffness in the morning a symptom of arthritis?", "requires_records": False},
    {"id": 52, "category": "Symptoms & Chief Complaint", "question_text": "What causes lower back pain and when is it serious?", "requires_records": False},
    {"id": 53, "category": "Symptoms & Chief Complaint", "question_text": "What should I do if I notice blood in my cough?", "requires_records": False},
    {"id": 54, "category": "Symptoms & Chief Complaint", "question_text": "What are common symptoms of seasonal allergies?", "requires_records": False},
    {"id": 55, "category": "Symptoms & Chief Complaint", "question_text": "What causes sudden ear pain and how is it evaluated?", "requires_records": False},
    {"id": 56, "category": "Symptoms & Chief Complaint", "question_text": "When is fatigue considered a medical concern?", "requires_records": False},

    # Category 3: Medical History & Conditions (Q57 - Q85)
    {"id": 57, "category": "Medical History & Conditions", "question_text": "What are my currently active diagnoses and chronic conditions?", "requires_records": True},
    {"id": 58, "category": "Medical History & Conditions", "question_text": "When was my diabetes or hypertension first diagnosed?", "requires_records": True},
    {"id": 59, "category": "Medical History & Conditions", "question_text": "What does my diagnosis of high cholesterol mean for my heart health?", "requires_records": False},
    {"id": 60, "category": "Medical History & Conditions", "question_text": "Do I have any documented surgeries or hospitalizations in my records?", "requires_records": True},
    {"id": 61, "category": "Medical History & Conditions", "question_text": "How is asthma typically managed on a daily basis?", "requires_records": False},
    {"id": 62, "category": "Medical History & Conditions", "question_text": "What is the difference between Type 1 and Type 2 diabetes?", "requires_records": False},
    {"id": 63, "category": "Medical History & Conditions", "question_text": "How does high blood pressure damage arteries over time?", "requires_records": False},
    {"id": 64, "category": "Medical History & Conditions", "question_text": "What are the long-term management strategies for osteoarthritis?", "requires_records": False},
    {"id": 65, "category": "Medical History & Conditions", "question_text": "Does my record show any history of heart palpitations?", "requires_records": True},
    {"id": 66, "category": "Medical History & Conditions", "question_text": "What chronic conditions in my list require regular blood monitoring?", "requires_records": True},
    {"id": 67, "category": "Medical History & Conditions", "question_text": "What is sleep apnea and how does it impact cardiovascular health?", "requires_records": False},
    {"id": 68, "category": "Medical History & Conditions", "question_text": "Are there any thyroid disorders noted in my health summary?", "requires_records": True},
    {"id": 69, "category": "Medical History & Conditions", "question_text": "What does a diagnosis of gastroesophageal reflux disease (GERD) involve?", "requires_records": False},
    {"id": 70, "category": "Medical History & Conditions", "question_text": "What are the common triggers for eczema flare-ups?", "requires_records": False},
    {"id": 71, "category": "Medical History & Conditions", "question_text": "Is chronic kidney disease reversible, or how is it slowed?", "requires_records": False},
    {"id": 72, "category": "Medical History & Conditions", "question_text": "Do I have any past childhood medical conditions listed?", "requires_records": True},
    {"id": 73, "category": "Medical History & Conditions", "question_text": "What are the key symptoms of rheumatoid arthritis?", "requires_records": False},
    {"id": 74, "category": "Medical History & Conditions", "question_text": "What is osteoporosis and how is bone density maintained?", "requires_records": False},
    {"id": 75, "category": "Medical History & Conditions", "question_text": "Does my history show any prior treatments for iron-deficiency anemia?", "requires_records": True},
    {"id": 76, "category": "Medical History & Conditions", "question_text": "What is the clinical definition of metabolic syndrome?", "requires_records": False},
    {"id": 77, "category": "Medical History & Conditions", "question_text": "Are there any respiratory conditions documented in my file?", "requires_records": True},
    {"id": 78, "category": "Medical History & Conditions", "question_text": "Do my records show a history of shingles?", "requires_records": True},
    {"id": 79, "category": "Medical History & Conditions", "question_text": "What are the stages of chronic kidney disease?", "requires_records": False},
    {"id": 80, "category": "Medical History & Conditions", "question_text": "Is there a record of me having chickenpox as a child?", "requires_records": True},
    {"id": 81, "category": "Medical History & Conditions", "question_text": "What is pre-diabetes and can it be reversed?", "requires_records": False},
    {"id": 82, "category": "Medical History & Conditions", "question_text": "Do I have any history of migraine headaches recorded?", "requires_records": True},
    {"id": 83, "category": "Medical History & Conditions", "question_text": "What is COPD and what are its primary causes?", "requires_records": False},
    {"id": 84, "category": "Medical History & Conditions", "question_text": "Do my records document any cardiovascular interventions?", "requires_records": True},
    {"id": 85, "category": "Medical History & Conditions", "question_text": "What are the common symptoms of hypothyroidism?", "requires_records": False},

    # Category 4: Medications & Allergies (Q86 - Q114)
    {"id": 86, "category": "Medications & Allergies", "question_text": "What medications am I currently prescribed, and what are their dosages?", "requires_records": True},
    {"id": 87, "category": "Medications & Allergies", "question_text": "What are the instructions for taking my prescribed medications?", "requires_records": True},
    {"id": 88, "category": "Medications & Allergies", "question_text": "How many refills do I have left for my active prescriptions?", "requires_records": True},
    {"id": 89, "category": "Medications & Allergies", "question_text": "What are the potential side effects of Lisinopril or Metformin?", "requires_records": False},
    {"id": 90, "category": "Medications & Allergies", "question_text": "Are there any food or drug interactions I should avoid with my medications?", "requires_records": True},
    {"id": 91, "category": "Medications & Allergies", "question_text": "What should I do if I accidentally miss a dose of my blood pressure medication?", "requires_records": False},
    {"id": 92, "category": "Medications & Allergies", "question_text": "Do my records show when my medication course is scheduled to end?", "requires_records": True},
    {"id": 93, "category": "Medications & Allergies", "question_text": "What is the purpose of taking Atorvastatin?", "requires_records": False},
    {"id": 94, "category": "Medications & Allergies", "question_text": "Am I currently taking any over-the-counter medications that should be recorded?", "requires_records": False},
    {"id": 95, "category": "Medications & Allergies", "question_text": "How does insulin help regulate blood sugar levels?", "requires_records": False},
    {"id": 96, "category": "Medications & Allergies", "question_text": "What is the difference between brand-name and generic drugs?", "requires_records": False},
    {"id": 97, "category": "Medications & Allergies", "question_text": "Are there any vitamins or herbal supplements listed in my chart?", "requires_records": True},
    {"id": 98, "category": "Medications & Allergies", "question_text": "Can I stop taking my antibiotics once I start feeling better?", "requires_records": False},
    {"id": 99, "category": "Medications & Allergies", "question_text": "Which of my medications should be taken with food?", "requires_records": True},
    {"id": 100, "category": "Medications & Allergies", "question_text": "What is a beta-blocker and how does it lower heart rate?", "requires_records": False},
    {"id": 101, "category": "Medications & Allergies", "question_text": "Do my records contain any expired prescriptions?", "requires_records": True},
    {"id": 102, "category": "Medications & Allergies", "question_text": "How should medications be safely stored at home?", "requires_records": False},
    {"id": 103, "category": "Medications & Allergies", "question_text": "What should I do if my medication looks different from the last refill?", "requires_records": False},
    {"id": 104, "category": "Medications & Allergies", "question_text": "Which of my prescriptions was filled most recently?", "requires_records": True},
    {"id": 105, "category": "Medications & Allergies", "question_text": "Do I have any documented drug allergies in the system?", "requires_records": True},
    {"id": 106, "category": "Medications & Allergies", "question_text": "What is the difference between a medication side effect and an allergy?", "requires_records": False},
    {"id": 107, "category": "Medications & Allergies", "question_text": "What are the common symptoms of an allergic reaction to penicillin?", "requires_records": False},
    {"id": 108, "category": "Medications & Allergies", "question_text": "Do my records show any food allergies, like nuts or shellfish?", "requires_records": True},
    {"id": 109, "category": "Medications & Allergies", "question_text": "What is anaphylaxis and how is it treated in emergency situations?", "requires_records": False},
    {"id": 110, "category": "Medications & Allergies", "question_text": "How does an antihistamine work to relieve allergy symptoms?", "requires_records": False},
    {"id": 111, "category": "Medications & Allergies", "question_text": "Are there any seasonal environmental allergies noted in my file?", "requires_records": True},
    {"id": 112, "category": "Medications & Allergies", "question_text": "What are the symptoms of lactose intolerance vs milk allergy?", "requires_records": False},
    {"id": 113, "category": "Medications & Allergies", "question_text": "Does my history indicate any reaction to contrast dye used in scans?", "requires_records": True},
    {"id": 114, "category": "Medications & Allergies", "question_text": "When is an EpiPen necessary for an allergic reaction?", "requires_records": False},

    # Category 5: Lifestyle & Family History (Q115 - Q142)
    {"id": 115, "category": "Lifestyle & Family History", "question_text": "Does my medical history contain family details regarding heart disease?", "requires_records": True},
    {"id": 116, "category": "Lifestyle & Family History", "question_text": "How does a family history of diabetes influence my personal risk?", "requires_records": False},
    {"id": 117, "category": "Lifestyle & Family History", "question_text": "What hereditary risk factors for cancer should I discuss with my doctor?", "requires_records": False},
    {"id": 118, "category": "Lifestyle & Family History", "question_text": "Are my living situation, support network, or caregiver details in the system?", "requires_records": True},
    {"id": 119, "category": "Lifestyle & Family History", "question_text": "What is genetic counseling and who is it recommended for?", "requires_records": False},
    {"id": 120, "category": "Lifestyle & Family History", "question_text": "Does my record capture my current employment status or occupation?", "requires_records": True},
    {"id": 121, "category": "Lifestyle & Family History", "question_text": "How does physical work or desk work affect spinal and muscle health?", "requires_records": False},
    {"id": 122, "category": "Lifestyle & Family History", "question_text": "Are my habits regarding tobacco or alcohol use documented in my file?", "requires_records": True},
    {"id": 123, "category": "Lifestyle & Family History", "question_text": "What resources are available for smoking cessation?", "requires_records": False},
    {"id": 124, "category": "Lifestyle & Family History", "question_text": "How does high stress at home or work impact overall physical health?", "requires_records": False},
    {"id": 125, "category": "Lifestyle & Family History", "question_text": "Are my dietary preferences or exercise habits listed in my profile?", "requires_records": True},
    {"id": 126, "category": "Lifestyle & Family History", "question_text": "What is a balanced diet for managing hypertension?", "requires_records": False},
    {"id": 127, "category": "Lifestyle & Family History", "question_text": "How much exercise is recommended per week for general fitness?", "requires_records": False},
    {"id": 128, "category": "Lifestyle & Family History", "question_text": "How much daily water intake is recommended for an average adult?", "requires_records": False},
    {"id": 129, "category": "Lifestyle & Family History", "question_text": "How does caffeine consumption affect sleep quality and blood pressure?", "requires_records": False},
    {"id": 130, "category": "Lifestyle & Family History", "question_text": "What are healthy habits to improve sleep duration and depth?", "requires_records": False},
    {"id": 131, "category": "Lifestyle & Family History", "question_text": "Do I have a list of recent vaccinations, like flu or COVID-19, in my profile?", "requires_records": True},
    {"id": 132, "category": "Lifestyle & Family History", "question_text": "When am I due for my next vaccine boosters?", "requires_records": True},
    {"id": 133, "category": "Lifestyle & Family History", "question_text": "What screening tests (mammogram, colonoscopy, etc.) are recommended for my age?", "requires_records": False},
    {"id": 134, "category": "Lifestyle & Family History", "question_text": "How does regular physical activity help lower blood sugar levels?", "requires_records": False},
    {"id": 135, "category": "Lifestyle & Family History", "question_text": "What are the health risks associated with a sedentary lifestyle?", "requires_records": False},
    {"id": 136, "category": "Lifestyle & Family History", "question_text": "Is high blood pressure hereditary?", "requires_records": False},
    {"id": 137, "category": "Lifestyle & Family History", "question_text": "What is the genetic risk of developing Alzheimer's disease?", "requires_records": False},
    {"id": 138, "category": "Lifestyle & Family History", "question_text": "Do my records state whether I live alone or with family?", "requires_records": True},
    {"id": 139, "category": "Lifestyle & Family History", "question_text": "How does social isolation affect mental and physical health in older adults?", "requires_records": False},
    {"id": 140, "category": "Lifestyle & Family History", "question_text": "Is there any history of genetic blood disorders in my family records?", "requires_records": True},
    {"id": 141, "category": "Lifestyle & Family History", "question_text": "How do I share health data securely with my family members?", "requires_records": False},
    {"id": 142, "category": "Lifestyle & Family History", "question_text": "What is considered moderate alcohol consumption for men vs women?", "requires_records": False},

    # Category 6: Diagnostic Tests & Lab Results (Q143 - Q171)
    {"id": 143, "category": "Diagnostic Tests & Lab Results", "question_text": "What are my most recent vital signs, like blood pressure and heart rate?", "requires_records": True},
    {"id": 144, "category": "Diagnostic Tests & Lab Results", "question_text": "When was my last blood test, and what did it screen for?", "requires_records": True},
    {"id": 145, "category": "Diagnostic Tests & Lab Results", "question_text": "What do my cholesterol test results mean (HDL vs LDL vs triglycerides)?", "requires_records": True},
    {"id": 146, "category": "Diagnostic Tests & Lab Results", "question_text": "Are my blood glucose levels or HbA1c results in the system?", "requires_records": True},
    {"id": 147, "category": "Diagnostic Tests & Lab Results", "question_text": "What does a thyroid panel test (TSH, Free T4) measure?", "requires_records": False},
    {"id": 148, "category": "Diagnostic Tests & Lab Results", "question_text": "Do my records include any recent imaging reports, like X-rays or MRIs?", "requires_records": True},
    {"id": 149, "category": "Diagnostic Tests & Lab Results", "question_text": "What is a complete blood count (CBC) and what does a high white blood cell count mean?", "requires_records": False},
    {"id": 150, "category": "Diagnostic Tests & Lab Results", "question_text": "Do my records indicate any abnormalities in my urine analysis?", "requires_records": True},
    {"id": 151, "category": "Diagnostic Tests & Lab Results", "question_text": "What do the abbreviations BMP and CMP mean on lab results?", "requires_records": False},
    {"id": 152, "category": "Diagnostic Tests & Lab Results", "question_text": "Are there any pending diagnostic test results that have not been uploaded?", "requires_records": True},
    {"id": 153, "category": "Diagnostic Tests & Lab Results", "question_text": "What does a high serum creatinine level suggest about kidney health?", "requires_records": False},
    {"id": 154, "category": "Diagnostic Tests & Lab Results", "question_text": "Do my records contain any liver function test (LFT) values?", "requires_records": True},
    {"id": 155, "category": "Diagnostic Tests & Lab Results", "question_text": "What is an EKG (electrocardiogram) and why is it performed?", "requires_records": False},
    {"id": 156, "category": "Diagnostic Tests & Lab Results", "question_text": "Are my vitamin D levels noted in my recent blood panels?", "requires_records": True},
    {"id": 157, "category": "Diagnostic Tests & Lab Results", "question_text": "What is the normal range for fasting blood glucose?", "requires_records": False},
    {"id": 158, "category": "Diagnostic Tests & Lab Results", "question_text": "Do my records contain diagnostic findings from an ultrasound scan?", "requires_records": True},
    {"id": 159, "category": "Diagnostic Tests & Lab Results", "question_text": "What does electrolyte balance (sodium, potassium) mean for health?", "requires_records": False},
    {"id": 160, "category": "Diagnostic Tests & Lab Results", "question_text": "Do my records include any bone density (DEXA) scan results?", "requires_records": True},
    {"id": 161, "category": "Diagnostic Tests & Lab Results", "question_text": "What is the clinical significance of a high C-reactive protein (CRP) level?", "requires_records": False},
    {"id": 162, "category": "Diagnostic Tests & Lab Results", "question_text": "Who should I contact to explain a lab result that is out of range?", "requires_records": False},
    {"id": 163, "category": "Diagnostic Tests & Lab Results", "question_text": "What does a blood urea nitrogen (BUN) test measure?", "requires_records": False},
    {"id": 164, "category": "Diagnostic Tests & Lab Results", "question_text": "Do my records have a pulse oximetry reading?", "requires_records": True},
    {"id": 165, "category": "Diagnostic Tests & Lab Results", "question_text": "What does a high platelet count indicate in blood tests?", "requires_records": False},
    {"id": 166, "category": "Diagnostic Tests & Lab Results", "question_text": "Do my records include a cardiac stress test report?", "requires_records": True},
    {"id": 167, "category": "Diagnostic Tests & Lab Results", "question_text": "What is the normal range for heart rate at rest?", "requires_records": False},
    {"id": 168, "category": "Diagnostic Tests & Lab Results", "question_text": "Are my blood test results categorized by date?", "requires_records": True},
    {"id": 169, "category": "Diagnostic Tests & Lab Results", "question_text": "What is a hemoglobin A1c test and how often is it done?", "requires_records": False},
    {"id": 170, "category": "Diagnostic Tests & Lab Results", "question_text": "Do my records contain any calcium blood level measurements?", "requires_records": True},
    {"id": 171, "category": "Diagnostic Tests & Lab Results", "question_text": "What is the significance of a high red blood cell count?", "requires_records": False},

    # Category 7: Access Security & AI Guidance (Q172 - Q200)
    {"id": 172, "category": "Access Security & AI Guidance", "question_text": "Which doctors have active access grants to view my medical records?", "requires_records": True},
    {"id": 173, "category": "Access Security & AI Guidance", "question_text": "Do I have any pending record access requests from clinicians?", "requires_records": True},
    {"id": 174, "category": "Access Security & AI Guidance", "question_text": "How do I approve or decline a pending access request?", "requires_records": False},
    {"id": 175, "category": "Access Security & AI Guidance", "question_text": "How can I revoke a doctor's access to my records?", "requires_records": False},
    {"id": 176, "category": "Access Security & AI Guidance", "question_text": "Are my records stored securely on the blockchain, and what does that mean?", "requires_records": False},
    {"id": 177, "category": "Access Security & AI Guidance", "question_text": "Can I see an audit log of who has viewed my medical files?", "requires_records": True},
    {"id": 178, "category": "Access Security & AI Guidance", "question_text": "How does MedChain protect my health privacy?", "requires_records": False},
    {"id": 179, "category": "Access Security & AI Guidance", "question_text": "Do I need to sign a consent form for every specialist I visit?", "requires_records": False},
    {"id": 180, "category": "Access Security & AI Guidance", "question_text": "Can I share specific records while keeping others private?", "requires_records": False},
    {"id": 181, "category": "Access Security & AI Guidance", "question_text": "What is the purpose of cryptographic signing in record sharing?", "requires_records": False},
    {"id": 182, "category": "Access Security & AI Guidance", "question_text": "What answer format does the patient prefer: short summary, detailed explanation, checklist, timeline, or doctor-prep note?", "requires_records": False},
    {"id": 183, "category": "Access Security & AI Guidance", "question_text": "Should the answer include citations or references to specific uploaded records?", "requires_records": False},
    {"id": 184, "category": "Access Security & AI Guidance", "question_text": "Which retrieved records support the answer?", "requires_records": True},
    {"id": 185, "category": "Access Security & AI Guidance", "question_text": "Which parts of the answer are uncertain because data is missing or conflicting?", "requires_records": True},
    {"id": 186, "category": "Access Security & AI Guidance", "question_text": "What medical terms in the retrieved records need plain-language explanation?", "requires_records": True},
    {"id": 187, "category": "Access Security & AI Guidance", "question_text": "What does the patient need to do next based on doctor instructions already present in the records?", "requires_records": True},
    {"id": 188, "category": "Access Security & AI Guidance", "question_text": "What symptoms would require urgent or emergency care for this patient's situation?", "requires_records": True},
    {"id": 189, "category": "Access Security & AI Guidance", "question_text": "What non-urgent self-care steps are already recommended in the patient's records?", "requires_records": True},
    {"id": 190, "category": "Access Security & AI Guidance", "question_text": "What questions should the patient ask their doctor at the next visit?", "requires_records": True},
    {"id": 191, "category": "Access Security & AI Guidance", "question_text": "What information should the patient bring or upload before the next visit?", "requires_records": True},
    {"id": 192, "category": "Access Security & AI Guidance", "question_text": "What medication, diagnosis, or lab result should be explained first for the patient?", "requires_records": True},
    {"id": 193, "category": "Access Security & AI Guidance", "question_text": "What timeline of events should be generated from the patient's records?", "requires_records": True},
    {"id": 194, "category": "Access Security & AI Guidance", "question_text": "What changed since the patient's last appointment or record upload?", "requires_records": True},
    {"id": 195, "category": "Access Security & AI Guidance", "question_text": "What should be included in a patient-friendly clinical summary?", "requires_records": True},
    {"id": 196, "category": "Access Security & AI Guidance", "question_text": "What should be included in a doctor-facing summary of the patient's concern?", "requires_records": True},
    {"id": 197, "category": "Access Security & AI Guidance", "question_text": "What privacy or sharing warning should be shown before generating or sharing an answer?", "requires_records": True},
    {"id": 198, "category": "Access Security & AI Guidance", "question_text": "Does the answer avoid giving a definitive diagnosis when the records are incomplete?", "requires_records": True},
    {"id": 199, "category": "Access Security & AI Guidance", "question_text": "Does the answer clearly tell the patient when to contact a clinician or emergency service?", "requires_records": True},
    {"id": 200, "category": "Access Security & AI Guidance", "question_text": "What follow-up question should the system ask the patient to make the answer safer and more accurate?", "requires_records": True}
]

def get_questions_by_category() -> Dict[str, List[Dict[str, Any]]]:
    """Organizes all questions in the bank by their categories."""
    categories: Dict[str, List[Dict[str, Any]]] = {}
    for q in QUESTIONS:
        cat = q["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(q)
    return categories

def get_suggested_followups(question_id: int) -> List[str]:
    """
    Given a question ID, return 2 to 3 related follow-up question texts.
    Falls back to next sequential questions if no specific mapping is defined.
    """
    # Specific interesting clinical guided flows
    flow_map = {
        1: [5, 6, 8],      # Profile -> doctor, specialists, emergency contact
        5: [6, 7, 13],     # Doctor -> specialists, clinic name, authorized users
        8: [15, 27, 2],    # Emergency contact -> secondary emergency, emergency checklist, reason
        29: [30, 33, 36],  # Symptoms -> start date, severity, triggers
        30: [31, 32, 37],  # Start date -> sudden/gradual, trajectory, history
        33: [34, 38, 47],  # Severity -> location, accompanying, emergency shortness of breath
        57: [58, 59, 66],  # Chronic conditions -> diagnosis dates, cholesterol, blood monitoring
        86: [87, 88, 90],  # Medications -> instructions, refills, interactions
        105: [106, 108, 114], # Drug allergies -> side effects vs allergy, food allergy, epipen
        115: [116, 117, 136], # Heart disease family -> diabetes family, cancer risk, hypertension hered
        125: [126, 127, 130], # Lifestyle -> exercise, vaccine status, sleep habits
        143: [144, 145, 146], # Vitals -> blood test, cholesterol, glucose
        172: [173, 175, 177], # Access grants -> pending requests, revoke access, audit logs
        182: [183, 184, 195], # Format preference -> citations, supporting records, summary format
    }

    q_ids = flow_map.get(question_id)
    if not q_ids:
        # Fallback: Suggest the next 3 questions in the same category
        target_q = next((q for q in QUESTIONS if q["id"] == question_id), None)
        if target_q:
            cat = target_q["category"]
            cat_qs = [q for q in QUESTIONS if q["category"] == cat]
            idx = cat_qs.index(target_q)
            suggested_qs = []
            for i in range(1, 4):
                next_idx = (idx + i) % len(cat_qs)
                suggested_qs.append(cat_qs[next_idx])
            q_ids = [q["id"] for q in suggested_qs]
        else:
            q_ids = [1, 5, 57]

    texts = []
    for q_id in q_ids:
        q_item = next((q for q in QUESTIONS if q["id"] == q_id), None)
        if q_item:
            texts.append(q_item["question_text"])
    return texts
