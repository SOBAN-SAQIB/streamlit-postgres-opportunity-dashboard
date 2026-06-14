# Internship & Job Tracking Dashboard

A full-stack web application for university departments to manage internship and job opportunities. Built with Streamlit, PostgreSQL, and Docker Compose.

---

## Project Overview

This system allows faculty members to:
- Add, view, search, update, and delete opportunity records
- Upload bulk data via CSV and export filtered results
- Detect duplicate entries automatically
- Monitor application deadlines with alerts
- View comprehensive analytics and KPIs
- Manage access via Admin and Viewer roles

---

## Team Members

| Name | Role | GitHub Username |
|------|------|-----------------|
| Member 1 | Backend & Database | @member1 |
| Member 2 | Frontend & UI | @member2 |
| Member 3 | Docker & DevOps | @member3 |
| Member 4 | Analytics & Reports | @member4 |

---

## Folder Structure

```
streamlit-postgres-assignment/
├── app/
│   ├── main.py                        # Home page & login
│   ├── db.py                          # Database connection
│   ├── queries.py                     # All SQL queries
│   ├── auth.py                        # Login & role management
│   ├── utils.py                       # CSV helpers & validation
│   └── pages/
│       ├── 1_Add_Opportunity.py
│       ├── 2_View_Search.py
│       ├── 3_Update_Opportunity.py
│       ├── 4_Delete_Opportunity.py
│       ├── 5_Analytics_Dashboard.py
│       ├── 6_CSV_Upload_Export.py
│       ├── 7_Duplicate_Detection.py
│       ├── 8_Deadline_Alerts.py
│       └── 9_Database_Health_Check.py
├── database/
│   ├── init.sql                       # Table schema
│   └── seed_data.sql                  # 45 sample records
├── screenshots/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Git](https://git-scm.com/) installed
- No Python installation required on the host machine (runs inside Docker)

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/streamlit-postgres-opportunity-dashboard.git
cd streamlit-postgres-opportunity-dashboard
```

### 2. Start all services

```bash
docker compose up -d
```

This single command starts:
- **PostgreSQL** on port `5432`
- **pgAdmin** on port `5050`
- **Streamlit app** on port `8501`

### 3. Access the applications

| Service | URL | Credentials |
|---------|-----|-------------|
| Streamlit App | http://localhost:8501 | admin / admin123 |
| pgAdmin | http://localhost:5050 | admin@example.com / admin123 |

### 4. Login credentials for Streamlit

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin (full access) |
| viewer | view123 | Viewer (read-only) |

---

## Docker Compose Explanation

The `docker-compose.yml` defines three services connected via a shared Docker network (`app_network`).

### Services

#### `postgres_db`
```yaml
postgres_db:
  image: postgres:latest          # Official PostgreSQL image
  container_name: opportunity_postgres
  environment:
    POSTGRES_DB: student_opportunities_db   # Database name
    POSTGRES_USER: app_user                 # DB user
    POSTGRES_PASSWORD: app_password         # DB password
  ports:
    - "5432:5432"                 # host:container port mapping
  volumes:
    - postgres_data:/var/lib/postgresql/data          # Named volume for persistence
    - ./database/init.sql:/docker-entrypoint-initdb.d/01_init.sql   # Auto-runs on first start
    - ./database/seed_data.sql:/docker-entrypoint-initdb.d/02_seed_data.sql
  restart: unless-stopped         # Restart policy: restart unless manually stopped
```

- **`image`**: Uses the official PostgreSQL Docker image
- **`environment`**: Sets database name, user, and password inside the container
- **`ports`**: Maps container port 5432 to host port 5432
- **`volumes`**: Named volume preserves data; SQL files in `/docker-entrypoint-initdb.d/` are auto-executed on first startup
- **`restart: unless-stopped`**: Container automatically restarts after crashes or system reboots

#### `pgadmin`
```yaml
pgadmin:
  image: dpage/pgadmin4:latest
  depends_on:
    - postgres_db                 # Waits for postgres_db to start first
  ports:
    - "5050:80"                   # pgAdmin web UI on port 5050
```

