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

# Start Docker Compose in the background
Start-Process -NoNewWindow -FilePath "docker" -ArgumentList "compose up" 

$AppCid = ""
while (-not $AppCid) {
    Start-Sleep -Seconds 1
    $AppCid = docker compose ps -q demo-app
}

# Wait for the container to exit
docker wait $AppCid

# Shut down the stack
docker compose down
