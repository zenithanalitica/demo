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
   git clone <repo-url>
   cd <repo-directory>
   ```
2. Make the `run.sh` script executable:

   ```bash
   chmod +x run.sh
   ```
3. Execute the script:

   ```bash
   ./run.sh
   ```

---

### On Windows

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```
2. Run the batch file:

   ```bash
   run.bat
   ```

---
