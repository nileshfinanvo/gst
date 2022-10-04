
git clone https://nileshfinanvo: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@github.com/nileshfinanvo/gst_scripts.git

sudo apt update
sudo apt install python3-pip
pip3 install requests bs4 mysql-connector azcaptchaapi pytz lxml
chmod +x gst_scripts/server_cron.sh
./gst_scripts/server_cron.sh
