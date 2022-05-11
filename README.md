# epaper frame

### Icnluded scripts:

- bitcoin.py
  Shows info about Bitcoin price, Fear & Greed index and Mempool
- picture.py
  Loops images in `pictures` folder

### Required hardware:

- Raspberry Pi (Zero)
- Waveshare e-Paper HAT
- 7.5" Waveshare e-Ink display

### Setup process:

1.  Install dietpi
2.  SSH in with user dietpi
3.  In ~, clone Waveshare e-Paper repo from
    https://github.com/waveshare/e-Paper
4.  Install additional dependencies:
    - ???
5.  Setup crontab:

    - `crontab -e`
    - Enter:
      `*/15 * * * * cd /home/dietpi/e-Paper/RaspberryPi_JetsonNano/python/display && ./cron.sh`
    - Press Ctrl+X and then Return to save and exit

6.  Use dietpi-config -> Autostart options -> Custom script (background, no autologin) with this script:

        #!/bin/bash
        # DietPi-Autostart custom script
        # Location: /var/lib/dietpi/dietpi-autostart/custom.sh

        cd /home/dietpi/e-Paper/RaspberryPi_JetsonNano/python/display
        ./cron.sh &
        python3 serve.py

        exit 0
