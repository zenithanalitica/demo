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

# Run docker compose
docker compose up --exit-code-from app
