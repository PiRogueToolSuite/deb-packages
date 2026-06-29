# This folder
Place here extra service nginx 'location' .conf files.
They will be included within nginx `server {}` declarations.

Ex:
```
location /my-service/ {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Prefix /my-service;
    proxy_pass http://localhost:12345/;
}
```