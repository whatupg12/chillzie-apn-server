# chillzie-apn-server

Generate self-signed SSL keys like this: use 'rest.chillzie.com' as CN

```shell
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout rest.chillzie.com.key \
    -out rest.chillzie.com.crt
```

Build docker:
```shell
docker build -t chillzie .
```

Run docker:

```shell
keypath=/key-dir/
keystore_name=keystore.p8
key_id=key-id
team_id=team-id
docker run -it --rm -p 443:443 \
    -v ${keypath}:/keys/ \
    -e APN_KEYSTORE_P8=/keys/${keystore} \
    -e APN_AUTH_KEY_ID${key_id} \
    -e APN_TEAM_ID=${team_id} \
    chillzie
```

Forcing a push
```shell
token=123
alarm=2019-05-11T11:21:00EDT
server=https://localhost
curl -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "token_hex=${token}&alarm=${alarm}" \
    --insecure \
    ${server}/alarm
```