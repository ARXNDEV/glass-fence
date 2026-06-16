# Installation

The preferred way to install Glass Fence is to use Docker. This method is easy to set up and manage, it contains all the necessary dependencies, and it is isolated from the host system. Other installation methods are out of scope for this documentation.

## Docker Run {#docker-run}

To start a basic Glass Fence container, use the following command:

```sh
docker run -d --rm \
  -p 8080:8080 \
  -p 56000-56100:56000-56100/udp \
  -e GF_WEBRTC_EPR=56000-56100 \
  -e GF_WEBRTC_NAT1TO1=127.0.0.1 \
  -e GF_MEMBER_MULTIUSER_USER_PASSWORD=glass-fence \
  -e GF_MEMBER_MULTIUSER_ADMIN_PASSWORD=admin \
  arxndevv/glass-fence/firefox:latest
```

### Explanation {#docker-run-explanation}

- `-d --rm` - Run the container in the background and automatically remove the container when it exits.
- `-p 8080:8080` - Map the container's port `8080` to the host's port `8080`.
- `-p 56000-56100:56000-56100/udp` - Map the container's UDP ports `56000-56100` to the host's ports `56000-56100`.
- `-e GF_WEBRTC_EPR=56000-56100` - Set the WebRTC endpoint range, this value must match the mapped ports above.
  - See [WebRTC Ephemeral Port Range](/docs/v3/configuration/webrtc#epr) for more information about this setting.
  - There is an alternative to use only a single port, see [WebRTC UDP/TCP multiplexing](/docs/v3/configuration/webrtc#mux).
- `-e GF_WEBRTC_NAT1TO1=127.0.0.1` - Set the address where the WebRTC client should connect to.
  - To test only on the local computer, use `127.0.0.1`.
  - To use it in a private network, use the host's IP address (e.g., `192.168.1.5`).
  - To use it in a public network, you need to correctly set up port forwarding on your router and remove this env variable.
  - See [WebRTC Server IP Address](/docs/v3/configuration/webrtc#ip) for more information about this setting.
- `-e GF_MEMBER_MULTIUSER_USER_PASSWORD=glass-fence` - Set the password for the user account.
- `-e GF_MEMBER_MULTIUSER_ADMIN_PASSWORD=admin` - Set the password for the admin account.
  - See [Multiuser Configuration](/docs/v3/configuration/authentication#member.multiuser) for more information about this setting.
  - There are other authentication providers available, see [Authentication Providers](/docs/v3/configuration/authentication#member).
- `arxndevv/glass-fence/firefox:latest` - The Docker image to use.
  - See available [Docker Images](/docs/v3/installation/docker-images).

Now, open your browser and go to: `http://localhost:8080`. You should see the Glass Fence interface.

### Further Configuration {#configuration}

You can configure Glass Fence by setting environment variables or configuration file. See the [Configuration Reference](/docs/v3/configuration) for more information.

## Docker Compose {#docker-compose}

You can also use Docker Compose to run Glass Fence. It is preferred to use Docker Compose for running Glass Fence in production because you can easily manage the container, update it, and configure it.

Create a `docker-compose.yml` file with the following content:

```yaml title="docker-compose.yaml"
services:
  glass-fence:
    image: arxndevv/glass-fence/firefox:latest
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "56000-56100:56000-56100/udp"
    environment:
      GF_WEBRTC_EPR: "56000-56100"
      GF_WEBRTC_NAT1TO1: "127.0.0.1"
      GF_MEMBER_MULTIUSER_USER_PASSWORD: "glass-fence"
      GF_MEMBER_MULTIUSER_ADMIN_PASSWORD: "admin"
```

Then, run the following command:

```sh
docker compose up -d
```

To stop Glass Fence, run:

```sh
docker compose down
```

To update Glass Fence, run:

```sh
docker compose pull
docker compose up -d
```

Learn more about [how compose works](https://docs.docker.com/compose/intro/compose-application-model/).

:::note
You need to be in the same directory as the `docker-compose.yml` file to run the `docker compose` commands.
:::

## Next Steps {#next}

import DocCardList from '@theme/DocCardList';

<DocCardList />
