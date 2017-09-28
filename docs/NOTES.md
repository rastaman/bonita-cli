# Notes

## Test the Bonita API by hand

Open session:
```sh
curl -v -c saved_cookies.txt -X POST --url 'http://10.196.76.232:8080/bonita/loginservice' --header 'Content-Type: application/x-www-form-urlencoded; charset=utf-8' -O /dev/null -d 'username=install&password=install&redirect=false&redirectURL='
```

Try to stop a tenant:
```sh
curl -b saved_cookies.txt -X PUT -H "Content-Type: application/json" -d '{"paused":"true"}' --url 'http://10.196.76.232:8080/bonita/API/system/tenant/unusedid'
```
