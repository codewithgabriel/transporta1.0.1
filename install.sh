#!/bin/bash

printf "\033[93m[+] installing transporta...\033[0m \n"
printf "[+] installing requirement... \n"
pip3 install -r requirements.txt
printf "[+] installing transporta to /usr/bin/transporta..this require sudo privillage! \n" 
sudo cp transporta /usr/bin/transporta
printf "[+] done \n"
