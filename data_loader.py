"""
data_loader.py - Educational Data Loader for Edugator
Loads documents from text/PDF files and provides a comprehensive
fallback knowledge base about Indian education.
"""

import os
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
    PyPDFLoader
)


class EduDataLoader:
    """Loads educational content from files and built-in knowledge base."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

    def load_all(self) -> list:
        """Load documents from all supported formats in the data directory."""
        docs = []

        if not os.path.exists(self.data_dir):
            print(f"📁 Data directory '{self.data_dir}' not found. Using fallback.")
            return docs

        # Load .txt files
        txt_files = list(Path(self.data_dir).glob("**/*.txt"))
        for f in txt_files:
            try:
                loader = TextLoader(str(f), encoding="utf-8")
                loaded = loader.load()
                for doc in loaded:
                    doc.metadata["source"] = f.stem.replace("_", " ").title()
                docs.extend(loaded)
                print(f"  ✅ Loaded: {f.name}")
            except Exception as e:
                print(f"  ⚠️ Could not load {f.name}: {e}")

        # Load .pdf files
        pdf_files = list(Path(self.data_dir).glob("**/*.pdf"))
        for f in pdf_files:
            try:
                loader = PyPDFLoader(str(f))
                loaded = loader.load()
                for doc in loaded:
                    doc.metadata["source"] = f.stem.replace("_", " ").title()
                docs.extend(loaded)
                print(f"  ✅ Loaded PDF: {f.name}")
            except Exception as e:
                print(f"  ⚠️ Could not load PDF {f.name}: {e}")

        print(f"📚 Total documents loaded from files: {len(docs)}")
        return docs

    def get_fallback_docs(self) -> list:
        """
        Built-in comprehensive knowledge base for Indian education.
        Used when no external data files are found.
        """
        content_blocks = [

            # ─── AFTER 10TH GRADE ───────────────────────────────────────────
            ("After 10th Grade - Stream Selection", """
CHOOSING YOUR STREAM AFTER 10TH GRADE IN INDIA

After completing 10th grade (SSC/CBSE/ICSE/State Board), students must choose a stream for
classes 11 and 12. This is one of the most important decisions of your academic life.

SCIENCE STREAM
Subjects: Physics, Chemistry, Mathematics (PCM) or Biology (PCB) or both (PCMB)
Best for: Students who love logic, problem-solving, experiments
Career paths: Engineering, Medicine, Research, IT, Pharmacy, Architecture
Key entrance exams: JEE Main, JEE Advanced (for engineering), NEET-UG (for medicine)
Required marks: Usually 60-70%+ in 10th science and math recommended

COMMERCE STREAM
Subjects: Accountancy, Business Studies, Economics, Mathematics (optional)
Best for: Students interested in business, finance, banking, trade
Career paths: CA, CS, MBA, Banking, Finance, Stock Market, Entrepreneurship
Key exams: CA Foundation, CS Foundation, CLAT (for commerce + law)
Required marks: 55%+ recommended

ARTS / HUMANITIES STREAM
Subjects: History, Geography, Political Science, Economics, Sociology, Psychology
Best for: Creative, analytical students who love reading and social sciences
Career paths: Civil Services (IAS/IPS), Law, Journalism, Teaching, Design, Literature
Key exams: UPSC, CLAT, NID, NLU entrance exams
Required marks: Open to most students

DIPLOMA / POLYTECHNIC (After 10th)
Duration: 3 years
Institutions: Government Polytechnic Colleges (admission via TNEA/State polytechnic counselling)
Popular trades: Mechanical Engineering, Civil Engineering, Electrical Engineering,
                Computer Science, Electronics, Automobile Engineering
Advantage: Direct lateral entry to 2nd year of BE/BTech after diploma (via TANCET/LEET)
Best for: Students who want job-ready technical skills faster
Admission: Based on 10th marks - no entrance exam required in most states

ITI COURSES (Industrial Training Institute)
Duration: 1-2 years
Trades: Electrician, Fitter, Turner, Welder, COPA (Computer), Plumber
Advantage: Government jobs eligibility, quick employment
Admission: Via 8th/10th marks

