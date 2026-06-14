-- Seed data: 45 sample internship/job opportunities
-- Companies: Systems Ltd, Arbisoft, NetSol, Folio3, 10Pearls, Contour Software, Tkxel, i2c
-- Cities: Karachi, Lahore, Islamabad, Rawalpindi, Peshawar
-- Categories: Data Science, AI, Web Development, Cyber Security, Software Engineering

INSERT INTO opportunities (company_name, job_title, category, city, country, work_mode, required_skills, salary_min, salary_max, currency, experience_level, application_deadline, status, source_link) VALUES

-- Systems Ltd
('Systems Ltd', 'Junior Data Scientist', 'Data Science', 'Karachi', 'Pakistan', 'Hybrid', 'Python, Pandas, NumPy, Machine Learning, SQL', 60000, 90000, 'PKR', 'Entry Level', '2026-07-15', 'Open', 'https://systemsltd.com/careers'),
('Systems Ltd', 'Senior Software Engineer', 'Software Engineering', 'Lahore', 'Pakistan', 'Onsite', 'Java, Spring Boot, Microservices, Docker, Kubernetes', 150000, 220000, 'PKR', 'Senior Level', '2026-07-20', 'Open', 'https://systemsltd.com/careers'),
('Systems Ltd', 'Web Developer Intern', 'Web Development', 'Karachi', 'Pakistan', 'Onsite', 'HTML, CSS, JavaScript, React, Node.js', 25000, 35000, 'PKR', 'Internship', '2026-06-30', 'Open', 'https://systemsltd.com/careers'),
('Systems Ltd', 'Cyber Security Analyst', 'Cyber Security', 'Islamabad', 'Pakistan', 'Hybrid', 'Network Security, SIEM, Penetration Testing, OWASP, Firewalls', 100000, 150000, 'PKR', 'Mid Level', '2026-08-01', 'Closed', 'https://systemsltd.com/careers'),
('Systems Ltd', 'AI Research Engineer', 'AI', 'Lahore', 'Pakistan', 'Remote', 'TensorFlow, PyTorch, NLP, Computer Vision, Python', 130000, 200000, 'PKR', 'Senior Level', '2026-07-10', 'Open', 'https://systemsltd.com/careers'),

-- Arbisoft
('Arbisoft', 'Full Stack Developer', 'Web Development', 'Lahore', 'Pakistan', 'Hybrid', 'React, Django, PostgreSQL, REST APIs, AWS', 90000, 140000, 'PKR', 'Mid Level', '2026-07-25', 'Open', 'https://arbisoft.com/careers'),
('Arbisoft', 'Data Engineer', 'Data Science', 'Lahore', 'Pakistan', 'Remote', 'Apache Spark, Kafka, Python, Airflow, AWS Glue', 120000, 180000, 'PKR', 'Mid Level', '2026-06-25', 'Shortlisted', 'https://arbisoft.com/careers'),
('Arbisoft', 'Machine Learning Engineer', 'AI', 'Lahore', 'Pakistan', 'Hybrid', 'Python, Scikit-learn, TensorFlow, MLflow, Docker', 110000, 170000, 'PKR', 'Mid Level', '2026-08-10', 'Open', 'https://arbisoft.com/careers'),
('Arbisoft', 'DevOps Engineer', 'Software Engineering', 'Lahore', 'Pakistan', 'Remote', 'Docker, Kubernetes, Jenkins, AWS, Terraform, Linux', 100000, 160000, 'PKR', 'Mid Level', '2026-07-30', 'Open', 'https://arbisoft.com/careers'),
('Arbisoft', 'Security Engineer', 'Cyber Security', 'Lahore', 'Pakistan', 'Onsite', 'AWS Security, IAM, Vulnerability Assessment, Python, SIEM', 130000, 190000, 'PKR', 'Senior Level', '2026-05-30', 'Expired', 'https://arbisoft.com/careers'),

