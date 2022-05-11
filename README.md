# epaper display

A collection of scripts for 7.5" e-ink displays

### Included scripts:

- `bitcoin.py` - shows some Bitcoin info:

  - current price
  - fear & greed index
  - 7 day graph
  - block time
  - moscow time
  - fees

  TODO sample

- `picture.py` - loops images in `pictures` folder

  TODO sample

- `fear_and_greed.py`- shows the latest [Fear & Greed index gauge](https://alternative.me/crypto/fear-and-greed-index/) as image

  TODO sample

### Required hardware:

- Raspberry Pi Zero W
- Waveshare e-Paper HAT
- 7.5" Waveshare e-Ink display

### Setup process:

1.  Flash [dietpi](https://dietpi.com) to an SD card
2.  Connect Raspberry Pi with HAT & display, insert SD and boot
3.  SSH in with user `dietpi`
4.  In the home folder, clone Waveshare e-Paper repo from
    https://github.com/waveshare/e-Paper
5.  Clone this repo or download and extract it to:
    `/home/dietpi/e-Paper/RaspberryPi_JetsonNano/python`
6.  Install additional dependencies:
    - ???
7.  Setup crontab:

    - `crontab -e`
    - Enter:
      `*/10 * * * * */10 * * * * curl http://localhost/flip-the-script`
    - Press `Ctrl+X` and then `Return` to save and exit

    This will change the display script every 10 minutes, switch between bitcoin info and picture frame with the default setup

8.  Use `dietpi-config` -> Autostart options -> Custom script (background, no autologin) with this script:

        #!/bin/bash
        # DietPi-Autostart custom script
        # Location: /var/lib/dietpi/dietpi-autostart/custom.sh

        cd /home/dietpi/e-Paper/RaspberryPi_JetsonNano/python/display
        ./runscript.sh &
        python3 serve.py

        exit 0

9.  Optional:

    If you have [Flic](https://flic.io) buttons you can use them to refresh the display and change the script.

    To do this, use this script in FlicHub SDK. A single click will refresh, double click or hold will change the script.

    ```
    // main.js
    var buttonManager = require("buttons");
    var http = require("http");

    buttonManager.on("buttonSingleOrDoubleClickOrHold", function(obj) {
    var url = "http://epaper"; // put your hostname here if you used a different one
    var button = buttonManager.getButton(obj.bdaddr);
    var clickType = obj.isSingleClick ? "click" : obj.isDoubleClick ? "double_click" : "hold";

        console.log('pressed button "' + button.name + '": ' + clickType)

        if(button.name === "ePaper") {
          switch(clickType) {
            case 'click':
              url+= "/refresh";
              break;

            case 'double_click':
            case 'hold':
              url+= "/flip-the-script";
              break;

            default:
              return;
          }

          http.makeRequest({
            url: url,
            method: "GET",
          }, function(err, res) {
            console.log("requested URL: " + url);
            // console.log(err, res)
          });
        }

    });

    console.log("Listening for ePaper button...");
    ```
