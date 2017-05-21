sudo yum install docker<< EOF
y
EOF
sudo service docker start
sudo chkconfig docker on
sudo docker build -t python_bug docker/
cd bug
sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-x86_64.tar.bz2
sudo tar xjf phantomjs-1.9.7-linux-x86_64.tar.bz2
sudo docker run -it --rm -v /home/ec2-user/python/bug/:/home python_bug