-- NetSol Technologies
('NetSol Technologies', 'Business Intelligence Analyst', 'Data Science', 'Lahore', 'Pakistan', 'Onsite', 'Power BI, Tableau, SQL, Excel, DAX, Data Modeling', 70000, 110000, 'PKR', 'Mid Level', '2026-07-18', 'Open', 'https://netsol.com/careers'),
('NetSol Technologies', 'React Native Developer', 'Web Development', 'Lahore', 'Pakistan', 'Hybrid', 'React Native, JavaScript, Redux, REST APIs, TypeScript', 80000, 130000, 'PKR', 'Mid Level', '2026-08-05', 'Open', 'https://netsol.com/careers'),
('NetSol Technologies', 'AI Solutions Architect', 'AI', 'Islamabad', 'Pakistan', 'Remote', 'Azure AI, OpenAI API, LangChain, Python, Solution Design', 200000, 300000, 'PKR', 'Senior Level', '2026-07-22', 'Open', 'https://netsol.com/careers'),
('NetSol Technologies', 'QA Engineer Intern', 'Software Engineering', 'Lahore', 'Pakistan', 'Onsite', 'Manual Testing, Selenium, JIRA, Test Cases, Agile', 20000, 30000, 'PKR', 'Internship', '2026-06-20', 'Closed', 'https://netsol.com/careers'),
('NetSol Technologies', 'Network Security Engineer', 'Cyber Security', 'Karachi', 'Pakistan', 'Onsite', 'Cisco, Firewall Configuration, VPN, IDS/IPS, Network Monitoring', 110000, 160000, 'PKR', 'Mid Level', '2026-07-28', 'Open', 'https://netsol.com/careers'),

-- Folio3
('Folio3', 'Python Backend Developer', 'Software Engineering', 'Karachi', 'Pakistan', 'Hybrid', 'Python, Django, FastAPI, PostgreSQL, Redis, Docker', 90000, 145000, 'PKR', 'Mid Level', '2026-08-15', 'Open', 'https://folio3.com/careers'),
('Folio3', 'Data Scientist Intern', 'Data Science', 'Karachi', 'Pakistan', 'Onsite', 'Python, Statistics, Pandas, Data Visualization, ML Basics', 25000, 40000, 'PKR', 'Internship', '2026-07-01', 'Open', 'https://folio3.com/careers'),
('Folio3', 'Computer Vision Engineer', 'AI', 'Karachi', 'Pakistan', 'Remote', 'OpenCV, YOLO, TensorFlow, Python, Image Processing', 140000, 210000, 'PKR', 'Senior Level', '2026-07-15', 'Shortlisted', 'https://folio3.com/careers'),
('Folio3', 'Angular Developer', 'Web Development', 'Karachi', 'Pakistan', 'Hybrid', 'Angular, TypeScript, RxJS, REST APIs, SCSS', 75000, 120000, 'PKR', 'Mid Level', '2026-06-15', 'Expired', 'https://folio3.com/careers'),
('Folio3', 'Penetration Tester', 'Cyber Security', 'Karachi', 'Pakistan', 'Onsite', 'Kali Linux, Metasploit, Burp Suite, OWASP, Ethical Hacking', 120000, 180000, 'PKR', 'Mid Level', '2026-08-20', 'Open', 'https://folio3.com/careers'),

