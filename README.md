# chillzie-apn-server

Generate self-signed SSL keys like this: use 'rest.chillzie.com' as CN

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout rest.chillzie.com.key -out rest.chillzie.com.crt