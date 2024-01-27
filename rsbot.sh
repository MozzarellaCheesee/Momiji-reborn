#!/bin/bash 

if ["$1" = "Momiji"]; then
	cd /var/Momiji-reborn
	git pull;
	pm2 restart momiji;
fi
if ["$1" = "Chester"]; then
	cd /var/Chester;
	git pull;
	pm2 restart chester;
fi
if [ "$#" -lt 1 ]; then
	echo "Недостаточно аргументов. Пожалуйста, передайте в качестве аргумента имя. Пример: $0 Vasya";
    	exit 1;
fi
