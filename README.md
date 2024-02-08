# IMI8


# Flask Registration App

This is a simple Flask application for user registration with **MySQL database** integration. Used simple HTML and CSS for frontend.

## How to Run

1. Clone the repository:

    ```bash
    git clone https://github.com/Janesh7/IMI8.git
    ```

2. Navigate to the project directory:

    ```bash
    cd IMI8/Registration
    ```

3. Install Flask and other dependencies:

    ```bash
    pip install Flask mysql-connector-python
    ```

4. Ensure you have **MySQL server installed and running.** Modify the `db_config` dictionary in `app.py` to match your MySQL server configuration, including the **database name, username, and password.**

    **NOTE: Dont forget to change the password**

5. Create the database and table by running the following SQL commands:

    ```sql
    CREATE DATABASE IF NOT EXISTS `test` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    USE `test`;
    CREATE TABLE IF NOT EXISTS `registration` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `username` VARCHAR(50) NOT NULL,
      `email` VARCHAR(100) NOT NULL,
      `phoneNumber` VARCHAR(20),
      `address` VARCHAR(255),
      `DateOfBirth` DATE NOT NULL,
      `CreatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      `UpdatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ```

6. Run the Flask application:

    ```bash
    python app.py
    ```

7. Access the application in your web browser at `http://localhost:5000`.

## Functionality

### Register

- Users can register by providing their username, email, phone number, address, and date of birth.
- Input validation is performed for each field to ensure data integrity and prevent malicious input:
    - **Username**: Must contain only characters and numbers.
    - **Email**: Must have a valid email format.
    - **Phone number**: Must contain exactly 10 digits.
    - **Date of Birth**: Must be in the past (not greater than the current date).
- **Duplicate username checks** are performed to prevent duplicate registrations.
- Flash messages are used to display error messages to users in case of validation failures or database errors.

### Display

- This route displays a list of registered users fetched from the MySQL database, **including date of creation and updation**.
- Users can filter the list based on specific criteria such as username or email.
- You need to type in the **search bar and select the field using the drop down** to filter.

### Update

- Users can update their registration information by providing their username and new details.
- Input validation is performed for all fields to ensure data integrity and prevent malicious input similar to register module.
- A **valid username** is required to update the fields
- Flash messages are used to display error messages to users in case of validation failures or database errors.

### Delete

- Users can delete their registration by providing their username.
- **Valid username** is required to delete an entry from the table. 
- Flash messages are used to display success messages or error messages if the user does not exist.

---

