# Exit immediately if a command fails
$ErrorActionPreference = "Stop"

# Function to clone or pull the latest changes
function Clone-OrPull {
    param (
        [string]$RepoUrl,
        [string]$TargetDir
    )

    if (Test-Path "$TargetDir\.git") {
        Write-Host "Updating $TargetDir..."
        git -C $TargetDir pull
    } else {
        Write-Host "Cloning $RepoUrl into $TargetDir..."
        git clone $RepoUrl $TargetDir
    }
}

# Clone or pull repositories
Clone-OrPull -RepoUrl "https://github.com/zenithanalitica/data-pipeline" -TargetDir "data-pipeline"
Clone-OrPull -RepoUrl "https://github.com/zenithanalitica/sentiment-score" -TargetDir "sentiment-score"

# Set environment variables
$env:NEO4J_URI = "neo4j:7687"
$env:NEO4J_USERNAME = "neo4j"
$env:NEO4J_PASSWORD = "verycomplicatedpassword"
$env:NEO4J_AUTH = "$($env:NEO4J_USERNAME)/$($env:NEO4J_PASSWORD)"

# Run Docker Compose
docker compose up --exit-code-from app
