# Chat-server

In the terminal window:
STEP 1
docker network create chat-network
STEP 2
docker run -d --network chat-network -p 55555:55555 --name chat-server chat-server

STEP 3
To start different clients please connect each chat client using a unique name.
Example:
docker run -it --network chat-network --name chat-client1 chat-client
docker run -it --network chat-network --name chat-client2 chat-client
docker run -it --network chat-network --name chat-client3 chat-client