sudo sed -i 's|DocumentRoot "/var/www/html"|DocumentRoot "/var/www/html/nutanix"|' /etc/httpd/conf/httpd.conf
echo '<Directory "/var/www/html/nutanix">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>' | sudo tee /etc/httpd/conf.modules.d/nutanix.conf

echo "<IfModule mod_dir.c>
        DirectoryIndex index.php index.html index.cgi index.pl index.php index.xhtml index.htm
</IfModule>" | sudo tee /etc/httpd/conf.modules.d/dir.conf

sudo mkdir -p /var/www/html/nutanix
cd /var/www/html/nutanix

echo 'SetEnv PLATFORM "@@{PLATFORM}@@"' | sudo tee .htaccess
sudo wget https://raw.githubusercontent.com/pipoe2h/calm/master/demo/webpage/index.php 
sudo wget https://raw.githubusercontent.com/pipoe2h/calm/master/demo/webpage/nutanix_hybrid_cloud.png
sudo wget https://raw.githubusercontent.com/pipoe2h/calm/master/demo/webpage/style.css
sudo wget https://github.com/pipoe2h/calm/raw/master/demo/webpage/nutanix_logo.png

sudo systemctl enable httpd.service
sudo systemctl restart httpd.service