# chillzie-apn-server

Generate self-signed SSL keys like this: use 'rest.chillzie.com' as CN

```shell
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout rest.chillzie.com.key \
    -out rest.chillzie.com.crt
```

Run docker:

```shell
docker run -it --rm -p 443:443 \
    -v /key-dir/:/keys/ \
    -e APN_KEYSTORE_P8=/keys/keystore.p8 \
    -e APN_AUTH_KEY_ID=key-id \
    -e APN_TEAM_ID=team-id \
    chillzie
```

Forcing a push
```shell
curl -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "token_hex=123&alarm=2019-05-11T11:21:00EDT" \
    --insecure \
    https://localhost/alarm
```