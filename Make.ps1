# Load environment variables from .env file if it exists
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^#][^=]+)=(.*)$") {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
} else {
    Write-Warning ".env file not found, see .env.example for reference"
}

function Setup {
    Write-Host "Setting up Python environment and installing packages..."
    uv sync --group dev
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    
    exit $LASTEXITCODE
}

function Format {
    Write-Host "Formatting code with ruff..."
    if (Test-Path ".venv") {
        .\.venv\Scripts\Activate.ps1
    }
    ruff format .
    exit $LASTEXITCODE
}

function RunTests {
 uv run pytest
 exit $LastExitCode
}

switch ($Args[0]) {
    'setup' { Setup }
    'format' { Format }
    'run-tests' { RunTests }
    default { 
        Write-Host "Available commands: setup, add-crs, format"
        Write-Host "Usage: .\Make.ps1 <command>"
    }
}

