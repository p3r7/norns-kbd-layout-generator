# norns-kbd-layout-generator

convert layout files from [QMK project](https://github.com/qmk/qmk_firmware) to monome norns own format.


### usage

retrieve any of the layout files (`keymap_*.h`) from https://github.com/qmk/qmk_firmware/tree/master/quantum/keymap_extras/ locally.

run the script, e.g.:

    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_french.h --dest fr.lua

drop the resulting file in the `/home/we/norns/lua/core/keymap/`

tweak the following section in `/home/we/norns/lua/core/keyboard.lua`

```lua
keyboard.keymap = {}
keyboard.keymap.us = require 'core/keymap/us'
keyboard.keymap.fr = require 'core/keymap/fr' -- new entry
keyboard.selected_map = "fr"                  -- changed value
```

### full dump

    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_belgian.h --dest be.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_croatian.h --dest hr.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_czech.h --dest cz.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_danish.h --dest dk.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_estonian.h --dest ee.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_finnish.h --dest fi.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_french.h --dest fr.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_german.h --dest de.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_greek.h --dest gr.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_hungarian.h --dest hu.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_icelandic.h --dest is.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_irish.h --dest ie.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_italian.h --dest it.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_jp.h --dest jp.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_korean.h --dest kp.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_latvian.h --dest lv.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_norwegian.h --dest no.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_polish.h --dest pl.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_portuguese.h --dest pt.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_romanian.h --dest ro.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_russian.h --dest ru.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_serbian.h --dest rs.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_slovak.h --dest sk.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_slovenian.h --dest si.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_spanish.h --dest es.lua
    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_swedish.h --dest se.lua


### limitations

lots of keyboard layout use AltGr (right Alt key) in addition to Shift for entering a bunch of characters. norns' simple keyboard support implementation currently does not support it.
