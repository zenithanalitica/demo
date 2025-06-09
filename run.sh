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

# Run docker compose
docker compose up
