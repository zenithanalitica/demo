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

# Recognize if nvidia driver is availabe
$NVIDIA = $false
if (Get-Command /Windows/System32/nvidia-smi -ErrorAction SilentlyContinue) {
    $null = & /Windows/System32/nvidia-smi 2>$null
    if ($LASTEXITCODE -eq 0) {
        $NVIDIA = $true
    }
}

# Run docker compose with appropriate profile
if ($NVIDIA) {
    docker compose --profile gpu up -d
    $APP_NAME = "demo-app-gpu"
} else {
    docker compose --profile cpu up -d
    $APP_NAME = "demo-app-cpu"
}

# Wait for demo-app container to be running
$APP_CID = ""
while (-not $APP_CID) {
    Start-Sleep -Seconds 1
    $APP_CID = docker compose ps -q $APP_NAME
}

# Wait for the container to exit
docker wait $AppCid

# Shut down the stack
docker compose down
