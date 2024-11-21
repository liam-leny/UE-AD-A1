# TP REST - UE Architectures distribuées A1

## Table of Contents

- [Description](#description)
- [Project Goal](#project-goal)
- [Microservices](#microservices)
  - [Movie](#movie)
  - [Times](#times)
  - [Booking](#booking)
  - [User](#user)
- [Overall Functionality](#overall-functionality)
- [Architecture](#architecture)
- [Project Directory Structure](#project-directory-structure)
- [Features](#features)
- [Launching All Services](#launching-all-services)
- [Authors](#authors)

## Description

The **TP REST - UE Architectures distribuées A1** project is a distributed application consisting of several services for managing movies, showtimes, bookings, and users in a cinema. This application uses **REST APIs** for all its microservices, providing a unified interaction model.

## Project Goal

The main goal of this project is to build a set of **microservices** to simulate a cinema movie and booking management platform. The application consists of four independent services, each responsible for a different part of the system.

## Microservices

### Movie
This microservice is responsible for managing movies. It contains a small JSON database listing the movies available in the cinema, with information such as title, description, genre, etc. It exposes a **REST API** to allow users to retrieve and manage information about movies.

### Times
This service manages the showtimes of the movies. It contains a JSON database with the dates and the movies available on those dates. **Times** provides a **REST API** to allow querying available showtimes.

### Booking
This microservice allows users to book movies. It contains a JSON database with the users' bookings. The **Booking** service interacts with **Times** to verify that the selected showtimes are valid. It exposes a **REST API** for managing bookings.

### User
The **User** microservice is the entry point for users. It manages the user database, containing information such as user ID and their bookings. **User** interacts with **Booking** to allow users to make reservations and with **Movie** to provide information about available movies. This service exposes a **REST API** to manage users and their interactions with other services.

## Overall Functionality

The application allows a user to:
1. View the list of available movies via the **Movie** service.
2. See the movie showtimes via the **Times** service.
3. Make a booking for a movie via the **Booking** service.
4. Manage their user account via the **User** service.

## Architecture

The architecture of the project relies on **independent microservices** that communicate with each other through REST APIs:
- All microservices expose their functionality through REST endpoints for simple and accessible interactions.

The services are designed to run independently, each managing its own data storage in the form of JSON files.

## Project Directory Structure

Here is the directory structure of the project:

```
.
├── booking
│   ├── booking.py
│   ├── databases
│   │   └── bookings.json
│   ├── Dockerfile
│   ├── requirements.txt
│   └── UE-archi-distribuees-Booking-1.0.0-resolved.yaml
├── docker-compose.yml
├── LICENSE
├── movie
│   ├── databases
│   │   └── movies.json
│   ├── Dockerfile
│   ├── movie.py
│   ├── requirements.txt
│   ├── templates
│   └── UE-archi-distribuees-Movie-1.0.0-resolved.yaml
├── README.md
├── requirements.txt
├── showtime
│   ├── databases
│   │   └── times.json
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── showtime.py
│   └── UE-archi-distribuees-Showtime-1.0.0-resolved.yaml
├── start_services.sh
├── user
│   ├── databases
│   │   └── users.json
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── UE-archi-distribuees-User-1.0.0-resolved.yaml
│   └── user.py
└── venv
    ├── bin
    ├── lib
    └── pyvenv.cfg
```

## Features

- **User**

| Method  | Endpoint                              | Description                                                                                     |
|---------|---------------------------------------|-------------------------------------------------------------------------------------------------|
| **GET** | `/`                                   | Home page. Displays a welcome message.                                                         |
| **GET** | `/users/<userId>/reservations`        | Retrieves all reservations for a specific user by their user ID.                               |
| **GET** | `/users/<userId>/movies`              | Retrieves detailed movie information for all reservations of a specific user.                  |
| **PUT** | `/users/<userId>`                     | Updates information for a specific user. Validates that the user exists and updates the fields provided. |
| **DELETE** | `/users/<userId>`                  | Deletes a specific user by their user ID.                                                      |

- **Movie**

| Method  | Endpoint                           | Description                                                          |
|---------|------------------------------------|----------------------------------------------------------------------|
| **GET** | `/`                                | Home page. Displays a welcome message.                               |
| **GET** | `/template`                        | Renders an HTML template for the Movie service.                      |
| **GET** | `/json`                            | Retrieves the complete list of movies in JSON format.                |
| **GET** | `/movies/<movieid>`                | Retrieves a specific movie by its ID.                                |
| **GET** | `/moviesbytitle`                   | Retrieves a specific movie by its title using a query parameter.     |
| **GET** | `/moviesbydirector`                | Retrieves all movies by a director using a query parameter.          |
| **GET** | `/moviesbyrating`                  | Retrieves all movies with a rating greater than or equal to the given value. |
| **POST**| `/addmovie/<movieid>`              | Adds a new movie to the database using its ID.                       |
| **PUT** | `/movies/<movieid>/<rate>`         | Updates the rating of a movie identified by its ID.                  |
| **DELETE**| `/movies/<movieid>`              | Deletes a movie by its ID.                                           |
| **GET** | `/help`                            | Lists all available API endpoints with their descriptions.           |

- **Showtime**

| Method  | Endpoint                 | Description                                                          |
|---------|--------------------------|----------------------------------------------------------------------|
| **GET** | `/`                      | Home page. Displays a welcome message.                               |
| **GET** | `/showtimes`             | Retrieves the complete showtime schedule in JSON format.             |
| **GET** | `/showmovies/<date>`     | Retrieves the showtime schedule for a specific date.                 |

- **Booking**

| Method  | Endpoint                | Description                                                                                 |
|---------|-------------------------|---------------------------------------------------------------------------------------------|
| **GET** | `/`                     | Home page. Displays a welcome message.                                                     |
| **GET** | `/bookings`             | Retrieves the complete list of bookings in JSON format.                                     |
| **GET** | `/bookings/<userid>`    | Retrieves bookings for a specific user by their user ID.                                    |
| **POST**| `/bookings/<userid>`    | Adds a new booking for a user. Validates date and movie availability via the Showtime service.|

## Launching All Services

Before launching all services, ensure you have set up a virtual environment and installed the required dependencies. Run the following commands at the root of the project:

```bash
# Create a virtual environment
virtualenv ./venv

# Activate the virtual environment
source ./venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

Once the environment is ready, you can launch all services simultaneously using the `start_services.sh` script located at the root of the project:

```bash
./start_services.sh
```

This command will start all the services in the background, running them simultaneously so that the application functions correctly.

## Authors

- **Liam LE NY**
- **Camille GOUAULT--LAMOUR**
- **Hélène COULLON**
