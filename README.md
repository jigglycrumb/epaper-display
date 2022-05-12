# epaper display

A collection of scripts for 7.5" e-ink displays

![epaper-front](https://user-images.githubusercontent.com/1476865/168150419-a330e386-8eb9-402c-b98f-0a8688f49a43.jpg)

![epaper-back](https://user-images.githubusercontent.com/1476865/168150472-f4ccc03f-5fee-44b2-b353-94d27c2aff33.jpg)

### Required hardware:

- Raspberry Pi Zero W
- Waveshare e-Paper HAT
- 7.5" Waveshare e-Ink display

### Included scripts:

- `bitcoin.py` - shows some Bitcoin info:

  - current price
  - fear & greed index
  - 7 day graph
  - block time
  - moscow time
  - fees

  ![epaper-bitcoin](https://user-images.githubusercontent.com/1476865/168150548-44273cfc-8e8e-424c-b157-e8669a2663b9.jpg)

- `picture.py` - loops images in `pictures` folder

  ![epaper-picture](https://user-images.githubusercontent.com/1476865/168150525-7a35f9d5-da87-43e3-b657-7c3a04ae0a1a.jpg)

- `fear_and_greed.py`- shows the latest [Fear & Greed index gauge](https://alternative.me/crypto/fear-and-greed-index/) as image

  ![epaper-fear-and-greed](https://user-images.githubusercontent.com/1476865/168160969-f7b898b2-c13e-45d0-8e68-f850c5ae0a90.jpg)

### Interface

The display hosts a small website - open http://epaper to access it.  
It will show the current script (and image, if the picture script is active)
and links to refresh the display or change the script:

- http://epaper/refresh  
  Refreshes the display.  
  When the picture script is active, it changes to the next picture.

- http://epaper/flip-the-script  
  Changes the current display script and refreshes the display.  
  Modify the `scripts` variable in `display/serve.py` to adjust included scripts.  
  The default scripts are the `bitcoin.py` and `picture.py` script.

### Setup process:

1.  Flash [dietpi](https://dietpi.com) to an SD card
2.  Connect Raspberry Pi with HAT & display, insert SD and boot
3.  SSH in with user `dietpi`
4.  In the home folder, clone the [Waveshare e-Paper repo](https://github.com/waveshare/e-Paper):  
    `git clone https://github.com/waveshare/e-Paper.git`
5.  Clone this repo or download and extract it to:  
    `/home/dietpi/e-Paper/RaspberryPi_JetsonNano/python`
6.  Install additional dependencies:
    - `sudo pip3 install cairosvg`
    - `sudo pip3 install pillow`
    - `sudo pip3 install requests`
7.  Setup crontab:

    - `crontab -e`
    - Add this line:
      `*/10 * * * * curl http://localhost/flip-the-script`
    - Press `Ctrl+X` and then `Return` to save and exit

    This will change the display script every 10 minutes, switching between bitcoin info and picture frame with the default setup.

    To just refresh without changing scripts, use this in crontab:  
    `*/10 * * * * curl http://localhost/refresh`

8.  Use `dietpi-config` -> Autostart options -> Custom script (background, no autologin) with this script:

    ```bash
    #!/bin/bash

    # DietPi-Autostart custom script
    # Location: /var/lib/dietpi/dietpi-autostart/custom.sh

    cd /home/dietpi/e-Paper/RaspberryPi_JetsonNano/python/display
    ./runscript.sh &
    python3 serve.py

    exit 0
    ```

9.  Optional:

    If you have [Flic](https://flic.io) buttons you can use them to refresh the display and change the script.

    A single click will refresh, double click or hold will change the script.

    To set this up, open FlicHub SDK, create a new module, paste this script and start it.
    Then, connect a button via the app and name it `ePaper`.

    ```javascript
    // main.js
    var buttonManager = require("buttons");
    var http = require("http");

    buttonManager.on("buttonSingleOrDoubleClickOrHold", function (obj) {
      var url = "http://epaper"; // put your hostname here if you used a different one
      var button = buttonManager.getButton(obj.bdaddr);
      var clickType = obj.isSingleClick
        ? "click"
        : obj.isDoubleClick
        ? "double_click"
        : "hold";

      console.log('pressed button "' + button.name + '": ' + clickType);

      if (button.name === "ePaper") {
        switch (clickType) {
          case "click":
            url += "/refresh";
            break;

          case "double_click":
          case "hold":
            url += "/flip-the-script";
            break;

          default:
            return;
        }

        http.makeRequest(
          {
            url: url,
            method: "GET",
          },
          function (err, res) {
            console.log("requested URL: " + url);
          }
        );
      }
    });

    console.log("Listening for ePaper button...");
    ```
