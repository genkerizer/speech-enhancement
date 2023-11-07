docker run --rm -it \
           --network="host" \
           -v `pwd`:/server \
           --name mpsenet \
           hopny:latest bash