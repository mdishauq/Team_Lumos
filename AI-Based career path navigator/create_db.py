import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("career_paths.db")
c = conn.cursor()

# ------------------ CREATE TABLES ------------------
c.execute('''
CREATE TABLE IF NOT EXISTS career_paths (
    career TEXT PRIMARY KEY,
    skills TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS career_roadmaps (
    career TEXT,
    step_order INTEGER,
    step TEXT,
    PRIMARY KEY (career, step_order)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS career_skill_importance (
    career TEXT,
    skill TEXT,
    importance INTEGER,
    PRIMARY KEY (career, skill)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS career_income (
    career TEXT PRIMARY KEY,
    fresher_income INTEGER,
    experienced_income INTEGER
)
''')


# ------------------ DATA ------------------

career_paths_data = [
    # Technology / Engineering
    ("Software Developer", "Python,Java,C++,Algorithms,Git"),
    ("Data Scientist", "Python,Statistics,Machine Learning,Pandas,SQL"),
    ("Embedded Systems Engineer", "C,C++,Microcontrollers,Electronics,Debugging"),
    ("Cybersecurity Analyst", "Networking,Linux,Cryptography,Firewalls,Security"),
    ("Web Developer", "HTML,CSS,JavaScript,React,Node.js"),
    ("Cloud Engineer", "AWS,Azure,DevOps,Python,Linux"),
    ("AI/ML Engineer", "Python,Machine Learning,TensorFlow,Pandas,Statistics"),
    ("Robotics Engineer", "C++,Python,ROS,Microcontrollers,Sensors,Robotics Algorithms"),
    ("IoT Developer", "Python,C,ESP32,Arduino,Sensors,MQTT,Electronics"),
    
    # Medical / Health
    ("Doctor", "Medical Knowledge,Diagnosis,Patient Care,Communication,Ethics"),
    ("Nurse", "Patient Care,Medical Knowledge,Communication,Time Management,Empathy"),
    ("Pharmacist", "Chemistry,Pharmacology,Attention to Detail,Regulations,Communication"),
    
    # Management / Business
    ("Business Analyst", "Data Analysis,SQL,Communication,Problem Solving,Excel"),
    ("Project Manager", "Leadership,Planning,Risk Management,Communication,Agile"),
    ("Entrepreneur", "Business Strategy,Marketing,Leadership,Finance,Networking"),
    
    # Arts / Humanities
    ("Graphic Designer", "Photoshop,Illustrator,Creativity,UI/UX,Typography"),
    ("Content Writer", "Writing,SEO,Creativity,Research,Editing"),
    ("Musician", "Instrument Skills,Music Theory,Creativity,Performance,Collaboration"),
    ("Actor", "Acting,Expression,Creativity,Communication,Networking"),
    
    # Science / Research
    ("Research Scientist", "Research,Experimentation,Analysis,Communication,Writing"),
    ("Chemist", "Chemistry,Lab Skills,Analysis,Experimentation,Reporting"),
    ("Physicist", "Physics,Mathematics,Research,Analysis,Problem Solving"),
    
    # Education
    ("Teacher", "Subject Knowledge,Communication,Patience,Lesson Planning,Creativity"),
    ("Professor", "Research,Teaching,Communication,Publication,Mentorship"),

    #R&D Engineer
    ("R&D Engineer", "Research,Core Engineering Fundamentals,CAD/CAE Software,Mathematics & Simulation,Problem Solving & Innovation"),

]

