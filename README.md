# Description

An e-learning platform for educational groups.

This web app was made using Django for backend, JS/HTML/CSS for frontend.

# How To Run

Clone the repository and run the Django app using python manage.py runserver (assuming you have django installed).

There will be an admin account which has a username of "admin" and a password of "adminpass" (all the other accounts are deleted from the database).

### **IMPORTANT**: Before running the website you need to go to settings.py and uncomment the emailing settings and insert the email you want to send the verification email from in the EMAIL_FROM variable and the EMAIL_HOST_USER variable and the app password in the EMAIL_HOST_PASSWORD variable.

**To make an app password for the above step** you need to go to account settings for your google account and go to security and enable 2-step verification. Then you'll find app passwords. Create one and paste in the EMAIL_HOST_PASSWORD variable in settings.py.



