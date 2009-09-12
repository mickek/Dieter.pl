server {
        listen 80;
        server_name www.dieter.pl;
        rewrite ^/(.*) http://.dieter.pl/$1 permanent;
}


server {

	listen 80;
        server_name beta.dieter.pl;

        access_log  /var/log/nginx/dieter.access.log;

	rewrite ^/s/(.*)$ /media/$1 last;

        location ^~ /media/  {
                gzip on;
                root /var/www/dieter/;
                expires 60d;
        }

        location ^~ /admin-media/ {
                root /var/www/dieter/;
                expires 30d;
        }

        location / {

                auth_basic            "Restricted";
                auth_basic_user_file  /etc/nginx/htpasswd-dieter;
		expires -1;

                # host and port to fastcgi server
                fastcgi_pass 127.0.0.1:10000;
                fastcgi_param PATH_INFO $fastcgi_script_name;
                fastcgi_param REQUEST_METHOD $request_method;
                fastcgi_param QUERY_STRING $query_string;
                fastcgi_param CONTENT_TYPE $content_type;
                fastcgi_param CONTENT_LENGTH $content_length;
                fastcgi_param SERVER_PROTOCOL $server_protocol;
                fastcgi_param SERVER_PORT $server_port;
                fastcgi_param SERVER_NAME $server_name;
                fastcgi_pass_header Authorization;
                fastcgi_intercept_errors off;
        }

        error_page  404  /404.html;
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
                root   /var/www/nginx-default;
        }
}
