# 💼 Jobs Data Cleaning Mini Project

An automated ETL pipeline designed to extract, clean, and analyze job market data using **Apache Airflow** and **PostgreSQL**.

## 📁 Project Structure
```text
Jobs-Cleaning-Mini-Project/
├── dags/               # Airflow DAG definitions
├── etl/                # Python scripts for Extract, Transform, Load
├── sql/                # SQL scripts for data transformation and databases initilization
├── data/               # Raw data files (.csv)
├── analysis/           # Post-cleaning data analysis
├── config.py           # Database connection settings
├── pipeline.py         # Manual pipeline execution script
├── requirements.txt    # Project dependencies
└── constraints.txt     # Airflow version-specific constraints
```

## 🛠 Installation & Setup
### 1. Environment Setup
Create a virtual environment and install dependencies using the constraints file to ensure version compatibility:
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install libraries with constraints
pip install -r requirements.txt --constraint constraints.txt
```

### 2. Database Initialization (PostgreSQL)
You need to create the tables manually by executing the SQL scripts provided in the sql/ folder. You can use psql or any DB tool (pgAdmin, DBeaver):
```bash
# Initialize the staging/temporary tables
psql -U your_user -d your_temporary_database -f sql/init_temp.sql

# Initialize the main warehouse tables
psql -U your_user -d your_warehouse_database -f sql/init_db.sql
```
***Note:** Update your credentials in ***config.py*** after creating the tables.*

### 3. Airflow Setup & Integration
```bash
# Link the project DAG to Airflow
mkdir -p ~/airflow/dags
ln -s $(pwd)/dags/jobs_dag.py ~/airflow/dags/
```

### 4. Start Airflow
```bash
airflow standalone
```

## 🔄 ETL Workflow
**1. Extract:** Reads raw data and loads it into the PostgreSQL Staging Area.  
**2. Transform:** Executes cleaning and standardization logic using SQL.  
**3. Load:** Finalizes data migration into the Data Warehouse.

## 📊 Analysis & Visualization
After the ETL pipeline completes, run the visualization script to generate insights:
```bash
python3 analysis/visualize.py
```
