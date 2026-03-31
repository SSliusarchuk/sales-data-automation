# Automated processing of cash register data for a retail chain

The project automates the generation and loading of sales data for a chain of household goods stores.

---
1. Clone the repository:
```bash
git clone https://github.com/SSliusarchuk/auto-depl.sim.git
cd auto-depl.sim
```
2. Create and activate a virtual environment:
```bash
 python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```
3. Install dependencies: pip install -r requirements.txt
4. Create a configuration file and fill in database connection details::
```bash
DB_NAME=<database_name>
DB_USER=<user>
DB_PASSWORD=<password>
DB_HOST=<host>
DB_PORT=<port>
```
## Usage
Data generation

The generate_data.py script creates CSV files for N stores in the data/ folder:
python scripts/generate_data.py
Files are named in the format: {{shop_num}}_{{cash_num}}.csv
One receipt can contain multiple items.
Product categories: household chemicals, textiles, tableware, kitchen appliances, miscellaneous.

Loading data into the database
The load_to_db.py script processes CSV files from the data/ folder and saves the data into the database:
python scripts/load_to_db.py
It skips files that do not match the required format.
After successful upload, files are deleted..

Automation on Windows
For automatic daily execution, you can use Task Scheduler.
Set up a task to run start.bat daily, except Sundays.

Database creation

DDL commands for creating tables are located in the sql/ folder:
receipts: receipt information
items: items in receipts

Logs

The load_to_db.py script creates a log file in the logs/ folder containing processing information and errors.