career_roadmaps_data = [
    # Software Developer
    ("Software Developer", 1, "Learn a programming language (Python, Java, C++)"),
    ("Software Developer", 2, "Learn data structures & algorithms"),
    ("Software Developer", 3, "Build small projects (To-Do app, Calculator, Games)"),
    ("Software Developer", 4, "Learn Git & GitHub for version control"),
    ("Software Developer", 5, "Contribute to open-source projects / internships"),

    # Data Scientist
    ("Data Scientist", 1, "Learn Python & libraries (Pandas, NumPy, Matplotlib)"),
    ("Data Scientist", 2, "Understand statistics & probability"),
    ("Data Scientist", 3, "Learn machine learning basics"),
    ("Data Scientist", 4, "Do small projects (Sales prediction, Sentiment analysis)"),
    ("Data Scientist", 5, "Build portfolio & participate in competitions"),

    # Embedded Systems Engineer
    ("Embedded Systems Engineer", 1, "Learn C/C++ and basic Python"),
    ("Embedded Systems Engineer", 2, "Understand microcontrollers (Arduino, STM32, ESP32)"),
    ("Embedded Systems Engineer", 3, "Work on IoT/hardware projects"),
    ("Embedded Systems Engineer", 4, "Learn debugging & testing embedded code"),
    ("Embedded Systems Engineer", 5, "Build portfolio projects (robots, drones)"),

    # Cybersecurity Analyst
    ("Cybersecurity Analyst", 1, "Learn networking and Linux basics"),
    ("Cybersecurity Analyst", 2, "Understand cryptography and firewalls"),
    ("Cybersecurity Analyst", 3, "Practice penetration testing"),
    ("Cybersecurity Analyst", 4, "Work on security projects / CTFs"),
    ("Cybersecurity Analyst", 5, "Get certifications (CEH, CompTIA Security+)"),

    # Web Developer
    ("Web Developer", 1, "Learn HTML, CSS, JavaScript"),
    ("Web Developer", 2, "Learn backend development (Node.js, Python)"),
    ("Web Developer", 3, "Learn frontend frameworks (React, Angular)"),
    ("Web Developer", 4, "Build small web projects"),
    ("Web Developer", 5, "Deploy projects and create portfolio"),

    # Cloud Engineer
    ("Cloud Engineer", 1, "Learn cloud platforms (AWS, Azure)"),
    ("Cloud Engineer", 2, "Understand DevOps basics and Linux"),
    ("Cloud Engineer", 3, "Learn Python for automation"),
    ("Cloud Engineer", 4, "Work on cloud deployment projects"),
    ("Cloud Engineer", 5, "Get cloud certifications (AWS, Azure)"),

    # AI/ML Engineer
    ("AI/ML Engineer", 1, "Learn Python & statistics"),
    ("AI/ML Engineer", 2, "Learn ML algorithms and libraries"),
    ("AI/ML Engineer", 3, "Work on small ML projects"),
    ("AI/ML Engineer", 4, "Learn deep learning frameworks (TensorFlow, PyTorch)"),
    ("AI/ML Engineer", 5, "Build portfolio & participate in competitions"),

    # Robotics Engineer
    ("Robotics Engineer", 1, "Learn C++ and Python basics"),
    ("Robotics Engineer", 2, "Learn ROS and microcontrollers"),
    ("Robotics Engineer", 3, "Work on sensors and actuators"),
    ("Robotics Engineer", 4, "Build robotics projects (drones, arms)"),
    ("Robotics Engineer", 5, "Participate in competitions / internships"),

    # IoT Developer
    ("IoT Developer", 1, "Learn Python and C for microcontrollers"),
    ("IoT Developer", 2, "Understand ESP32/Arduino & sensors"),
    ("IoT Developer", 3, "Learn MQTT and IoT protocols"),
    ("IoT Developer", 4, "Build IoT projects (home automation, monitoring)"),
    ("IoT Developer", 5, "Document projects and build portfolio"),

    # Doctor
    ("Doctor", 1, "Complete medical degree (MBBS/MD)"),
    ("Doctor", 2, "Gain clinical experience through rotations"),
    ("Doctor", 3, "Pass licensing exams"),
    ("Doctor", 4, "Specialize through residency if desired"),
    ("Doctor", 5, "Start practicing or join a hospital"),

    # Nurse
    ("Nurse", 1, "Complete nursing degree"),
    ("Nurse", 2, "Learn patient care and clinical procedures"),
    ("Nurse", 3, "Gain practical experience in hospitals"),
    ("Nurse", 4, "Learn communication and time management skills"),
    ("Nurse", 5, "Specialize or work in healthcare facilities"),

    # Pharmacist
    ("Pharmacist", 1, "Complete pharmacy degree"),
    ("Pharmacist", 2, "Learn pharmacology & chemistry"),
    ("Pharmacist", 3, "Practice dispensing and patient counseling"),
    ("Pharmacist", 4, "Understand regulations and safety standards"),
    ("Pharmacist", 5, "Work in hospitals or pharmaceutical companies"),

    # Business Analyst
    ("Business Analyst", 1, "Learn data analysis and Excel"),
    ("Business Analyst", 2, "Understand business processes"),
    ("Business Analyst", 3, "Learn SQL and reporting tools"),
    ("Business Analyst", 4, "Work on case studies and projects"),
    ("Business Analyst", 5, "Apply for analyst roles / internships"),

    # Project Manager
    ("Project Manager", 1, "Learn leadership and planning skills"),
    ("Project Manager", 2, "Understand risk management and agile methodology"),
    ("Project Manager", 3, "Practice team management"),
    ("Project Manager", 4, "Manage small projects for experience"),
    ("Project Manager", 5, "Apply for project management roles"),

    # Entrepreneur
    ("Entrepreneur", 1, "Learn business strategy and finance"),
    ("Entrepreneur", 2, "Learn marketing and networking"),
    ("Entrepreneur", 3, "Start small projects or side business"),
    ("Entrepreneur", 4, "Build a team and scale operations"),
    ("Entrepreneur", 5, "Launch a startup or product"),

    # Graphic Designer
    ("Graphic Designer", 1, "Learn Photoshop and Illustrator"),
    ("Graphic Designer", 2, "Build portfolio with sample designs"),
    ("Graphic Designer", 3, "Learn UI/UX basics"),
    ("Graphic Designer", 4, "Practice typography and layout"),
    ("Graphic Designer", 5, "Apply for internships or freelance projects"),

    # Content Writer
    ("Content Writer", 1, "Learn writing techniques and grammar"),
    ("Content Writer", 2, "Understand SEO basics"),
    ("Content Writer", 3, "Practice creating blogs and articles"),
    ("Content Writer", 4, "Edit and proofread work"),
    ("Content Writer", 5, "Build portfolio and apply for writing jobs"),

    # Musician
    ("Musician", 1, "Learn instrument skills and music theory"),
    ("Musician", 2, "Practice regularly and perform"),
    ("Musician", 3, "Record music and collaborate"),
    ("Musician", 4, "Perform at events / online platforms"),
    ("Musician", 5, "Build portfolio and grow fanbase"),

    # Actor
    ("Actor", 1, "Learn acting and expression skills"),
    ("Actor", 2, "Practice in theater or short films"),
    ("Actor", 3, "Audition for roles and build network"),
    ("Actor", 4, "Take workshops and improve craft"),
    ("Actor", 5, "Start acting professionally / portfolio building"),

    # Research Scientist
    ("Research Scientist", 1, "Learn research methodology"),
    ("Research Scientist", 2, "Perform experiments and collect data"),
    ("Research Scientist", 3, "Analyze results and draw conclusions"),
    ("Research Scientist", 4, "Write papers and publish findings"),
    ("Research Scientist", 5, "Apply for research projects or PhD"),

    # Chemist
    ("Chemist", 1, "Learn chemistry fundamentals"),
    ("Chemist", 2, "Practice lab skills and experiments"),
    ("Chemist", 3, "Analyze results and document"),
    ("Chemist", 4, "Learn reporting and compliance"),
    ("Chemist", 5, "Apply for laboratory jobs or research roles"),

    # Physicist
    ("Physicist", 1, "Learn physics fundamentals and mathematics"),
    ("Physicist", 2, "Perform experiments and simulations"),
    ("Physicist", 3, "Analyze data and test theories"),
    ("Physicist", 4, "Write research papers and publish"),
    ("Physicist", 5, "Apply for research roles or PhD programs"),

    # Teacher
    ("Teacher", 1, "Learn teaching techniques and curriculum"),
    ("Teacher", 2, "Plan lessons and classroom activities"),
    ("Teacher", 3, "Practice teaching in real classes"),
    ("Teacher", 4, "Get certifications if required"),
    ("Teacher", 5, "Apply for teaching jobs / tutoring"),

    # Professor
    ("Professor", 1, "Earn advanced degree in your subject"),
    ("Professor", 2, "Gain research experience"),
    ("Professor", 3, "Publish papers and articles"),
    ("Professor", 4, "Teach undergraduate or graduate students"),
    ("Professor", 5, "Apply for academic positions"),

    #R&D Engineer (Core Product Development)
    ("R&D Engineer", 1, "Complete a degree in your core engineering branch"),
    ("R&D Engineer", 2, "Learn CAD/CAE tools and simulation software"),
    ("R&D Engineer", 3, "Work on small design and development projects"),
    ("R&D Engineer", 4, "Intern or contribute to R&D labs / innovation centers"),
    ("R&D Engineer", 5, "Build a portfolio of prototypes and research work"),

]

