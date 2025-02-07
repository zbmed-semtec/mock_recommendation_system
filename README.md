# STELLA Integration with the Mock Recommendation System

This repository consists of code for a mock recommendation system designed for internal learning purposes to understand the STELLA architecture and its integration potential for recommendation systems in production and utilizes the RELISH corpus. 


## Developer Documentation

- [STELLA Integration with the Mock Recommendation System](#stella-integration-with-the-mock-recommendation-system)
  - [Developer Documentation](#developer-documentation)
  - [Prequisites : Installing Docker](#prequisites--installing-docker)
  - [Setting up the Mock Recommendation System](#setting-up-the-mock-recommendation-system)
    - [1. Cloning the Repository](#1-cloning-the-repository)
    - [2. Building and Running the Docker Container](#2-building-and-running-the-docker-container)
    - [3. Accessing the System](#3-accessing-the-system)
  - [Setting up STELLA-SERVER](#setting-up-stella-server)
    - [1. Cloning the Repository](#1-cloning-the-repository-1)
    - [2. Building and Running the Docker Container](#2-building-and-running-the-docker-container-1)
    - [3. Initialize the database](#3-initialize-the-database)
    - [4. Register the system](#4-register-the-system)
    - [5. Adding Systems](#5-adding-systems)
    - [6. Check the STELLA Server Database](#6-check-the-stella-server-database)
  - [Setting up STELLA-APP](#setting-up-stella-app)
    - [1. Cloning the Repository](#1-cloning-the-repository-2)
    - [2. Add Datasets](#2-add-datasets)
    - [3. Building and Running the Docker Container](#3-building-and-running-the-docker-container)
    - [4. Initialize the database](#4-initialize-the-database)
    - [5. Index data for the systems](#5-index-data-for-the-systems)
  - [User Query Tracking and Logging](#user-query-tracking-and-logging)




## Prequisites : Installing Docker

To install Docker on an Ubuntu server, follow these steps:

+ Update your existing list of packages:
```
sudo apt update
```

+ Install a few prerequisite packages which let apt use packages over HTTPS:
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```


+ Add the GPG key for the official Docker repository:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```


+ Add the Docker repository to APT sources:
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```


+ Update the package database with the Docker packages:
```
sudo apt update
```


+ Install Docker:
```
sudo apt install docker-ce
```


+ Verify the installation:
```
sudo docker run hello-world
```

------------

## Setting up the Mock Recommendation System
### 1. Cloning the Repository

To set up the Mock Recommendation System, clone the repository from GitHub.

###### Using HTTP:

```
git clone https://github.com/zbmed-semtec/mock_recommendation_system.git
cd mock_recommendation_system
```

###### Using SSH:
Ensure you have set up SSH keys in your GitHub account.

```
git@github.com:zbmed-semtec/mock_recommendation_system.git
cd mock_recommendation_system
```

### 2. Building and Running the Docker Container

To build and start the containers, run the following command:

```
sudo docker compose build
```

```
sudo docker compose up -d
```

To check if the containers are working as required, you could run the following command:

```
sudo docker container ps -a
```

### 3. Accessing the System
Once the system is up and running, you can access it using your web browser at http://localhost:8888/


------------

## Setting up STELLA-SERVER

### 1. Cloning the Repository

Clone the STELLA-SERVER repository from GitHub.

###### Using HTTP:

```
git clone https://github.com/stella-project/stella-server.git
cd stella-server
```
###### Using SSH:
Ensure you have set up SSH keys in your GitHub account.

```
git@github.com:stella-project/stella-server.git
cd stella-server
```

### 2. Building and Running the Docker Container

To build and start the containers, run the following command:

```
sudo docker compose build
```

```
sudo docker compose up -d
```

### 3. Initialize the database

```
sudo docker exec -it stella-server-web-1 /bin/bash
```

Inside the container, run:

```
flask seed-db
```

This will seed the database with users and systems.

### 4. Register the system

1. Access the STELLA Server by navigating to http://localhost:8000.

2. Login with the following credentials:

   -   Username: ```experimenter@stella-project.org```
   -   Password: ```pass```
3. Go to the Systems tab and click on Register Docker System.

4. Register the following systems:

   -   Name: ```mock_rec_base```, URL: ```https://github.com/zbmed-semtec/mock_rec_base```
   -   Name: ```mock_rec_experiment```, URL: ```https://github.com/zbmed-semtec/mock_rec_experiment```

### 5. Adding Systems

1. Login as an admin user:

   - Username: ```admin@stella-project.org```
   - Password: ```pass```

2. Activate the systems in the Systems subpage.

3. Update STELLA-APP through the administration interface:
   -   Go to the *Administration* tab and click on *Update STELLA APP*.

### 6. Check the STELLA Server Database

To verify the newly added systems, connect to the STELLA Server’s database by running:

```
sudo docker exec -it stella-server-db-1 /bin/bash
```

Then connect to the PostgreSQL database:

```
psql -h localhost -p 5432 -U postgres
\c postgres
```

To list all tables, use:

```
\dt
```

To check all running systems, run:

```
select * from systems;
```

This should list all systems currently registered on the STELLA Server.

------------


## Setting up STELLA-APP


### 1. Cloning the Repository

Clone the STELLA-APP repository from GitHub and switch to the **mock_rec_sys** branch.

###### Using HTTP:

```
git clone https://github.com/stella-project/stella-app.git
cd stella-app
git checkout mock_rec_sys
```
###### Using SSH:
Ensure you have set up SSH keys in your GitHub account.

```
git@github.com:stella-project/stella-app.git
cd stella-app
git checkout mock_rec_sys
```

### 2. Add Datasets

Within the data directory, copy the relish datasets. Both the relish_text.jsonl and relish_recoms.jsonl. These files can be found within the ```mock_recommendation_system/data/``` folder

### 3. Building and Running the Docker Container

To build and start the containers, run the following command:

```
sudo docker compose build
```

```
sudo docker compose up -d
```

### 4. Initialize the database

```
sudo docker exec -it stella-app-web-1 /bin/bash
```

Inside the container, run:

```
flask seed-db
```

This will seed the database with users and systems.

### 5. Index data for the systems

   - Access the STELLA APP by navigating to http://localhost:8080
   - Index the data by clicking on the *Index* button next to both the systems


-----------

## User Query Tracking and Logging

- The **mock_recommendation_system** interface is available at http://localhost:8888
- Enter a query using the RELISH corpus data (e.g., PMID: 29302810, 29696019, or 25673835).
- Review the stella-app logs to observe how the app requests rankings from both systems:
  
```
sudo docker logs stella-app-web-1
```

- Check the stella-app database to ensure rankings and sessions are being generated.

- To verify the newly added systems, connect to the STELLA App’s database by running:

```
sudo docker exec -it stella-app-db-1 /bin/bash
```

Then connect to the PostgreSQL database:

```
psql -h localhost -p 5430 -U postgres
\c postgres
```

To list all tables, use:

```
\dt
```

To check the results, run:

```
select * from results;
```

- Click on a document to view its details and recommendations for related documents.
- Check the stella-app database for feedback entries, which include session click data:
```
select * from feedbacks;
```

- Logs are eventually transferred to the stella-server and displayed in the simple dashboard. This can be viewed by connecting to the STELLA Server Database
- Navigate to the dashboard tab on the STELLA Server and select the system to view its stats. 
