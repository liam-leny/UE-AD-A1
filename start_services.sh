#!/bin/bash

# Start the GraphQL service
echo "Starting the GraphQL movie service..."
python3 movie/movie.py &

# Start the REST service
echo "Starting the REST user service..."
python3 user/user.py &

# Start the first gRPC service (booking)
echo "Starting the gRPC booking service..."
python3 booking/booking.py &

# Start the second gRPC service (showtime)
echo "Starting the gRPC showtime service..."
python3 showtime/showtime.py &

wait