career_skills_data = [
    # Software Developer
    ("Software Developer", "Python", 30),
    ("Software Developer", "Java", 25),
    ("Software Developer", "C++", 20),
    ("Software Developer", "Algorithms", 15),
    ("Software Developer", "Git", 10),

    # Data Scientist
    ("Data Scientist", "Python", 30),
    ("Data Scientist", "Statistics", 20),
    ("Data Scientist", "Machine Learning", 25),
    ("Data Scientist", "Pandas", 15),
    ("Data Scientist", "SQL", 10),

    # Embedded Systems Engineer
    ("Embedded Systems Engineer", "C", 25),
    ("Embedded Systems Engineer", "C++", 25),
    ("Embedded Systems Engineer", "Microcontrollers", 20),
    ("Embedded Systems Engineer", "Electronics", 20),
    ("Embedded Systems Engineer", "Debugging", 10),

    # Cybersecurity Analyst
    ("Cybersecurity Analyst", "Networking", 25),
    ("Cybersecurity Analyst", "Linux", 20),
    ("Cybersecurity Analyst", "Cryptography", 20),
    ("Cybersecurity Analyst", "Firewalls", 20),
    ("Cybersecurity Analyst", "Security", 15),

    # Web Developer
    ("Web Developer", "HTML/CSS", 25),
    ("Web Developer", "JavaScript", 25),
    ("Web Developer", "React", 20),
    ("Web Developer", "Node.js", 20),
    ("Web Developer", "Backend", 10),

    # Cloud Engineer
    ("Cloud Engineer", "AWS", 25),
    ("Cloud Engineer", "Azure", 20),
    ("Cloud Engineer", "DevOps", 20),
    ("Cloud Engineer", "Python", 20),
    ("Cloud Engineer", "Linux", 15),

    # AI/ML Engineer
    ("AI/ML Engineer", "Python", 30),
    ("AI/ML Engineer", "Machine Learning", 30),
    ("AI/ML Engineer", "TensorFlow", 15),
    ("AI/ML Engineer", "Pandas", 15),
    ("AI/ML Engineer", "Statistics", 10),

    # Robotics Engineer
    ("Robotics Engineer", "C++", 25),
    ("Robotics Engineer", "Python", 25),
    ("Robotics Engineer", "ROS", 20),
    ("Robotics Engineer", "Microcontrollers", 15),
    ("Robotics Engineer", "Sensors", 15),

    # IoT Developer
    ("IoT Developer", "Python", 25),
    ("IoT Developer", "C", 25),
    ("IoT Developer", "ESP32", 15),
    ("IoT Developer", "Arduino", 15),
    ("IoT Developer", "Sensors", 10),
    ("IoT Developer", "MQTT", 10),

    # Doctor
    ("Doctor", "Medical Knowledge", 40),
    ("Doctor", "Diagnosis", 25),
    ("Doctor", "Patient Care", 15),
    ("Doctor", "Communication", 10),
    ("Doctor", "Ethics", 10),

    # Nurse
    ("Nurse", "Patient Care", 30),
    ("Nurse", "Medical Knowledge", 25),
    ("Nurse", "Communication", 15),
    ("Nurse", "Time Management", 15),
    ("Nurse", "Empathy", 15),

    # Pharmacist
    ("Pharmacist", "Chemistry", 25),
    ("Pharmacist", "Pharmacology", 25),
    ("Pharmacist", "Attention to Detail", 20),
    ("Pharmacist", "Regulations", 15),
    ("Pharmacist", "Communication", 15),

    # Business Analyst
    ("Business Analyst", "Data Analysis", 25),
    ("Business Analyst", "SQL", 20),
    ("Business Analyst", "Communication", 20),
    ("Business Analyst", "Problem Solving", 20),
    ("Business Analyst", "Excel", 15),

    # Project Manager
    ("Project Manager", "Leadership", 25),
    ("Project Manager", "Planning", 20),
    ("Project Manager", "Risk Management", 20),
    ("Project Manager", "Communication", 20),
    ("Project Manager", "Agile", 15),

    # Entrepreneur
    ("Entrepreneur", "Business Strategy", 25),
    ("Entrepreneur", "Marketing", 20),
    ("Entrepreneur", "Leadership", 20),
    ("Entrepreneur", "Finance", 20),
    ("Entrepreneur", "Networking", 15),

    # Graphic Designer
    ("Graphic Designer", "Photoshop", 25),
    ("Graphic Designer", "Illustrator", 25),
    ("Graphic Designer", "Creativity", 20),
    ("Graphic Designer", "UI/UX", 20),
    ("Graphic Designer", "Typography", 10),

    # Content Writer
    ("Content Writer", "Writing", 30),
    ("Content Writer", "SEO", 20),
    ("Content Writer", "Creativity", 20),
    ("Content Writer", "Research", 15),
    ("Content Writer", "Editing", 15),

    # Musician
    ("Musician", "Instrument Skills", 25),
    ("Musician", "Music Theory", 20),
    ("Musician", "Creativity", 20),
    ("Musician", "Performance", 20),
    ("Musician", "Collaboration", 15),

    # Actor
    ("Actor", "Acting", 30),
    ("Actor", "Expression", 25),
    ("Actor", "Creativity", 20),
    ("Actor", "Communication", 15),
    ("Actor", "Networking", 10),

    # Research Scientist
    ("Research Scientist", "Research", 25),
    ("Research Scientist", "Experimentation", 20),
    ("Research Scientist", "Analysis", 20),
    ("Research Scientist", "Communication", 15),
    ("Research Scientist", "Writing", 20),

    # Chemist
    ("Chemist", "Chemistry", 30),
    ("Chemist", "Lab Skills", 25),
    ("Chemist", "Analysis", 20),
    ("Chemist", "Experimentation", 15),
    ("Chemist", "Reporting", 10),

    # Physicist
    ("Physicist", "Physics", 30),
    ("Physicist", "Mathematics", 25),
    ("Physicist", "Research", 20),
    ("Physicist", "Analysis", 15),
    ("Physicist", "Problem Solving", 10),

    # Teacher
    ("Teacher", "Subject Knowledge", 30),
    ("Teacher", "Communication", 25),
    ("Teacher", "Patience", 20),
    ("Teacher", "Lesson Planning", 15),
    ("Teacher", "Creativity", 10),

    # Professor
    ("Professor", "Research", 25),
    ("Professor", "Teaching", 25),
    ("Professor", "Communication", 20),
    ("Professor", "Publication", 15),
    ("Professor", "Mentorship", 15),

    #R&D Engineer (Core Product Development)
    ("R&D Engineer", "Core Engineering Fundamentals", 30),
    ("R&D Engineer", "CAD/CAE Software", 25),
    ("R&D Engineer", "Mathematics & Simulation", 20),
    ("R&D Engineer", "Problem Solving & Innovation", 15),
    ("R&D Engineer", "Project Documentation & Reporting", 10),

]

