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
