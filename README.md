# Project Setup and Running

## Prerequisites

* **[Docker](https://docs.docker.com/get-docker/)** (with Docker Compose ≥ 2.0)
* **[Git](https://git-scm.com/)**
* **[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)** (Optional, but significantly speeds up sentiment score calculations)

> **Note for Windows Users:**
> If you're using GPU acceleration, refer to the [Docker GPU support documentation](https://docs.docker.com/desktop/features/gpu/).

---

## Running

### On Linux

1. Clone the repository:

   ```bash
   git clone https://github.com/zenithanalitica/demo/
   cd demo/

2. Place unzipped data in the current directory, so it looks like this:
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
3. Make the `run.sh` script executable:

   ```bash
   chmod +x run.sh
   ```
4. Execute the script:

   ```bash
   ./run.sh
   ```

---

### On Windows

1. Clone the repository:

   ```bash
   git clone https://github.com/zenithanalitica/demo/
   cd demo/
2. Place unzipped data in the current directory, so it looks like this:
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
3. Run the Powershell file:

   ```bash
   .\run.ps1
   ```
(You may need to bypass the execution policy with `powershell -ExecutionPolicy Bypass -File run.ps1`)

---

### Running with an Existing and Populated Database

To run the demo without setting up or populating a new database, create a `.env` file in the project root directory with the following environment variables:

* `NEO4J_URI      # Points to the database address (e.g., example.com:7687)`
* `NEO4J_USER`
* `NEO4J_PASSWORD`

Then run the demo using:

```bash
uv run python -m demo
```

---

### Running with an Existing `conversations.pkl` File

Ensure the `conversations.pkl` file is located in the project root directory.
Then, simply execute:

```bash
uv run python -m demo
```

---

## Project Structure

```
demo/
│
├── conversation/        # Handles sentiment evolution calculation and categorization into topics
│   └── adjust.py        # Filters conversations by a specified time frame
│
└── poster_plots/        # Generates visualizations used in the poster
```

The demo relies on the [`conversation-store`](https://github.com/zenithanalitica/conversation-store) library, developed in-house. It retrieves conversations from the database and stores them in a pickle file for fast access.

When running `run.sh` (Linux/macOS) or `run.ps1` (Windows), two additional repositories are cloned automatically:

* [`data-pipeline`](https://github.com/zenithanalitica/data-pipeline): Parses `.json` files, cleans the data, removes duplicates, and uploads it to the database.
* [`sentiment-score`](https://github.com/zenithanalitica/sentiment-score): Computes sentiment scores for each Tweet stored in the database.

---