career_income_data = [
    # Technology / Engineering
    ("Software Developer", 400000, 1200000),       # (fresher, experienced)
    ("Data Scientist", 450000, 1500000),
    ("Embedded Systems Engineer", 350000, 1000000),
    ("Cybersecurity Analyst", 400000, 1300000),
    ("Web Developer", 300000, 900000),
    ("Cloud Engineer", 450000, 1400000),
    ("AI/ML Engineer", 500000, 1600000),
    ("Robotics Engineer", 400000, 1300000),
    ("IoT Developer", 350000, 1100000),

    # Medical / Health
    ("Doctor", 600000, 2500000),
    ("Nurse", 300000, 800000),
    ("Pharmacist", 350000, 900000),

    # Management / Business
    ("Business Analyst", 400000, 1200000),
    ("Project Manager", 500000, 1500000),
    ("Entrepreneur", 0, 0),  # Wide range, can add custom estimate

    # Arts / Humanities
    ("Graphic Designer", 250000, 700000),
    ("Content Writer", 200000, 600000),
    ("Musician", 150000, 1000000),
    ("Actor", 150000, 2000000),

    # Science / Research
    ("Research Scientist", 400000, 1300000),
    ("Chemist", 350000, 900000),
    ("Physicist", 400000, 1200000),

    # Education
    ("Teacher", 250000, 600000),
    ("Professor", 400000, 1200000),

    #R&D Engineer (Core Product Development)
    ("R&D Engineer", 400000, 1200000),


]


# ------------------ INSERT DATA ------------------ 
c.executemany("INSERT OR IGNORE INTO career_paths VALUES (?, ?)", career_paths_data)
c.executemany("INSERT OR IGNORE INTO career_roadmaps VALUES (?, ?, ?)", career_roadmaps_data)
c.executemany("INSERT OR IGNORE INTO career_skill_importance VALUES (?, ?, ?)", career_skills_data)
c.executemany("INSERT OR IGNORE INTO career_income VALUES (?, ?, ?)", career_income_data)


conn.commit()
conn.close()
print("Database created with expanded career data!")
