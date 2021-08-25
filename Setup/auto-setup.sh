echo "==========start setup ssh,ip fixed,wifi =========="

#wifiを設定
cp wpa_supplicant.conf /etc/wpa_supplicant.conf

#ssh有効化
mkdir /boot/ssh

#ip固定化
cp dhcpcd.conf /etc/dhcpcd.conf

#再起動
sudo reboot
echo "==========           finish             =========="


