#!/bin/bash

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -aq)

# Remove all containers
echo "Removing all containers..."
docker rm $(docker ps -aq)

# Remove all images
echo "Removing all images..."
docker rmi -f $(docker images -q)

# Remove all volumes
echo "Removing all volumes..."
docker volume rm $(docker volume ls -q)

# Remove all networks
echo "Removing all networks..."
docker network rm $(docker network ls -q)

# Remove Docker build cache
echo "Removing Docker build cache..."
docker builder prune -f

# Optional: Remove all dangling volumes
echo "Removing dangling volumes..."
docker volume prune -f

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -aq)

# Remove all containers
echo "Removing all containers..."
docker rm $(docker ps -aq)

# Remove all images
echo "Removing all images..."
docker rmi -f $(docker images -q)

# Remove all volumes
echo "Removing all volumes..."
docker volume rm $(docker volume ls -q)

# Remove all networks (excluding default ones)
echo "Removing all networks..."
docker network prune -f

# Remove Docker build cache
echo "Removing Docker build cache..."
docker builder prune -f

# Optional: Remove any remaining dangling volumes
echo "Removing dangling volumes..."
docker volume prune -f

# Optional: Remove dangling images (untagged images)
echo "Removing dangling images..."
docker image prune -f

# Optional: Remove dangling containers (exited but not removed)
echo "Removing dangling containers..."
docker container prune -f

echo "Docker cleanup completed."
