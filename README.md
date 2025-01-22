# Django Project with Poetry

This is a Django-based web application that uses [Poetry](https://python-poetry.org/) for dependency management and project packaging.

---

## Prerequisites

Ensure the following are installed on your machine:

1. **Python**
   - Download and install Python 3.13 or higher from the [official Python website](https://www.python.org/downloads/).
   - Verify the installation:
     ```bash
     python --version
     ```
     or
     ```bash
     python3 --version
     ```

2. **Poetry**
   - Install Poetry by running:
     ```bash
     curl -sSL https://install.python-poetry.org | python3 -
     ```
   - Verify the installation:
     ```bash
     poetry --version
     ```
3. **Postgres**
   - Install postgres
     ```bash
     brew install postgresql
     ``` 
   - Start psql
     ```bash
     sudo -i -u postgres
     psql
     ```
   - Create databse
    ```sql
    CREATE DATABASE ecommerce;
    CREATE USER commerceuser WITH PASSWORD 'ecommerpassword';
    GRANT ALL PRIVILEGES ON DATABASE ecommerce TO commerceuser;

    ```
---

## Project Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kirankumbhar/ecommerce.git
   cd ecommerce
   ```

2. **Install Dependencies**
   Run the following command to install all project dependencies:
   ```bash
   poetry install
   ```

3. **Activate the Virtual Environment**
   Poetry automatically manages a virtual environment for your project. Activate it with:
   ```bash
   poetry shell
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project root and add your environment variables. Example:
   ```env
   DEBUG=True
   DB_NAME=ecommerce
   DB_USER=commerceuser
   DB_PASSWORD=ecommerpassword
   ```

   Use the `python-decouple` package to load these variables in your project settings.

5. **Apply Migrations**
   Set up the database schema by running:
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```
   Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to view your application.

---

## Running Tests

Run tests using the Django test runner:
```bash
pytest --cov "." --cov-report html
```


