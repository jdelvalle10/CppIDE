🖥️ C++ IDE — Self-Hosted Classroom Environment
A containerized, browser-based C++ development environment for classroom use, built on code-server (VS Code in the browser), Docker, and Caddy. Designed for intranet deployment — no internet connection required once built.

Developed for use at Doral Academy and Miami Dade College
Maintainer: Professor Del Valle — Cybersecurity & Computer Science


What This Is
Each student gets their own isolated VS Code environment running in a Docker container, accessible from any browser on the school network. Code is saved to a persistent Docker volume — students pick up exactly where they left off between sessions.
FeatureDetailIDEVS Code (code-server 4.23.1)CompilerGCC 12, C++17 (-std=c++17)IsolationOne Docker container per studentPersistenceDocker named volumes (survives restarts)RoutingCaddy reverse proxy (HTTPS, intranet)AuthPer-student password via environment variableTarget scale15–30 concurrent users

Repository Structure
cpp-ide-deploy/
├── Dockerfile              # Custom image — GCC 12 + code-server + extensions
├── settings.json           # VS Code settings baked into the image
├── hello.cpp               # Starter file loaded in every student workspace
├── students.csv            # Your student roster (username, password, name)
├── generate_compose.py     # Generates docker-compose.yml from students.csv
├── generate_caddyfile.py   # Generates Caddyfile from students.csv
├── deploy.sh               # One-command deployment script
└── README.md               # This file

Server Requirements
ResourceMinimumRecommendedCPU8 cores16+ coresRAM32 GB64 GBOSUbuntu Server 22.04 LTSUbuntu Server 22.04 LTSNetworkIntranet (LAN)Intranet (LAN)InternetBuild time onlyBuild time only

Note: At 30 concurrent students, expect ~30–45 GB RAM usage at peak compilation. A 64 GB server handles this comfortably.


Quick Start
1. Clone the Repository
bashgit clone https://github.com/your-org/cpp-ide-deploy.git
cd cpp-ide-deploy
2. Configure Your Server Hostname
Edit generate_caddyfile.py and replace the placeholder with your actual server hostname or intranet IP:
pythonSERVER_HOST = "your-server.school.local"   # ← change this
3. Populate the Student Roster
Edit students.csv with your class roster:
csvusername,password,display_name
jdoe,Doe2024!,John Doe
msmith,Smith2024!,Maria Smith
alopez,Lopez2024!,Ana Lopez

Security: Use unique passwords per student. Do not commit real passwords to a public repository. See Managing Secrets below.

4. Run the Deployment Script
bashchmod +x deploy.sh
./deploy.sh
This script will:

Install Docker (if not present)
Install the Docker Compose plugin
Install Caddy
Build the cpp-ide:latest Docker image
Generate docker-compose.yml and Caddyfile from your roster
Start all student containers
Start the Caddy reverse proxy

5. Hand Out Student URLs
Each student accesses their environment at:
https://your-server.school.local/ide/USERNAME
They enter their password and get a full VS Code interface with C++17 ready to go.

Student Experience

Open any browser on the school network
Navigate to https://your-server.school.local/ide/their-username
Enter their password
Full VS Code loads — a starter hello.cpp is already open
Write code, open the integrated terminal, compile and run:

bashg++ -std=c++17 -Wall -o hello hello.cpp && ./hello
Or click the ▶ Run button (Code Runner extension) for one-click compile and run.
Files are automatically saved every 2 seconds and persist across sessions.

Pre-Installed VS Code Extensions
ExtensionPurposems-vscode.cpptoolsC/C++ IntelliSense, syntax highlighting, debuggingms-vscode.cpptools-extension-packExtended C++ toolingformulahendry.code-runnerOne-click compile and run

Compiler Configuration
All code is compiled with:
bashg++ -std=c++17 -Wall -Wextra -o <output> <source>
Standard libraries available out of the box:

<iostream>, <fstream>, <sstream>
<string>, <vector>, <array>, <list>, <map>, <set>
<cmath>, <cstdlib>, <ctime>
<algorithm>, <functional>, <utility>
<stdexcept>, <memory>, <thread>


Common Operations
bash# Check all running containers
docker compose ps

# View logs for a specific student
docker compose logs ide_jdoe

# Restart one student's container
docker compose restart ide_jdoe

# Stop all containers (e.g., end of school day)
docker compose stop

# Bring all containers back up
docker compose up -d

# Reload Caddy after editing the Caddyfile
sudo systemctl reload caddy
Adding a New Student Mid-Semester
bash# 1. Add a row to students.csv
# 2. Regenerate config files
python3 generate_compose.py
python3 generate_caddyfile.py

# 3. Bring up new container (existing ones are unaffected)
docker compose up -d

# 4. Reload Caddy
sudo systemctl reload caddy
Changing a Student's Password
Edit students.csv, then:
bashpython3 generate_compose.py
docker compose up -d --force-recreate ide_USERNAME

HTTPS on the Intranet
Caddy automatically generates a self-signed TLS certificate using tls internal. Students will see a browser security warning on first visit. They can proceed by clicking Advanced → Continue to site.
For a cleaner experience without warnings, distribute Caddy's root CA certificate to student machines (one-time IT task):
bash# On the server — find the CA cert
caddy trust

# Caddy stores its CA at:
# ~/.local/share/caddy/pki/authorities/local/root.crt
Install that certificate as a trusted root on each student device or push it via your school's MDM/GPO system.

Managing Secrets
Do not commit students.csv with real passwords to a public repository.
Options:

Add students.csv to .gitignore and distribute it separately
Use a .env file approach and generate passwords programmatically
Use your school's existing credential management system

bash# Add to .gitignore
echo "students.csv" >> .gitignore

Troubleshooting
SymptomLikely CauseFixBrowser shows "site can't be reached"Caddy not running or wrong hostnamesudo systemctl status caddyStudent sees blank pageContainer not starteddocker compose ps — check statusPassword rejectedContainer needs restart after password changedocker compose up -d --force-recreate ide_USERNAMECode Runner shows compile errorWrong file saved or wrong executorCheck settings.json is baked into imageContainer keeps restartingOut of memorydocker stats — check RAM usage

Architecture Overview
[Student Browser]
       │  HTTPS
       ▼
[Caddy Reverse Proxy :443]
       │  routes by /ide/USERNAME path
       ▼
[Docker Network: ide_net]
       │
       ├── Container: ide_jdoe   → Volume: jdoe_workspace
       ├── Container: ide_msmith → Volume: msmith_workspace
       └── Container: ide_alopez → Volume: alopez_workspace

Each container:
  └── code-server (port 8080, internal only)
  └── GCC 12 / g++ (C++17)
  └── VS Code extensions

License
For internal academic use only. Not licensed for commercial redistribution.
code-server is licensed under the MIT License.

Contact
Professor Jose Luis Del Valle
Doral Academy / Miami Dade College
Cybersecurity, AI, Computer Science & Programming
