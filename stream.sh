#!/bin/bash
# Script to restart container with updated .env file
# Kills the process and recreates the container

CONTAINER_NAME="youtube-stream"

echo "Checking container status..."
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container $CONTAINER_NAME does not exist. Creating new container..."
    docker run -d \
      --name $CONTAINER_NAME \
      --env-file .env \
      --restart unless-stopped \
      imvickykumar999/youtube-stream:latest
    docker ps | grep $CONTAINER_NAME
    exit 0
fi

echo "Getting PID of running container..."
PID=$(docker inspect $CONTAINER_NAME --format='{{.State.Pid}}' 2>/dev/null)
STATUS=$(docker inspect $CONTAINER_NAME --format='{{.State.Status}}' 2>/dev/null)

if [ "$STATUS" != "running" ]; then
    echo "Container is not running (status: $STATUS). Removing and recreating..."
    docker rm $CONTAINER_NAME 2>/dev/null
    docker run -d \
      --name $CONTAINER_NAME \
      --env-file .env \
      --restart unless-stopped \
      imvickykumar999/youtube-stream:latest
    docker ps | grep $CONTAINER_NAME
    exit 0
fi

if [ -z "$PID" ] || [ "$PID" = "0" ]; then
    echo "Warning: Could not get valid PID, but container appears running. Trying to stop normally..."
    docker stop $CONTAINER_NAME 2>/dev/null
    docker rm $CONTAINER_NAME 2>/dev/null
    docker run -d \
      --name $CONTAINER_NAME \
      --env-file .env \
      --restart unless-stopped \
      imvickykumar999/youtube-stream:latest
    docker ps | grep $CONTAINER_NAME
    exit 0
fi

echo "Container PID: $PID"
echo "Disabling restart policy..."
docker update --restart no $CONTAINER_NAME 2>/dev/null

echo "Killing process $PID..."
sudo kill -9 $PID

echo "Waiting for process to die..."
sleep 3

echo "Removing container..."
docker rm $CONTAINER_NAME

echo "Creating new container with updated .env..."
docker run -d \
  --name $CONTAINER_NAME \
  --env-file .env \
  --restart unless-stopped \
  imvickykumar999/youtube-stream:latest

echo "Verifying container status..."
sleep 2
docker ps | grep $CONTAINER_NAME

echo ""
echo "✅ Container restarted successfully with updated .env file!"