SKILL-BASED COURSES AFTER 10TH
- Certificate in Computer Applications (CCA)
- Tally ERP / Accounting courses
- Digital Marketing certificate
- Web Design basics
- Spoken English / Communication courses
- Graphic Design (Photoshop, CorelDRAW)
These can be done alongside regular schooling or polytechnic.
"""),

            # ─── AFTER 12TH GRADE ───────────────────────────────────────────
            ("After 12th Grade - Engineering Path", """
ENGINEERING COURSES AFTER 12TH (PCM)

B.E. / B.TECH (Bachelor of Engineering / Technology)
Duration: 4 years
Eligibility: 12th with PCM (Physics, Chemistry, Math), minimum 60%
Top entrance exams:
- JEE Main: National level, for NITs, IIITs, Government colleges
- JEE Advanced: For IITs (top 2.5 lakh from JEE Main qualify)
- TNEA: Tamil Nadu Engineering Admissions (for TN state colleges, based on 12th marks - NO entrance exam!)
- COMEDK: For Karnataka private colleges
- MHT-CET: Maharashtra engineering colleges
- AP/TS EAMCET: Andhra Pradesh and Telangana

Popular B.Tech branches:
1. Computer Science Engineering (CSE) - Highest demand, best placements
2. Electrical and Electronics Engineering (EEE)
3. Electronics and Communication (ECE)
4. Mechanical Engineering
5. Civil Engineering
6. Information Technology (IT)
7. AI & Machine Learning (new branch, very popular)
8. Data Science Engineering

Top engineering colleges in India:
- IIT Bombay, IIT Delhi, IIT Madras, IIT Kanpur (JEE Advanced)
- NIT Trichy, NIT Warangal, NIT Surathkal (JEE Main)
- Anna University (TNEA), VIT Vellore, SRM, PSG, SSN (Tamil Nadu)
- BITS Pilani (BITSAT entrance exam)

After B.Tech options:
- Campus placements (top companies visit IITs/NITs)
- M.Tech (GATE exam required)
- MBA (CAT exam)
- UPSC Civil Services
- MS abroad (GRE required)
- Startups / Entrepreneurship
"""),

            ("After 12th Grade - Medical Path", """
MEDICAL AND HEALTH SCIENCES AFTER 12TH (PCB)

MBBS (Bachelor of Medicine, Bachelor of Surgery)
Duration: 5.5 years (including 1 year internship)
Eligibility: 12th PCB (Physics, Chemistry, Biology), minimum 50-60%
Entrance exam: NEET-UG (National Eligibility cum Entrance Test) - MANDATORY for all medical colleges in India
NEET Details:
- Conducted by NTA (National Testing Agency)
- 180 questions: Biology (90), Physics (45), Chemistry (45)
- Marks: 720 total
- Syllabus: NCERT 11th and 12th
- Seat types: Government (cheap: ₹10,000-50,000/year), Private (expensive: ₹5-25 lakh/year)

Other medical courses:
- BDS (Dentistry): 5 years, via NEET
- BAMS (Ayurveda): 5.5 years, via NEET
- BHMS (Homeopathy): 5.5 years, via NEET
- B.Pharm (Pharmacy): 4 years
- B.Sc Nursing: 4 years
- BMLT (Medical Lab Tech): 3 years
- BASLP (Audiology, Speech): 4 years
- B.Sc Radiology, Physiotherapy, OT Technology

After MBBS options:
- MD/MS (Postgraduate medical degree via NEET-PG)
- Government hospital jobs (through UPSC/State PSC)
- Private practice
- Research (ICMR)
- Abroad (USMLE for USA, PLAB for UK)
"""),

            ("After 12th Grade - Arts Science Commerce", """
ARTS & SCIENCE DEGREES AND COMMERCE AFTER 12TH

B.Sc (Bachelor of Science)
Duration: 3 years
Popular branches: Computer Science, Maths, Physics, Chemistry, Biology, Nursing, Nutrition
Top options in Tamil Nadu: Madras University, Bharathiar, Bharathidasan, PSG, Stella Maris
Admission: Direct (some colleges have cutoffs), some via TNEA-type counselling

