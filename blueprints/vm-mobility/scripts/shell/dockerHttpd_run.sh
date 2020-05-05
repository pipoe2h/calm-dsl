# Start a Web server with the packages
docker run -dit --name webserver -p 8080:80 -v $HOME/www/:/usr/local/apache2/htdocs/ httpd:2.4
