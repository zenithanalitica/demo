# Project Setup and Running

## Prerequisites

- **[Docker](with https://docs.docker.com/get-docker/)** (Docker Compose ≥ 2.0)
- **[Git](https://git-scm.com/)**
- **[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)**  (*Optional — significantly speeds up sentiment score calculation*)
- **[uv](https://docs.astral.sh/uv/)**  (*Only needed if running without Docker — see [Using an Existing Database](#using-an-existing-database)*)

> [!NOTE]
> **Windows Users (GPU Support)**  
> Refer to [Docker GPU support documentation](https://docs.docker.com/desktop/features/gpu/) if using GPU acceleration.

---

## Running

### 1. Clone the Repository

```bash
git clone https://github.com/zenithanalitica/demo/
cd demo/
````

### 2. Add the Data Files

Place the unzipped data files in the project root so the structure looks like:

```
|
|- data/
|    |- airlines-15....json
|    |- airlines-15....json
|    |- ...
|- demo/
|- run.sh
|- run.ps1
```

### 3. Run the Script

#### On **Linux/macOS**:

Make the script executable and run it:

```bash
chmod +x run.sh
./run.sh
```

#### On **Windows**:

Run the PowerShell script:

```powershell
.\run.ps1
```

> You may need to bypass execution policy:
> `powershell -ExecutionPolicy Bypass -File run.ps1`

---

## Using an Existing Database
> [!WARNING]
> The program expects the database to be already populated with sentiment score calculated

To run the demo without importing data:

1. Create a `.env` file in the project root directory with:

```
NEO4J_URI=your-db-host:7687
NEO4J_USER=your_username
NEO4J_PASSWORD=your_password
```

2. Run the demo:

```bash
uv run python -m demo
```

---

## Using an Existing Pickled Conversations File

If you already have a `conversations.pkl` file, place it in the project root and run:

```bash
uv run python -m demo
```

---

## Project Structure

```
demo/
│
├── conversation/         # Computes sentiment evolution & categorizes by topic
│   └── adjust.py         # Filters conversations by a specified time frame
│
└── poster_plots/         # Generates visualizations for the project poster
```

The demo uses our custom library [`conversation-store`](https://github.com/zenithanalitica/conversation-store), which retrieves conversations from the database and stores them in a pickle file for fast access.

### External Dependencies (Cloned Automatically)

When running `run.sh` or `run.ps1`, the following repositories are cloned:

* [`data-pipeline`](https://github.com/zenithanalitica/data-pipeline)
  Parses `.json` files, cleans data, removes duplicates, and uploads to the database.

* [`sentiment-score`](https://github.com/zenithanalitica/sentiment-score)
  Calculates sentiment scores for each Tweet in the database.

---