-- 10Pearls
('10Pearls', 'Software Engineer (Java)', 'Software Engineering', 'Islamabad', 'Pakistan', 'Hybrid', 'Java, Spring Boot, REST APIs, MySQL, Git, Agile', 80000, 130000, 'PKR', 'Entry Level', '2026-07-12', 'Open', 'https://10pearls.com/careers'),
('10Pearls', 'NLP Engineer', 'AI', 'Islamabad', 'Pakistan', 'Remote', 'Python, NLTK, SpaCy, Transformers, BERT, GPT', 150000, 230000, 'PKR', 'Senior Level', '2026-08-08', 'Open', 'https://10pearls.com/careers'),
('10Pearls', 'Data Analyst', 'Data Science', 'Islamabad', 'Pakistan', 'Onsite', 'SQL, Excel, Python, Tableau, Statistical Analysis', 65000, 100000, 'PKR', 'Entry Level', '2026-07-05', 'Open', 'https://10pearls.com/careers'),
('10Pearls', 'Vue.js Developer', 'Web Development', 'Islamabad', 'Pakistan', 'Remote', 'Vue.js, JavaScript, Vuex, REST APIs, Node.js', 85000, 135000, 'PKR', 'Mid Level', '2026-05-20', 'Expired', 'https://10pearls.com/careers'),
('10Pearls', 'Information Security Analyst', 'Cyber Security', 'Islamabad', 'Pakistan', 'Hybrid', 'ISO 27001, Risk Assessment, Security Audits, Compliance, GDPR', 100000, 155000, 'PKR', 'Mid Level', '2026-07-19', 'Open', 'https://10pearls.com/careers'),

-- Contour Software
('Contour Software', 'Senior Data Scientist', 'Data Science', 'Karachi', 'Pakistan', 'Hybrid', 'Python, R, Machine Learning, Deep Learning, SQL, Tableau', 160000, 250000, 'PKR', 'Senior Level', '2026-08-25', 'Open', 'https://contour-software.com/careers'),
('Contour Software', 'Cloud Infrastructure Engineer', 'Software Engineering', 'Karachi', 'Pakistan', 'Remote', 'AWS, Azure, GCP, Terraform, Docker, Kubernetes, CI/CD', 140000, 220000, 'PKR', 'Senior Level', '2026-07-22', 'Open', 'https://contour-software.com/careers'),
('Contour Software', 'AI Product Manager', 'AI', 'Karachi', 'Pakistan', 'Hybrid', 'Product Management, AI/ML Understanding, Agile, JIRA, Roadmapping', 180000, 270000, 'PKR', 'Senior Level', '2026-06-30', 'Shortlisted', 'https://contour-software.com/careers'),
('Contour Software', 'Frontend Developer Intern', 'Web Development', 'Karachi', 'Pakistan', 'Onsite', 'HTML, CSS, JavaScript, React Basics, Git', 20000, 30000, 'PKR', 'Internship', '2026-07-10', 'Open', 'https://contour-software.com/careers'),
('Contour Software', 'SOC Analyst', 'Cyber Security', 'Karachi', 'Pakistan', 'Onsite', 'SIEM, Log Analysis, Incident Response, Threat Intelligence, Security Tools', 90000, 140000, 'PKR', 'Entry Level', '2026-08-01', 'Open', 'https://contour-software.com/careers'),

-- Tkxel
('Tkxel', 'MLOps Engineer', 'AI', 'Lahore', 'Pakistan', 'Remote', 'MLflow, Kubeflow, Docker, Python, CI/CD, AWS SageMaker', 130000, 200000, 'PKR', 'Mid Level', '2026-07-29', 'Open', 'https://tkxel.com/careers'),
('Tkxel', 'Node.js Developer', 'Web Development', 'Lahore', 'Pakistan', 'Hybrid', 'Node.js, Express, MongoDB, REST APIs, GraphQL, Docker', 75000, 125000, 'PKR', 'Mid Level', '2026-08-12', 'Open', 'https://tkxel.com/careers'),
('Tkxel', 'Data Engineer Intern', 'Data Science', 'Lahore', 'Pakistan', 'Onsite', 'Python, SQL, ETL Basics, Excel, Data Pipelines', 22000, 32000, 'PKR', 'Internship', '2026-06-18', 'Closed', 'https://tkxel.com/careers'),
('Tkxel', 'Software Engineer (.NET)', 'Software Engineering', 'Rawalpindi', 'Pakistan', 'Onsite', '.NET Core, C#, SQL Server, Entity Framework, Azure', 80000, 130000, 'PKR', 'Mid Level', '2026-07-25', 'Open', 'https://tkxel.com/careers'),
('Tkxel', 'Cloud Security Specialist', 'Cyber Security', 'Rawalpindi', 'Pakistan', 'Remote', 'AWS Security Hub, CloudTrail, IAM, Security Groups, Compliance', 140000, 210000, 'PKR', 'Senior Level', '2026-08-18', 'Open', 'https://tkxel.com/careers'),