B.Com (Bachelor of Commerce)
Duration: 3 years
Best for: Accounting, finance, banking careers
After B.Com: CA (Chartered Accountant), CS (Company Secretary), MBA Finance, Banking jobs

BA (Bachelor of Arts)
Duration: 3 years
Popular: History, Economics, English Literature, Sociology, Political Science, Psychology
After BA: MA, UPSC Civil Services (most IAS toppers are Arts graduates!), Journalism, Law (LLB)

BBA (Bachelor of Business Administration)
Duration: 3 years
Best for: Students wanting MBA later, business careers
Exam: Some colleges via SET, management entrance exams

BCA (Bachelor of Computer Applications)
Duration: 3 years
Best for: IT career without doing engineering
After BCA: MCA (Master of Computer Applications), direct IT jobs
Easier to get into than B.Tech but similar job opportunities

Law (LLB / BA LLB / BBA LLB)
Integrated: 5 years (after 12th)
Entrance: CLAT (for NLUs), LSAT, state law college exams
Career: Lawyer, Judge (after JMFC exam), Legal advisor, Civil Services

B.Ed (Bachelor of Education) - After graduation
Duration: 2 years
Required for: Teaching in government schools
Entrance: State B.Ed entrance exams (Tamil Nadu: TNTEU counselling)
"""),

            # ─── ENTRANCE EXAMS ─────────────────────────────────────────────
            ("Major Entrance Exams in India", """
IMPORTANT ENTRANCE EXAMS FOR INDIAN STUDENTS

JEE MAIN (Joint Entrance Examination - Main)
Conducting body: NTA (National Testing Agency)
Purpose: Admission to NITs, IIITs, GFTIs and other central institutions
Eligibility: 12th with PCM, minimum 75% (or top 20 percentile in board)
Pattern: 90 questions (Math 30, Physics 30, Chemistry 30), 3 hours
Attempts: 2 per year (January and April sessions)
Score range: -360 to +300
Cut-off for NITs: Generally 90+ percentile for top NITs
Website: jeemain.nta.nic.in

JEE ADVANCED (Joint Entrance Examination - Advanced)
Purpose: Admission to IITs only
Eligibility: Top 2.5 lakh JEE Main qualifiers, 75% in 12th
Pattern: 2 papers, 3 hours each, harder than JEE Main
Important: Only 2 attempts in lifetime allowed

NEET-UG (National Eligibility cum Entrance Test - Undergraduate)
Conducting body: NTA
Purpose: MBBS, BDS, BAMS, BHMS admissions across India
Eligibility: 12th with PCB, minimum 50% (45% for OBC, 40% for SC/ST)
Pattern: 200 questions (160 to attempt), Biology 100, Physics 50, Chemistry 50
Marks: 720 total
Date: Usually May every year
Attempts: Unlimited (no cap currently)
Website: neet.nta.nic.in

TNEA (Tamil Nadu Engineering Admissions)
Purpose: Engineering admissions in Tamil Nadu government and aided colleges
Special feature: NO ENTRANCE EXAM - purely based on 12th marks
Weightage: Math (1.5x), Physics (1x), Chemistry (1x)
Counselling: Online via tneaonline.org
Total seats: ~1.5 lakh seats in TN engineering colleges
Note: For private unaided colleges in TN, institutions conduct their own counselling

TNPSC (Tamil Nadu Public Service Commission)
Purpose: Recruitment to Tamil Nadu state government jobs
Group exams: Group 1, Group 2, Group 2A, Group 4, Group 8
Group 4: 10th pass, Clerical jobs (most popular for fresh graduates)
Group 2/2A: Graduation required, higher posts
Group 1: Graduation required, IAS-equivalent state civil services
Exam pattern: Objective type (Tamil + General Studies + Aptitude)
Website: tnpsc.gov.in

UPSC (Union Public Service Commission)
Purpose: IAS, IPS, IFS and other central government services
Eligibility: Any graduation (any stream!)
3 stages: Prelims (objective) → Mains (written) → Interview (personality test)
Preparation time: Usually 1-3 years of dedicated study
Toughest exam in India but most prestigious job
Website: upsc.gov.in

