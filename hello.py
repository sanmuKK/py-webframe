server
{
    listen
9999;  # 阿里云添加安全组规则端口8081
server_name
192.168
.8
.204;  # 域名或者公网IP
location / {
    proxy_pass
http: // 127.0
.0
.1: 9998;  # 指向gunicorn host的服务器地址
proxy_set_header
Host $host;
proxy_set_header
X - Forwarded - For $proxy_add_x_forwarded_for;
}}
# 前端
server
{
    listen
80;  # 1.你想让你的这个项目跑在哪个端口
server_name
192.168
.8
.204;  # 2.当前服务器ip
# location / {
location / {
    # add_header Access-Control-Allow-Origin *;
    # add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS, DELETE';
    # add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
    root / opt / dist_v22;  # 3.dist文件的
try_files $uri $uri / / index.html;  # 4.重定向,内部文件的指向(照写)
}
location / api
{
    rewrite ^ / api(. *)$ / $1
break;
proxy_pass
http: // localhost: 9999;
}

#     location /api {
#     proxy_pass   http://127.0.0.1:9999;
#     proxy_set_header Host $host;
#     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
# }
location / socket.io
{
proxy_pass
http: // 127.0
.0
.1: 9999 / socket.io / real_data_all;
proxy_redirect
off;
proxy_buffering
off;
proxy_read_timeout
600
s;

proxy_set_header
Host $host;
proxy_set_header
X - Real - IP $remote_addr;
proxy_set_header
X - Forwarded - For $proxy_add_x_forwarded_for;

proxy_http_version
1.1;
proxy_set_header
Upgrade $http_upgrade;
proxy_set_header
Connection
"Upgrade";
}
}