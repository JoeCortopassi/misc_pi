#! /bin/sh
FOO="$(nmap -p 22 --open 10.0.1.1/24 | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")"
echo "IP: ${FOO}"