SSC (Staff Selection Commission)
Purpose: Central government jobs (clerk, constable, translator, etc.)
Popular exams: SSC CGL (graduate level), SSC CHSL (12th level), SSC CPO (police)
SSC CGL: For posts like Income Tax Inspector, CBI, Auditor
Eligibility: Graduation (for CGL), 12th (for CHSL)
Website: ssc.nic.in

BANKING EXAMS
IBPS PO (Probationary Officer) - Nationalized banks
IBPS Clerk - Nationalized banks (easier than PO)
SBI PO - State Bank of India (prestigious)
SBI Clerk - SBI clerical posts
RBI Grade B - Reserve Bank of India (very prestigious, high salary)
IBPS RRB - Regional Rural Banks
Eligibility: Graduation in any stream, age 20-30 years

CAT (Common Admission Test)
Purpose: MBA admissions in IIMs and other top B-schools
Conducted by: IIM (rotates each year)
Score used by: IIM Ahmedabad, Bangalore, Calcutta, Kozhikode, all IIMs + 100s of colleges
Pattern: VARC, DILR, Quant sections

GATE (Graduate Aptitude Test in Engineering)
Purpose: M.Tech admissions + PSU recruitment
Who should take: Engineering/Science graduates wanting higher studies
PSUs that recruit via GATE: BHEL, IOCL, NTPC, GAIL, ONGC, BSNL
Score validity: 3 years
"""),

            # ─── CAREER GUIDANCE ────────────────────────────────────────────
            ("IT Career Guidance India", """
IT / SOFTWARE CAREER GUIDANCE FOR INDIAN STUDENTS

The IT sector is the largest employer of engineers in India.

TOP IT COMPANIES IN INDIA (Tier 1 - Mass recruiters):
- TCS (Tata Consultancy Services) - Largest IT employer
- Infosys - Trains freshers well
- Wipro, HCL Technologies, Tech Mahindra
- Cognizant (CTSH)
Package for freshers (2024-25): ₹3.5 - 7 LPA (Lakhs Per Annum)

PRODUCT COMPANIES (Higher salary, harder to get):
- Google, Microsoft, Amazon, Meta, Apple (FAANG)
- Zoho, Freshworks (Indian product companies)
- Swiggy, Zomato, Flipkart, Paytm (Indian unicorns)
Package range: ₹10 - 50+ LPA for freshers

SKILLS REQUIRED FOR IT JOBS:
Core Programming:
- Python: Most versatile, used in AI/ML, web, automation
- Java: Enterprise software, Android
- JavaScript: Web development (frontend + backend with Node.js)
- C++: Competitive programming, system software

For Web Development:
- Frontend: HTML, CSS, JavaScript, React.js or Vue.js
- Backend: Node.js (JavaScript), Django/Flask (Python), Spring Boot (Java)
- Database: MySQL, PostgreSQL, MongoDB
- Version control: Git and GitHub (must know!)

For Data Science / AI / ML:
- Python (NumPy, Pandas, Scikit-learn, TensorFlow, PyTorch)
- Statistics and Mathematics
- Machine Learning concepts
- SQL for data analysis

For Cloud Computing:
- AWS (Amazon Web Services) - Most in demand
- Azure (Microsoft) - Second most popular
- Google Cloud Platform (GCP)
- Certifications: AWS Cloud Practitioner (beginner), Solutions Architect (advanced)

PLACEMENT PREPARATION ROADMAP:
Year 1-2: Learn Data Structures and Algorithms (DSA)
Year 2-3: Build projects, learn a framework
Year 3-4: Internships (6 months), competitive coding
Year 4: Campus placements, off-campus applications

Coding practice platforms:
- LeetCode (most used for FAANG preparation)
- HackerRank (AMCAT, campus placements)
- GeeksforGeeks (theory + problems)
- CodeChef, Codeforces (competitive programming)

Certifications that help:
- NPTEL (free, IIT courses, certificates recognized in India)
- Coursera (Google, IBM, Meta certifications)
- AWS/Azure/GCP cloud certifications
- Oracle Java certification
"""),

            ("Government Jobs Career Guidance India", """
