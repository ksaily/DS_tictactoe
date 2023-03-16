# DS_tictactoe
Distributed systems tic-tac-toe game

Consists of three nodes: one server and two clients connecting at the same time. 

To run you need to have Docker installed.
To create an image:
- docker build -t [image_name] . 

To create a container inside image and start the server:
- docker run -it --name [container_name] [image_name]

You can then open two terminals for clients:
- docker exec -it [container_name] bash

And run:
- python client.py
to start a client (run two clients in different windows)

You can then play tic-tac-toe with someone else!
