# MUTUAL FUNDS ACCOUNT SYSTEM 

This guide will help you set up a MUTUAL FUNDS ACCOUNT SYSTEM on your system.
## Prerequisites

- Basic knowledge of python and Django Rest Framework.

## Setup Steps

Follow these steps to configure the project,

---

### Step 1: Setup Virtual Environment

1. **Setup Virtual Env**  
   

   ```bash
   python -m venv mfas_env

   source mfas_env/bin/activate

2.  **Clone the project from the github** 
 

    ```bash 
    git clone githubv://link

- After you clone the project now simply. Do these tasks.

    ```bash
    pip install -r requirements.txt

    # Migrate tables on database
    ```bash
    python manage.py migrate



3.  **Create the superuser** 
    Create a admin 

    ```bash
    python manage.py createsuperuser

4.  **Test the Server** 

    Simply run the project by

    ```bash
    python manage.py runserver 

    Go to your any web browser and test

    ```bash
    http://localhost:8000