GOVERNMENT JOB CAREER PATHS IN INDIA

India has one of the largest government sectors in the world.

CENTRAL GOVERNMENT JOBS:
1. IAS (Indian Administrative Service) via UPSC Civil Services
   - Most prestigious, salary: ₹56,100+ basic + allowances
   - Controls districts, runs government departments
   
2. IPS (Indian Police Service) via UPSC
   - SP, DIG, IG of police departments
   
3. IFS (Indian Foreign Service) via UPSC
   - Diplomat, posted in Indian embassies abroad
   
4. Income Tax / Customs Officer via SSC CGL
   - Package: ₹6-8 LPA for freshers
   
5. CBI Officer via SSC CGL
   - Investigates major crimes across India
   
6. Army / Navy / Air Force (Defence Jobs)
   - After 12th: NDA (National Defence Academy) exam
   - After graduation: CDS (Combined Defence Services) exam
   - Direct entry: SSB interview for officers
   
7. RBI Grade B Officer
   - One of the highest paid government jobs
   - Salary: ₹35,000-50,000/month + perks
   - Exam: Phase 1 (objective) + Phase 2 (written) + Interview

STATE GOVERNMENT JOBS (Tamil Nadu example - TNPSC):
- Group 1: Collector-level positions (very competitive)
- Group 2: Deputy Tahsildar, Commercial Tax Inspector
- Group 2A: Junior Cooperative Auditor, Assistant Inspector
- Group 4: VAO (Village Administrative Officer), Typist
- Group 8: Jr. Cooperative Auditor
- Teachers via TET (Teacher Eligibility Test) + TRB (Teacher Recruitment Board)

TEACHING CAREER IN GOVERNMENT SCHOOLS:
Tamil Nadu:
- Primary Teacher: Passed TET (Teacher Eligibility Test) + B.Ed or D.El.Ed
- High School Teacher: Subject graduation + B.Ed + TET
- PG Teacher: Post graduation + B.Ed + TET
- College Lecturer: Post graduation + NET/SET exam

National Level:
- CTET (Central Teacher Eligibility Test) for KVS, NVS schools
- KVS TGT/PGT: Kendriya Vidyalaya teacher
- NVS: Navodaya Vidyalaya teacher
- UGC NET: For college/university lecturers

Benefits of government jobs:
- Job security (no layoffs)
- Pension scheme (NPS for new recruits)
- Medical facilities (CGHS)
- Housing allowance (HRA)
- Easy work-life balance
- Respect in society

BANKING JOBS IN DETAIL:
Clerical Level:
- Bank clerk (IBPS Clerk / SBI Clerk)
- Salary: ₹25,000-35,000/month
- Work: Customer service, cash handling, data entry

Officer Level:
- Probationary Officer (IBPS PO / SBI PO)
- Starting salary: ₹40,000-55,000/month
- Growth: PO → Manager → AGM → GM → ED → MD

Specialist Officers:
- IT Officer, Law Officer, HR Officer
- Direct recruitment for specialized roles
- Higher salary than regular PO
"""),

            # ─── HIGHER STUDIES ─────────────────────────────────────────────
            ("Higher Studies and Postgraduate Options", """
HIGHER STUDIES OPTIONS FOR INDIAN GRADUATES

AFTER B.TECH/B.E.:

M.Tech (Master of Technology)
- Entrance: GATE exam
- Duration: 2 years
- Benefits: Stipend (₹12,400/month for GATE-qualified students at NITs/IITs!)
- Best for: Research-oriented students, want to become faculty
- IIT M.Tech: Top tier, great placement, research opportunities
- PSU recruitment via GATE: BHEL, IOCL, NTPC, ONGC

MBA (Master of Business Administration)
- Entrance: CAT (for IIMs), XAT (for XLRI), GMAT (international)
- Duration: 2 years
- Top colleges: IIM Ahmedabad, Bangalore, Calcutta, Kozhikode
- Average placement: ₹15-30 LPA at top IIMs
- Salary after IIM A: ₹25-35 LPA average
- Good for: Management roles, consulting, finance, entrepreneurship

