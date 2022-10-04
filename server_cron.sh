#!/bin/bash
chmod +x /home/ubuntu/gst_scripts/server_auth.sh
chmod +x /home/ubuntu/gst_scripts/server_bd.sh
chmod +x /home/ubuntu/gst_scripts/server_fd.sh
chmod +x /home/ubuntu/gst_scripts/server_jamku_hsn_as.sh
chmod +x /home/ubuntu/gst_scripts/server_jamku_hsndesc.sh
chmod +x /home/ubuntu/gst_scripts/server_jamku_sac_asc.sh
chmod +x /home/ubuntu/gst_scripts/server_jamku_sac_desc.sh
chmod +x /home/ubuntu/gst_scripts/server_octa.sh
chmod +x /home/ubuntu/gst_scripts/server_pan.sh
chmod +x /home/ubuntu/gst_scripts/server_callingf.sh
chmod +x /home/ubuntu/gst_scripts/server_gst_server.sh
chmod +x /home/ubuntu/gst_scripts/server_panvpds.sh
chmod +x /home/ubuntu/gst_scripts/server_textpayer.sh
chmod +x /home/ubuntu/gst_scripts/server_callingf2.sh
chmod +x /home/ubuntu/gst_scripts/server_callingf3.sh
chmod +x /home/ubuntu/gst_scripts/server_callingf4.sh
chmod +x /home/ubuntu/gst_scripts/server_callingf5.sh
chmod +x /home/ubuntu/gst_scripts/server_knowyour.sh
chmod +x /home/ubuntu/gst_scripts/server_tikshare.sh

cron_line="@reboot sh /home/ubuntu/gst_scripts/server_auth.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_bd.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_fd.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_pan.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_callingf.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_callingf2.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_callingf3.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_callingf4.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_callingf5.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -

cron_line="@reboot sh /home/ubuntu/gst_scripts/server_knowyour.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_tikshare.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_gst_server.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_panvpds.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_textpayer.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_jamku_hsn_as.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_jamku_hsndesc.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_jamku_sac_asc.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_jamku_sac_desc.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -
cron_line="@reboot sh /home/ubuntu/gst_scripts/server_octa.sh"
(crontab -u ubuntu -l; echo "$cron_line" ) | crontab -u ubuntu -

