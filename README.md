# house_hold_service
Household Services Application
It is a multi-user app (requires one admin and other service professionals/ customers) which acts as platform for providing comprehensive home servicing and solutions.

Frameworks to be used
These are the mandatory frameworks on which the project has to be built.


Flask for application code
Jinja2 templates + Bootstrap for HTML generation and styling
SQLite for data storage

Note: All demos should be possible on your local machine.

Roles
The platform will have three roles;


Admin - root access - it is a superuser of the app and requires no registration.

Admin login redirects to the admin dashboard
Admin will monitor all the users (customers/service professionals)
Admin will create a new service with a base price
Admin will approve a service professional after verification of profile docs
Admin will block customer/service professionals based on fraudulent activity/poor reviews
Other operations*

Service Professional - An individual that provides the service

Login/Register
Service professionals will accept/reject a request
Each professional may have;
ID
Name
Date created
Description
service_type
Experience
etc.
One professional is good at one of the services only
He/she can accept/reject an assigned service request
Professional profiles are visible based on customer reviews
The professional will exit the location after the service is closed by the customer

Customer - an individual who has to book a service request

Login/Register
View/Search the service by the name/location pin code
Open/close a service request
He/she can post reviews/remarks on the closed service
Others
Terminologies

Service - It refers to the type of service that the customer is looking for e.g. AC servicing, plumbing etc.


Each service may have;

ID
Name
Price
Time required
Description etc.

Service Request - A customer creates a service request providing the type of service the customers is looking for, when is it required etc.

A service request may contain the following attributes:

id - primary key
service_id(foreign key-services table)
customer_id(foreign key-customer table)
professional_id(foreign key-professional table)
date_of_request
date_of_completion
service_status(requested/assigned/closed)
remarks (if any) etc.

Note: the above fields are not exhaustive, students can add more fields a/c to their requirements

Application Wireframe
A-Z Household Services

 

Note: The wireframe is provided only to get the flow of the application and what should appear when a specific user navigates from one page to another. It is NOT mandatory to exactly replicate the views given in the wireframe. Students can work on their front-end ideas.

Core Functionalities
1 Admin login and user login

 

A login/register form with fields like username, password etc. for customer, service professional and admin login
You can create separate forms for each type of user
You can either use a proper login framework, or just use a simple HTML form with username and password (we are not concerned with how secure the login or the app is)
The app must have a suitable model to store and differentiate all the types of user of the app.

2. Admin Dashboard - for the Admin


Admin login redirects to admin dashboard
Admin will manage all the users (customers/service professional)
Admin will approve a service professional after verification of profile docs
Admin will block customer/service professional based on fraudulent activity/poor reviews

3. Service Management - for the Admin


Create a new service with a base price.
Update an existing service - e.g. name, price, time_required and/or other fields
Delete an existing service

4. Service Request - for the customers


Create a new service request based on the services available
Edit an existing service request - e.g. date_of_request, completion status, remarks etc
Close an existing service request.

5. Search for available services


The customers should be able to search for available services based on their location, name, pin code etc.
The admin should be able to search for a professional to block/unblock/review them.

6. Take action on a particular service request - for the service professional


Ability to view all the service requests from all the customers
Ability to accept/reject a particular service request
Ability to close the service request once completed*