MS Abroad (Master of Science)
- Countries: USA, Canada, Germany, UK, Australia
- Entrance: GRE (for USA/Canada), IELTS/TOEFL (English)
- Germany: Many public universities are FREE (no tuition fee!)
- USA: Top universities - MIT, Stanford, Carnegie Mellon, Georgia Tech
- Canada: PR pathway available after graduation (popular option)
- Cost: USA - $40,000-60,000/year; Germany - €500-1000/semester

PhD in India
- At IITs, IISc, NITs, Central Universities
- Fully funded (₹31,000-35,000/month JRF fellowship)
- Duration: 4-6 years
- Entry: GATE/NET/JEST/JAM scores + interview
- IISc Bangalore: Top research institute in India

AFTER GRADUATION (any stream):
- MBA via CAT/XAT
- UPSC Civil Services (IAS/IPS/IFS)
- LLB/LLM (Law)
- MA/M.Com/M.Sc (higher studies in same domain)
- MCA (for B.Sc Computer Science graduates)
- Distance education: IGNOU (Indira Gandhi National Open University)

ABROAD STUDY TIPS:
1. GRE score: 310+ for decent universities in USA
2. IELTS: 6.5+ band for most universities
3. Apply to 8-12 universities (safety/moderate/reach)
4. Scholarship: Look for TA (Teaching Assistant) and RA (Research Assistant) positions
5. Loan: Education loan available from SBI, Canara Bank, HDFC Credila
"""),

            # ─── SKILL DEVELOPMENT ──────────────────────────────────────────
            ("Skill Development and Freelancing India", """
SKILL DEVELOPMENT AND FREELANCING FOR INDIAN STUDENTS

FREE LEARNING PLATFORMS:
- NPTEL (nptel.ac.in): IIT/IISc courses with certification - FREE
- Swayam (swayam.gov.in): Government platform, 1000s of courses
- YouTube: Programming tutorials (Apna College, Code With Harry, Traversy Media)
- GeeksforGeeks: DSA, CS fundamentals
- Khan Academy: Maths, Science basics (free)
- Coursera/edX: Audit courses free, pay for certificate
- Google Digital Garage: Digital marketing (free certificate)
- AWS Training: Cloud basics for free
- Microsoft Learn: Azure, AI, Microsoft tools (free)

PAID BUT WORTH IT:
- Udemy courses (buy during sale at ₹399 per course)
- Coding Ninjas, Scaler, PW Skills: DSA + placement programs
- NIIT, APTECH: Traditional IT courses

FREELANCING CAREER PATH:
Platforms to start:
- Fiverr: Best for beginners, small gigs
- Upwork: Higher-paying, for experienced freelancers
- Freelancer.com: Multiple project types
- Toptal: Premium (top 3% of freelancers, vetted)
- LinkedIn: Professional networking + freelance work

Freelancable skills in demand (2024-25):
1. Web Development (React, WordPress, Shopify)
2. Mobile App Development (Flutter, React Native)
3. Graphic Design (Canva, Illustrator, Photoshop)
4. Video Editing (Premiere Pro, DaVinci Resolve, CapCut)
5. Content Writing & SEO
6. Data Analysis (Excel, Python, Tableau, Power BI)
7. Digital Marketing (Facebook Ads, Google Ads, SEO)
8. UI/UX Design (Figma)
9. AI/ML consulting (ChatGPT integration, automation)
10. Cybersecurity (bug bounty programs)

HOW TO START FREELANCING AS A STUDENT:
Step 1: Pick ONE skill and master it (3-6 months)
Step 2: Build 2-3 portfolio projects (real or mock)
Step 3: Create profiles on Fiverr/Upwork with portfolio
Step 4: Start with low rates to get first 5-10 reviews
Step 5: Gradually raise rates as you get experience
Step 6: Network on LinkedIn, Twitter (X) to get direct clients

STARTUP / ENTREPRENEURSHIP:
- Startup India: Government scheme with tax benefits, funding
- IIT/NIT incubators: Free workspace, mentorship for student startups
- Atal Innovation Mission: Govt. support for innovation
- TiE (The Indus Entrepreneurs): Networking, mentoring
- Seed funding: SIDBI, NABARD, Angel investors
- Apps for startups: Registered as Pvt Ltd company, get 80-IAC tax exemption

