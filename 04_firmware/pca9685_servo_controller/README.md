Перед запуском:
Bash
sudo apt-get install python3-smbus
sudo apt-get install i2c-tools
sudo raspi-config

включить:
Interface → I2C → Enable


Raspberry Pi
   ↓ I2C
PCA9685
   ↓ PWM
MG995 (язычок)