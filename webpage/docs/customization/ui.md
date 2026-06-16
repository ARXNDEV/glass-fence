---
sidebar_label: "User Interface"
description: "Customize the Glass Fence user interface with your own UI files."
---

# Customizing the UI

Currently there is no configuration for customizing the UI of Glass Fence. You need to modify the source code to change the UI.

```bash
# Clone the repository
git clone https://github.com/ARXNDEV/glass-fence
# Change to the client directory
cd glass-fence/client
# Install the dependencies
npm install
# Build the project
npm run build
```

You can mount your newly created UI files to the container to `/var/www` to overwrite the default files. The Glass Fence web server will automatically reload the new files when they are changed. You can use the following command to mount your new UI files to the container:

```yaml title="docker-compose.yaml"
services:
  glass-fence:
    image: "arxndevv/glass-fence/firefox:latest"
    restart: "unless-stopped"
    shm_size: "2gb"
    ports:
      - "8080:8080"
      - "52000-52100:52000-52100/udp"
    # highlight-start
    volumes:
      - "./client/dist:/var/www"
    # highlight-end
    environment:
      GF_DESKTOP_SCREEN: 1920x1080@30
      GF_MEMBER_MULTIUSER_USER_PASSWORD: glass-fence
      GF_MEMBER_MULTIUSER_ADMIN_PASSWORD: admin
      GF_WEBRTC_EPR: 52000-52100
      GF_WEBRTC_ICELITE: 1
```

## Query parameters {#query-parameters}

You can use query parameters to customize the Glass Fence web interface. These parameters can be added to the URL when accessing the Glass Fence web interface. The following table lists the available query parameters:

| Query Parameter    | Description                                                |
|--------------------|------------------------------------------------------------|
| `?usr=<username>`  | Prefills the username field.                               |
| `?pwd=<password>`  | Prefills the password field.                               |
| `?cast=1`          | Hides all controls and shows only the video.               |
| `?embed=1`         | Hides most additional components and shows only the video. |
| `?volume=<0-1>`    | Sets the volume to the given value (between 0 and 1).      |
| `?lang=<language>` | Sets the language to the given value.                      |
| `?show_side=1`     | Shows the sidebar on startup.                              |
| `?mute_chat=1`     | Mutes the chat on startup.                                 |

You can combine multiple query parameters in the URL. For example, to set the username to `guest`, the password to `glass-fence`, and enable casting mode, you can use the following URL:

Example: `http(s)://<URL:Port>/?pwd=glass-fence&usr=guest&cast=1`