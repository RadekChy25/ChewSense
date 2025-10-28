# ChewSense
This is a project for Expert in Teams course.

## Command to run:
Build the docker image. Then run the command to run the image.
Use xhost to allow Docker to connect.
```
xhost +local:docker
```
```
docker run -it --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix YOUR_DOCKER_IMAGE
```