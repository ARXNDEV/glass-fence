---
description: Building Glass Fence from source
---

# Building From Source

This guide walks you through the process of setting up Glass Fence on your local machine or server.

Start by cloning the Glass Fence Git repository to your machine:

```bash
git clone https://github.com/ARXNDEV/glass-fence.git
cd glass-fence
```

## Building the Frontend {#frontend}

Prerequisites for building the frontend:
- [node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/)

Navigate to the `client` directory and install the dependencies:

```bash
cd client;
npm install;
npm run build;
```

The `npm run build` command will create a production build of the frontend in the `client/build` directory.

## Building the Server {#server}

Prerequisites for building the server:
- [go](https://golang.org/) (version 1.18 or higher)
- Dependencies for building the server:
  ```bash
  sudo apt-get install -y --no-install-recommends libx11-dev libxrandr-dev libxtst-dev libgtk-3-dev libxcvt-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
  ```
Navigate to the `server` directory and build the server:

```bash
cd server;
./build;
```

This will create a binary file named `glass-fence` in the `bin` directory along with `plugins` that were built with the server.
