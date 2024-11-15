#!/bin/bash

# Lancer le service GraphQL
echo "Lancement du service GraphQL movie..."
python3 movie/movie.py &

# Lancer le service REST
echo "Lancement du service REST user..."
python3 user/user.py &

# Lancer le premier service gRPC (movie)
echo "Lancement du service gRPC movie..."
python3 movie/movie.py &

# Lancer le second service gRPC (showtime)
echo "Lancement du service gRPC showtime..."
python3 showtime/showtime.py &

# Attendre que tous les services se terminent (facultatif)
wait