-- i2c Inc
('i2c Inc', 'Big Data Engineer', 'Data Science', 'Rawalpindi', 'Pakistan', 'Hybrid', 'Hadoop, Spark, Hive, Scala, Python, AWS EMR', 130000, 200000, 'PKR', 'Mid Level', '2026-07-20', 'Open', 'https://i2cinc.com/careers'),
('i2c Inc', 'Generative AI Developer', 'AI', 'Rawalpindi', 'Pakistan', 'Hybrid', 'LangChain, OpenAI, Python, Vector Databases, RAG, LLMs', 160000, 250000, 'PKR', 'Mid Level', '2026-08-05', 'Open', 'https://i2cinc.com/careers'),
('i2c Inc', 'Backend Developer (Go)', 'Software Engineering', 'Rawalpindi', 'Pakistan', 'Onsite', 'Go, gRPC, PostgreSQL, Kafka, Docker, Kubernetes', 110000, 170000, 'PKR', 'Mid Level', '2026-07-15', 'Open', 'https://i2cinc.com/careers'),
('i2c Inc', 'Security Software Engineer', 'Cyber Security', 'Rawalpindi', 'Pakistan', 'Onsite', 'Cryptography, Secure Coding, C++, Python, PKI, HSM', 150000, 220000, 'PKR', 'Senior Level', '2026-06-10', 'Expired', 'https://i2cinc.com/careers'),
('i2c Inc', 'React Developer Intern', 'Web Development', 'Rawalpindi', 'Pakistan', 'Hybrid', 'React, JavaScript, HTML, CSS, Git, Agile Basics', 25000, 38000, 'PKR', 'Internship', '2026-07-08', 'Open', 'https://i2cinc.com/careers'),

-- Additional remote/Peshawar entries for variety
('Netsol Technologies', 'Remote ML Researcher', 'AI', 'Peshawar', 'Pakistan', 'Remote', 'Python, Research Papers, PyTorch, Experiment Design, LaTeX', 120000, 190000, 'PKR', 'Senior Level', '2026-08-30', 'Open', 'https://netsol.com/careers'),
('Arbisoft', 'PHP Laravel Developer', 'Web Development', 'Peshawar', 'Pakistan', 'Remote', 'PHP, Laravel, MySQL, Vue.js, REST APIs, Git', 65000, 105000, 'PKR', 'Entry Level', '2026-07-14', 'Open', 'https://arbisoft.com/careers'),
('Folio3', 'Data Science Intern', 'Data Science', 'Peshawar', 'Pakistan', 'Remote', 'Python, Pandas, Matplotlib, Statistics, Jupyter', 18000, 28000, 'PKR', 'Internship', '2026-06-28', 'Shortlisted', 'https://folio3.com/careers'),
('Systems Ltd', 'Ethical Hacker', 'Cyber Security', 'Peshawar', 'Pakistan', 'Hybrid', 'CEH, Burp Suite, Nmap, Metasploit, Wireshark, Python', 100000, 160000, 'PKR', 'Mid Level', '2026-07-28', 'Open', 'https://systemsltd.com/careers'),
('10Pearls', 'Software Engineering Intern', 'Software Engineering', 'Peshawar', 'Pakistan', 'Remote', 'Python or Java, OOP, Git, Problem Solving, Communication', 20000, 30000, 'PKR', 'Internship', '2026-07-03', 'Open', 'https://10pearls.com/careers');