YOUTUBE / CONTENT CREATION:
- Can earn ₹50,000-5,00,000/month with 1 lakh+ subscribers
- Education channels are very popular in India (Physics Wallah, etc.)
- Monetize through: YouTube ads, sponsorships, courses, affiliate marketing
"""),

            # ─── INTERVIEW & PLACEMENT PREP ─────────────────────────────────
            ("Placement Preparation and Resume Tips", """
PLACEMENT PREPARATION GUIDE FOR ENGINEERING STUDENTS

CAMPUS PLACEMENT PROCESS (Typical):
1. Pre-Placement Talk (PPT): Company presents about itself
2. Online Test: Aptitude + Coding + Technical MCQs
3. Group Discussion (GD): Not all companies, soft skill assessment
4. Technical Interview: DSA, OS, DBMS, CN, language-specific
5. HR Interview: Behavioral questions, salary negotiation

APTITUDE PREPARATION:
Topics:
- Quantitative: Percentages, Profit/Loss, Time-Speed, Averages, Ratios, Algebra
- Logical Reasoning: Seating arrangement, Blood relations, Coding-Decoding, Syllogisms
- Verbal: Reading comprehension, Vocabulary, Grammar
Resources:
- R.S. Aggarwal: Quantitative Aptitude (best book)
- IndiaBix.com: Free online practice
- PrepInsta: Company-specific aptitude papers
- YouTube: CareerRide, Freshersworld channels

TECHNICAL INTERVIEW TOPICS:
Data Structures: Arrays, Linked Lists, Trees, Graphs, Stacks, Queues, Heaps
Algorithms: Sorting, Searching, Dynamic Programming, Greedy
Database: SQL queries (JOINs, subqueries), Normalization, Indexing
Operating Systems: Process scheduling, Memory management, Deadlock
Computer Networks: TCP/IP, DNS, HTTP/HTTPS, OSI model
OOPs: Inheritance, Polymorphism, Encapsulation, Abstraction

Coding interview resources:
- LeetCode: Start with "Easy" problems, then "Medium"
- Striver's SDE Sheet: Most popular DSA sheet for placements
- Love Babbar's 450 DSA sheet
- NeetCode 150: Curated LeetCode problems

RESUME TIPS FOR FRESHERS:
1. Length: Maximum 1 page for freshers
2. Format: Clean, ATS-friendly (no fancy graphics for MNC applications)
3. Must-have sections:
   - Contact info (email, phone, LinkedIn, GitHub)
   - Education (10th, 12th, graduation with % and year)
   - Skills (Programming languages, tools, frameworks)
   - Projects (3-4 projects with GitHub links, tech used, impact)
   - Certifications (NPTEL, Coursera, cloud certs)
   - Achievements (Hackathons, competitions, open source)
4. Action words: "Developed", "Implemented", "Reduced", "Built", "Designed"
5. Quantify achievements: "Reduced page load time by 40%" beats "Improved performance"

SOFT SKILLS FOR INTERVIEWS:
- Communication: Practice talking about your projects clearly
- Problem-solving approach: Think out loud in coding interviews
- Confidence: Make eye contact (even in video calls), speak clearly
- Questions to ask interviewer: "What does the team structure look like?"
- Follow up: Send thank-you email within 24 hours

COMMON HR INTERVIEW QUESTIONS:
1. "Tell me about yourself" - 2-minute structured pitch
2. "Why do you want to join this company?" - Research the company!
3. "What are your strengths/weaknesses?" - Be honest, show self-awareness
4. "Where do you see yourself in 5 years?" - Show ambition + loyalty
5. "Why should we hire you?" - Highlight unique skills, enthusiasm
6. Salary question: Research market rate; say "₹X-Y based on role and growth"
"""),

            # ─── COUNSELLING GUIDE ──────────────────────────────────────────
            ("College Counselling Process India", """
COLLEGE COUNSELLING PROCESS IN INDIA

