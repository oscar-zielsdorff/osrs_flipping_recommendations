# OSRS Flipping Recommendations
This script generates a .xlsx file populated with items recommended to flip for profit. Different settings and filters can be modified within the script under the **Filters** section. The file is populated with opinionated default settings that may be good for earning a profit.

## Requirements
1. Python3 is installed.

## Setup
1. Clone the repository.
2. Open a terminal in the project directory (where `ge_items.py` is).
3. (Optionally) Create a virtual environment for dependency management.
    1. Run `python3 -m venv my_venv` to create the venv.
    2. Activate the venv by running one of the activate scripts (this varies depending on your OS / terminal shell):
        * **Linux:** `source my_venv/bin/activate`
        * **PowerShell:** `.\my_venv\bin\Activate.ps1`
4. Run `pip install -r requirements.txt` to install the necessary dependencies.

## Using the Script
1. Open a terminal in the project directory (where `ge_items.py` is).
2. Run `python3 ge_items.py` to execute the script.
3. Open the generated .xlsx file.

## Modifying the Filters
The filters can be toggled or changed by opening the script in a text editor and scrolling to the labeled ***Filters*** section. After saving your changes run the script again to generate a new table.