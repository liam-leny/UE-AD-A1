# TP MIXTE - UE Architectures distribuées A1

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

The **TP MIXTE - UE Architectures distribuées A1** project is a distributed application consisting of several services for managing movies, showtimes, bookings, and users in a cinema. This application uses mixed APIs, including **GraphQL** for some services and **REST** for the **User** service API, while the other services communicate via **gRPC**.

## Project Goal

The main goal of this project is to build a set of **microservices** to simulate a cinema movie and booking management platform. The application consists of four independent services, each responsible for a different part of the system.

## Microservices

### Movie

This microservice is responsible for managing movies. It contains a small JSON database listing the movies available in the cinema, with information such as title, description, genre, etc. It exposes a **GraphQL** API to allow users to retrieve information about the movies.

### Times

This service manages the showtimes of the movies. It contains a JSON database with the dates and the movies available on those dates. **Times** provides a gRPC API that other services can query to get the available movie showtimes.

### Booking

This microservice allows users to book movies. It contains a JSON database with the users' bookings. The **Booking** service interacts with **Times** to verify that the selected showtimes are valid, as it does not directly know the showtimes. It exposes a gRPC API for managing bookings.

### User

The **User** microservice is the entry point for users. It manages the user database, containing information such as user ID and their bookings. **User** interacts with **Booking** to allow users to make reservations and with **Movie** to provide information about available movies. This service exposes a **REST** API to manage users and their interactions with other services.

## Overall Functionality

The application allows a user to:

1. View the list of available movies via the **Movie** service.
2. See the movie showtimes via the **Times** service.
3. Make a booking for a movie via the **Booking** service.
4. Manage their user account via the **User** service.

## Architecture

The architecture of the project relies on **independent microservices** that communicate with each other through mixed APIs:

- **GraphQL** is used for interactions with movies in the **Movie** service.
- **gRPC** is used for communication between the **Times**, **Booking**, and **User** services to ensure fast and efficient exchanges.
- **REST** is used in the **User** service for simpler management of users and their interactions with other services.

The services are designed to run independently, each managing its own data storage in the form of JSON files. There is no use of Docker containers in this project.

Here is the translated version in English:

## Project Directory Structure

Here is the directory structure of the project:

```
.
├── booking
│   ├── booking
│   ├── booking_pb2_grpc.py
│   ├── booking_pb2.py
│   ├── booking.py
│   ├── data
│   │   └── bookings.json
│   ├── Dockerfile
│   ├── protos
│   │   ├── booking.proto
│   │   └── showtime.proto
│   ├── __pycache__
│   ├── requirements.txt
│   ├── showtime_pb2_grpc.py
│   ├── showtime_pb2.py
│   └── UE-archi-distribuees-Booking-1.0.0-resolved.yaml
├── docker-compose.yml
├── LICENSE
├── movie
│   ├── data
│   │   ├── actors.json
│   │   └── movies.json
│   ├── Dockerfile
│   ├── movie.graphql
│   ├── movie.py
│   ├── __pycache__
│   ├── requirements.txt
│   ├── resolvers.py
│   ├── UE-archi-distribuees-Movie-1.0.0-resolved.yaml
│   └── venv
├── README.md
├── requirements.txt
├── showtime
│   ├── data
│   │   └── times.json
│   ├── Dockerfile
│   ├── protos
│   │   └── showtime.proto
│   ├── __pycache__
│   ├── requirements.txt
│   ├── showtime_pb2_grpc.py
│   ├── showtime_pb2.py
│   ├── showtime.py
│   └── UE-archi-distribuees-Showtime-1.0.0-resolved.yaml
├── start_services.sh
├── user
│   ├── booking_pb2_grpc.py
│   ├── booking_pb2.py
│   ├── data
│   │   └── users.json
│   ├── Dockerfile
│   ├── protos
│   │   └── booking.proto
│   ├── __pycache__
│   ├── requirements.txt
│   └── user.py
└── venv
    ├── bin
    ├── lib
    └── pyvenv.cfg
```

## Features

- **User**

| Method | Description                                                            | URL                                                            |
| ------ | ---------------------------------------------------------------------- | -------------------------------------------------------------- |
| GET    | Home page. Displays a welcome message.                                 | http://localhost:3203/                                         |
| GET    | Retrieve all reservations for a specific user by their `userId`.       | http://localhost:3203/users/{userId}/reservations              |
| GET    | Retrieve all movies associated with a user's reservations.             | http://localhost:3203/users/{userId}/movies                    |
| POST   | Check the availability of a reservation for a specific date and movie. | http://localhost:3203/users/{userId}/reservations/availability |
| PUT    | Update a specific user's information by their `userId`.                | http://localhost:3203/users/{userId}                           |
| DELETE | Delete a specific user by their `userId`.                              | http://localhost:3203/users/{userId}                           |

- **Movie**

| Method  | Description                                      | URL / Method                            |
| ------- | ------------------------------------------------ | --------------------------------------- |
| GraphQL | Home page. Displays a welcome message.           | http://localhost:3200/                  |
| GraphQL | Retrieve all movies.                             | Query: `all_movies`                     |
| GraphQL | Retrieve a movie by its ID.                      | Query: `movie_with_id`                  |
| GraphQL | Retrieve a movie by its title.                   | Query: `movie_with_title`               |
| GraphQL | Retrieve movies directed by a specific director. | Query: `movie_with_director`            |
| GraphQL | Retrieve movies with a specific rating.          | Query: `movie_with_rating`              |
| GraphQL | Update the rating of a movie.                    | Mutation: `update_movie_rate`           |
| GraphQL | Add a new movie.                                 | Mutation: `add_movie`                   |
| GraphQL | Delete a movie.                                  | Mutation: `delete_movie`                |
| GraphQL | Retrieve the list of actors in a movie.          | Field Resolver: `actors` within `Movie` |

- **Showtime**

| Method | Description                                                                           | Method                         |
| ------ | ------------------------------------------------------------------------------------- | ------------------------------ |
| gRPC   | Retrieve all showtimes available in the schedule.                                     | `/Showtime/GetShowtimes`       |
| gRPC   | Retrieve showtimes for a specific date. Returns NOT_FOUND if the date is unavailable. | `/Showtime/GetShowtimesByDate` |

- **Booking**

| Method | Description                                                                                     | Method                        |
| ------ | ----------------------------------------------------------------------------------------------- | ----------------------------- |
| gRPC   | Retrieve booking details by user ID. Returns NOT_FOUND if the user ID is unavailable.           | `/Booking/GetBookingByUserID` |
| gRPC   | Add a new booking for a user. Checks movie availability via the Showtime service before adding. | `/Booking/AddBooking`         |
| gRPC   | Retrieve all bookings in the database.                                                          | `/Booking/GetAllBookings`     |

## Launching All Services

To launch all services simultaneously, you can use the `start_services.sh` script located at the root of the project. Run the following command at the root of the project:

```bash
./start_services.sh
```

This command will start all the services in the background, running them simultaneously so that the application functions correctly.

## Authors

- **Liam LE NY**
- **Camille GOUAULT--LAMOUR**
- **Hélène COULLON**