- **`depends_on`**: Ensures PostgreSQL starts before pgAdmin
- **`ports`**: pgAdmin runs on port 80 inside the container, mapped to host port 5050

#### `streamlit_app`
```yaml
streamlit_app:
  build: .                        # Build from local Dockerfile
  depends_on:
    - postgres_db
  environment:
    DB_HOST: postgres_db          # Uses service name as hostname (Docker DNS)
    DB_PORT: 5432
```

- **`build: .`**: Builds a Docker image from the `Dockerfile` in the current directory
- **`DB_HOST: postgres_db`**: Docker's internal network resolves the service name `postgres_db` as the hostname — no IP address needed

### Volumes

```yaml
volumes:
  postgres_data:    # Named volume; persists even when containers are stopped
```

### Networks

```yaml
networks:
  app_network:
    driver: bridge  # All three services communicate on this private network
```

---

## Dockerfile Explanation

```dockerfile
FROM python:3.11-slim             # Lightweight Python base image

WORKDIR /app                      # Set working directory inside container
COPY requirements.txt .           # Copy requirements first (Docker layer caching)
RUN pip install --no-cache-dir -r requirements.txt   # Install dependencies

COPY app/ ./app/                  # Copy Streamlit application code
EXPOSE 8501                       # Document the port (does not publish it)

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

---

## Database Setup

The database is initialized automatically when the PostgreSQL container first starts. The SQL files in `database/` are mounted into `/docker-entrypoint-initdb.d/` and executed in alphabetical/numbered order.

### Schema (`init.sql`)

```sql
CREATE TABLE opportunities (
    opportunity_id SERIAL PRIMARY KEY,
    company_name   VARCHAR(100) NOT NULL,
    job_title      VARCHAR(150) NOT NULL,
    category       VARCHAR(50)  NOT NULL,
    city           VARCHAR(80),
    country        VARCHAR(80),
    work_mode      VARCHAR(30)  CHECK (work_mode IN ('Remote', 'Onsite', 'Hybrid')),
    required_skills TEXT        NOT NULL,
    salary_min     NUMERIC(10,2),
    salary_max     NUMERIC(10,2),
    currency       VARCHAR(10)  DEFAULT 'PKR',
    experience_level VARCHAR(50),
    application_deadline DATE,
    status         VARCHAR(30)  DEFAULT 'Open'
                                CHECK (status IN ('Open', 'Closed', 'Expired', 'Shortlisted')),
    source_link    TEXT,
    created_at     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
```

### Seed Data (`seed_data.sql`)

- 45 sample records across 8 companies
- 5 cities: Karachi, Lahore, Islamabad, Rawalpindi, Peshawar
- 5 categories: Data Science, AI, Web Development, Cyber Security, Software Engineering
- All work modes: Remote, Onsite, Hybrid
- All statuses: Open, Closed, Expired, Shortlisted

---

## pgAdmin Setup

1. Open http://localhost:5050
2. Login: `admin@example.com` / `admin123`
3. Right-click **Servers** → **Register** → **Server**
4. Fill in the **General** tab:
   - Name: `OpportunityDB`
5. Fill in the **Connection** tab:
   - Host: `postgres_db` *(use the Docker service name, not localhost)*
   - Port: `5432`
   - Database: `student_opportunities_db`
   - Username: `app_user`
   - Password: `app_password`
6. Click **Save**

### Verification SQL Queries

Run these in pgAdmin's Query Tool (`Tools` → `Query Tool`):

```sql
-- View all records
SELECT * FROM opportunities;

-- Count total records
SELECT COUNT(*) FROM opportunities;

-- Records by category
SELECT category, COUNT(*) FROM opportunities GROUP BY category;

-- Records by work mode
SELECT work_mode, COUNT(*) FROM opportunities GROUP BY work_mode;

-- Open opportunities only
SELECT * FROM opportunities WHERE status = 'Open';

-- Closing within 7 days
SELECT * FROM opportunities
WHERE application_deadline <= CURRENT_DATE + INTERVAL '7 days';
```

---

## Docker Commands Reference

| Command | Purpose |
|---------|---------|
| `docker compose up -d` | Start all services in detached (background) mode |
| `docker compose ps` | Check running services and their mapped ports |
| `docker compose logs postgres_db` | View PostgreSQL container logs |
| `docker compose logs pgadmin` | View pgAdmin container logs |
| `docker compose logs streamlit_app` | View Streamlit app logs |
| `docker compose down` | Stop and remove containers (data preserved in volumes) |
| `docker volume ls` | List all Docker volumes |
| `docker volume inspect t_t_4_postgres_data` | Inspect the PostgreSQL volume |
| `docker compose down -v` | Stop containers AND delete volumes (WARNING: deletes all data) |
| `docker compose build --no-cache` | Rebuild the Streamlit image from scratch |
| `docker compose restart streamlit_app` | Restart only the Streamlit service |

---

## GitHub Workflow

```bash
# Initial setup
git init
git add .
git commit -m "initial project structure"
git branch -M main
git remote add origin <your-github-repository-url>
git push -u origin main

# Daily workflow
git status
git add app/pages/1_Add_Opportunity.py
git commit -m "add opportunity form with validation"
git push
```

### Commit Message Conventions

- `add <feature>` — new functionality added
- `fix <bug>` — bug fix
- `update <component>` — enhancement to existing feature
- `refactor <module>` — code restructure without behavior change
- `docs <section>` — documentation update
- `style <page>` — UI/layout improvement

---

## Troubleshooting

### PostgreSQL container not starting
```bash
docker compose logs postgres_db
# Common cause: port 5432 already in use
netstat -ano | findstr :5432      # Windows
lsof -i :5432                     # Mac/Linux
```

### pgAdmin cannot connect to PostgreSQL
- Use `postgres_db` as the host (not `localhost`) — Docker service name resolution
- Verify the container is running: `docker compose ps`

### Port already in use
```bash
# Change the host port in docker-compose.yml, e.g.:
ports:
  - "5433:5432"   # Use 5433 on host instead
```

### Streamlit cannot connect to database
```bash
docker compose logs streamlit_app
# Check DB_HOST is set to "postgres_db" not "localhost"
```

### Table does not exist
```bash
# The init.sql didn't run — happens if volume already existed
docker compose down -v    # Delete volume
docker compose up -d      # Fresh start (re-runs init.sql)
```

### CSV upload fails — missing columns
Download the template from the CSV Upload page and ensure your file matches the required column names exactly.

### Data disappears after `docker compose down -v`
The `-v` flag removes named volumes. Use `docker compose down` (without `-v`) to preserve data.

### Git push rejected
```bash
git pull --rebase origin main    # Fetch and rebase
git push                         # Then push
```

### Merge conflict during group work
```bash
git status                       # See conflicting files
# Manually resolve conflicts in the files
git add <resolved-file>
git commit -m "resolve merge conflict in <file>"
git push
```

---

## Application Pages

| Page | Access | Description |
|------|--------|-------------|
| Home | All | Project overview, architecture, team info |
| Add Opportunity | Admin only | Insert new records with full validation |
| View & Search | All | Browse, filter, search all records |
| Update Opportunity | Admin only | Edit status, salary, deadline, skills |
| Delete Opportunity | Admin only | Preview and permanently delete a record |
| Analytics Dashboard | All | KPIs, charts, trends, skill frequency |
| CSV Upload / Export | Upload: Admin / Export: All | Bulk insert and download |
| Duplicate Detection | All | Find and remove duplicate records |
| Deadline Alerts | All | Closing soon and expired opportunities |
| Database Health Check | All | Connection status, schema, SQL runner |

---

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [pgAdmin Container Docs](https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Plotly Python Documentation](https://plotly.com/python/)
