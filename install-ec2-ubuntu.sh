#Install dependencies on raw ec2 ubuntu machine
#RUN FROM WITHIN dragDropUpload HOME DIR!

wget https://nodejs.org/dist/v12.17.0/node-v12.17.0-linux-x64.tar.xz
tar -xf node-v12.17.0-linux-x64.tar.xz
rm *.xz
sudo mkdir /usr/local/lib/node
sudo mv node-v12.17.0-linux-x64 /usr/local/lib/node/nodejs
export NODEJS_HOME=/usr/local/lib/node/nodejs
export PATH=$NODEJS_HOME/bin:$PATH
. ~/.profile
   
#update apt-get, install stable python3 (typically 3.6)

sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip

#Install project requirements
npm install
pip3 install -r requirements.txt