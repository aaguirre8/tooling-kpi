# tooling-kpi
Tooling TAM5 KPIs


## Get started
1. Create and source conda env
```bash
$ conda env create -f environment.yml
$ conda activate toolingdev
```

2. Install requirements
```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

## Technologies used
- Database: postgres
- Data framework:
    - pandas
    - openpyxl
- Frontend framework: streamlit


## Requirements
1. PostgreSQL installed.


## Known issues
1. Duplicated work orders caused change of technician assigned to the order.
    Logic TBD.