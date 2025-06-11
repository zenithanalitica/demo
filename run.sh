#!/bin/bash
set -e

# Clone or pull latest changes
clone_or_pull() {
  repo_url=$1
  target_dir=$2

  if [ -d "$target_dir/.git" ]; then
    echo "Updating $target_dir..."
    git -C "$target_dir" pull
  else
    echo "Cloning $repo_url into $target_dir..."
    git clone "$repo_url" "$target_dir"
  fi
}

# Define repo URLs
clone_or_pull https://github.com/zenithanalitica/data-pipeline data-pipeline
clone_or_pull https://github.com/zenithanalitica/sentiment-score sentiment-score

# Set env vars
export NEO4J_URI="neo4j:7687"
export NEO4J_USERNAME=neo4j
export NEO4J_PASSWORD=verycomplicatedpassword
export NEO4J_AUTH="${NEO4J_USERNAME}/${NEO4J_PASSWORD}"

# Recognize if nvidia driver is availabe
if nvidia-smi &> /dev/null ; then
  NVIDIA=true
else
  NVIDIA=false
fi

# Run docker compose
if $NVIDIA; then
  docker compose --profile gpu up &
  APP_NAME="demo-app-gpu"
else
  docker compose --profile cpu up &
  APP_NAME="demo-app-cpu"
fi

# Wait for demo-app container to be running
APP_CID=""
while [ -z "$APP_CID" ]; do
  sleep 1
  APP_CID=$(docker-compose ps -q $APP_NAME)
done

# Wait for the app container to exit
docker wait $APP_CID

# Shut down the rest of the stack
docker-compose down
