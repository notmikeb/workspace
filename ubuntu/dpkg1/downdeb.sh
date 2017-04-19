apt-cache depends $1 |grep 'Depends:' | awk '{print $2}' | xargs -n 1 apt-get download 
apt-get download $1
