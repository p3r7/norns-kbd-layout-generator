# norns-kbd-layout-generator

convert layout files from [QMK project](https://github.com/qmk/qmk_firmware) to monome norns own format.


### usage

retrieve any of the layout files (`keymap_*.h`) from https://github.com/qmk/qmk_firmware/tree/master/quantum/keymap_extras/ locally.

run the script, e.g.:

    python3 ./main.py --src ~/Code/qmk_firmware/quantum/keymap_extras/keymap_french.h --dest fr.lua

drop the resulting file in the `/home/we/norns/lua/core/keymap/`

tweak the following section in `/home/we/norns/lua/core/keymap/keyboard.lua`

```lua
keyboard.keymap = {}
keyboard.keymap.us = require 'core/keymap/fr'
keyboard.selected_map = "fr"
```


### limitations

lots of keyboard layout use AltGr (right Alt key) in addition to Shift for entering a bunch of characters. norns' simple keyboard support implementation currently does not support it.
