# Department Management Mini System (DMMS)

*DMMS is made for EPAM Python Course Graduation Work*

To run this application you need:
1. git clone this repo
2. Set up MySQL database:  
For Ubuntu run this commands:
   * sudo apt-get update
   * sudo apt-get install mysql-server
   * sudo mysql -u root  
   Inside MySQL client:
       * CREATE USER 'manager_user'@'%' IDENTIFIED BY 'hard_password1234';
       * GRANT ALL PRIVILEGES ON *.* TO 'manager_user'@'%';
       * CREATE DATABASE company_db;
       * CREATE DATABASE test_company_db;
3. In repository:
    * pip install -r requirements.txt
    * gunicorn --bind localhost:5000 dmms.wsgi:app_rest
    * gunicorn --bind localhost:5001 dmms.wsgi:app_views
4. Go to localhost:5001 in your web browser and enjoy this project :)
