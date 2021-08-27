echo "==========start setup ssh,ip fixed,wifi =========="

#wifiを設定
sudo cp wpa_supplicant.conf /etc/wpa_supplicant.conf

#ssh有効化
sudo mkdir /boot/ssh

#ip固定化
sudo cp dhcpcd.conf /etc/dhcpcd.conf

#再起動
sudo reboot
echo "==========           finish             =========="