JEE MAIN COUNSELLING (JoSAA - Joint Seat Allocation Authority):
Step 1: Register on josaa.nic.in after results
Step 2: Fill choice of colleges + branches (can fill 500+ choices)
Step 3: Mock rounds released - check tentative allotment
Step 4: Seat allotment in 6 rounds
Step 5: Report to allotted college with original documents
Step 6: Pay fees online to accept seat

Documents needed for JoSAA:
- 10th, 12th mark sheets and certificates
- Category certificate (SC/ST/OBC-NCL) if applicable
- PwD certificate if applicable
- Passport size photos
- JEE Admit card and scorecard
- Aadhar card

NEET COUNSELLING (MCC - Medical Counselling Committee):
All India Quota (15%): MCC conducts online counselling
State Quota (85%): State medical counselling body
Example Tamil Nadu: Selection Committee Secretariat (TNSCS) in Chennai

TNEA COUNSELLING (Tamil Nadu Engineering):
Website: tneaonline.org
Steps:
1. Register and upload 12th mark sheet
2. Calculate TNEA score (Math x 1.5 + Physics + Chemistry)
3. Fill college and branch preferences (random number allotment system)
4. Document verification at facilitation center
5. Get college allotment
6. Report to college with original documents

Category reservations in TN:
- BC: 26.5%, MBC: 20%, SC: 18%, ST: 1%, BCM: 3.5%
- OC (Open Competition): 31%
- Management quota: 65% of seats in self-financing colleges

PREPARATION TIPS FOR COUNSELLING:
1. Keep all documents BEFORE counselling starts
2. Have scanned copies (PDF) of all documents
3. Research colleges thoroughly before filling preferences
4. Attend mock counselling rounds (no commitment, just practice)
5. Have backup choices (don't just pick top colleges)
6. Consider factors: Location, hostel, placements, faculty, infrastructure
7. Check NAAC grade, NBA accreditation, NIRF ranking of colleges

SCHOLARSHIP OPTIONS:
- NSP (National Scholarship Portal): scholarships.gov.in
- TN Government scholarships: BC, MBC, SC/ST students
- AICTE Pragati scholarship for women
- Prime Minister's Scholarship for central forces/RPF wards
- Minority scholarships
- Merit-cum-means scholarships
- Private scholarships: Tata Trust, Wipro Foundation, etc.
"""),
        ]

        # Convert to LangChain Document objects
        documents = []
        for title, content in content_blocks:
            doc = Document(
                page_content=content.strip(),
                metadata={"source": title, "type": "knowledge_base"}
            )
            documents.append(doc)

        print(f"📚 Fallback knowledge base: {len(documents)} topic documents loaded")
        return documents


def create_sample_data_files():
    """
    Creates sample .txt files in the data/ directory.
    Call this once to set up the data directory.
    Run: python -c "from data_loader import create_sample_data_files; create_sample_data_files()"
    """
    os.makedirs("data", exist_ok=True)

    sample = """AFTER 10TH GRADE GUIDE - INDIA

Science Stream:
Choose PCM (Physics, Chemistry, Maths) if you want engineering.
Choose PCB (Physics, Chemistry, Biology) if you want medicine.
Engineering entrance: JEE Main, JEE Advanced
Medical entrance: NEET UG

Commerce Stream:
Best for CA (Chartered Accountant), banking, finance.
No entrance exam required for most colleges.
After B.Com, you can do CA Foundation, MBA, or banking exams.

Arts Stream:
Best for UPSC Civil Services, law, journalism, teaching.
Many great IAS officers come from Arts background.
After BA: MA, LLB, UPSC preparation.

Polytechnic / Diploma:
3 year course after 10th.
Direct employment OR lateral entry to 2nd year engineering.
Trades: Mechanical, Civil, CSE, ECE, Electrical, Automobile.
"""

    with open("data/after_10th_guide.txt", "w", encoding="utf-8") as f:
        f.write(sample)

    print("✅ Sample data file created in data/after_10th_guide.txt")
    print("Add more .txt or .pdf files in the data/ folder and rebuild vector store.")


if __name__ == "__main__":
    create_sample_data_files()
