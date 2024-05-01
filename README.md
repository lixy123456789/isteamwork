### Smart Loading Installation and Usage Guide

Welcome to the Smart Loading GitHub repository! This application leverages PHP and Python to optimize container loading processes. It integrates a PHP-based web interface with a Python Flask backend to calculate and display optimal loading strategies.

#### Prerequisites
Before beginning the installation, ensure you have the following installed on your system:
- **Git**: Version control system to clone the repository.
- **PHP**: Version 7.4 or higher.
- **Python**: Version 3.8 or higher.
- **Flask: Python framework required to run the backend. Install using pip install flask.
- **XAMPP** or any similar server software that supports PHP.

#### Installation Steps

**Step 1: Cloning the Repository**
To get a copy of the Smart Loading project on your local machine, open a terminal or command prompt and run the following command:

```sh
git clone https://github.com/yancey7521/isteamwork.git
```

This command clones the repository and creates a directory named `smart-loading` in your current working directory.

**Step 2: Navigating to the Project Directory**
Change your directory to the newly created project directory:

```sh
cd smart-loading
```

**Step 3: Setting Up the Server Environment**
1. Install XAMPP or another PHP server environment.
2. Ensure that the PHP and Apache modules are running.
3. Copy the `smart-loading` directory into the `htdocs` folder of your XAMPP installation.

**Step 4: Starting the Servers**

- **PHP Server:**
  - Access `project_irs.php` through your web browser by navigating to:
    ```plaintext
    http://localhost/smart-loading/project_irs.php
    ```
  - This page is used for managing item data and generating container loading plans.

- **Python Flask Server:**
  - Open a command prompt or terminal in the project directory.
  - Run the following command to start the Flask server:
    ```sh
    python app.py
    ```
  - Ensure the Flask application is running to handle backend requests made by `project_irs.php`.

#### Usage Guide
After setting up the application, follow these steps to use Smart Loading:

1. **Adding Items:**
   - Go to `http://localhost/smart-loading/project_irs.php` in your web browser.
   - Use the provided form to input details of the items to be loaded into containers (length, width, height, weight, color, quantity).
   - Click "Add Item" to store the item in the session. Items will be displayed in a table with an option to delete any item.

2. **Generating Container Loading Plan:**
   - After adding all necessary items, click "Generate Container Loading Plan."
   - This sends the item data as a JSON payload via a POST request to the Flask server (`app.py`), which processes the request and returns an optimized loading configuration.
   - The PHP script then visualizes this configuration on the webpage, displaying how items are arranged within the container.

#### Contact
If you have any questions, feedback, or collaboration opportunities, we'd love to hear from you. Feel free to reach out to the project maintainers:

   - Li Xinye: A0230455M
   - Jantje Jupieter Tanuwidjaja: A0292396N
   - Suhardiman Agung: A0291911E
Let's revolutionize container logistics together with Smart Loading! 🚢📦🌟

#### Support
If you encounter any issues or have questions regarding the installation or usage of Smart Loading, please contact the project maintainers or open an issue on this GitHub repository.

#### Thank You
Thank you for choosing Smart Loading. We hope this guide helps you set up and enjoy using the system to its full potential. Your feedback and contributions are welcome!