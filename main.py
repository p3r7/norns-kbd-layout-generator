#!/usr/bin/env python 3

import re
import argparse
from pprint import pprint


## ------------------------------------------------------------------------
## DEBUG

DEBUG = False
# DEBUG = True


## ------------------------------------------------------------------------
## ARGS

parser = argparse.ArgumentParser("Convert QMK layout file to norns format")
parser.add_argument("--src", help="source QMK file, any of `qmk_firmware/quantum/keymap_extras/keymap_*.h`", required=True)
parser.add_argument("--dest", help="output norns file, typically `<ISO_3166_alpha2>.lua`", required=True)

args = parser.parse_args()

# args.src = '/home/eigen/Documents/Code/monome/qmk_firmware/quantum/keymap_extras/keymap_french.h'
# args.dest = 'fr.lua'


## ------------------------------------------------------------------------
## CONSTANTS

# norns/lua/core/keyboard.lua
# qmk_firmware/tmk_core/common/keycode.h

## NORNS <-> QMK keycode ids
norns_2_gmk = {
    'RESERVED': 'KC_NO',
    'ESC': 'KC_ESCAPE',
    '1': 'KC_1',
    '2': 'KC_2',
    '3': 'KC_3',
    '4': 'KC_4',
    '5': 'KC_5',
    '6': 'KC_6',
    '7': 'KC_7',
    '8': 'KC_8',
    '9': 'KC_9',
    '0': 'KC_0',
    'MINUS': 'KC_MINUS',
    'EQUAL': 'KC_EQUAL',
    'BACKSPACE': 'KC_BSPACE',
    'TAB': 'KC_TAB',
    'Q': 'KC_Q',
    'W': 'KC_W',
    'E': 'KC_E',
    'R': 'KC_R',
    'T': 'KC_T',
    'Y': 'KC_Y',
    'U': 'KC_U',
    'I': 'KC_I',
    'O': 'KC_O',
    'P': 'KC_P',
    'LEFTBRACE': 'KC_LBRACKET',
    'RIGHTBRACE': 'KC_RBRACKET',
    'ENTER': 'KC_ENTER',
    'LEFTCTRL': 'KC_LCTRL',
    'A': 'KC_A',
    'S': 'KC_S',
    'D': 'KC_D',
    'F': 'KC_F',
    'G': 'KC_G',
    'H': 'KC_H',
    'J': 'KC_J',
    'K': 'KC_K',
    'L': 'KC_L',
    'SEMICOLON': 'KC_SCOLON',
    'APOSTROPHE': 'KC_QUOTE', # unsure
    'GRAVE': 'KC_GRAVE',
    'LEFTSHIFT': 'KC_LSHIFT',
    'BACKSLASH': 'KC_BSLASH',
     'Z': 'KC_Z',
    'X': 'KC_X',
    'C': 'KC_C',
    'V': 'KC_V',
    'B': 'KC_B',
    'N': 'KC_N',
    'M': 'KC_M',
    'COMMA': 'KC_COMM',
    'DOT': 'KC_DOT',
    'SLASH': 'KC_SLASH',
    'RIGHTSHIFT': 'KC_RSHIFT',
    'KPASTERISK': 'KC_KP_ASTERISK',
    'LEFTALT': 'KC_LALT',
    'SPACE': 'KC_SPACE',
    'CAPSLOCK': 'KC_CAPSLOCK',
    'F1': 'KC_F1',
    'F2': 'KC_F2',
    'F3': 'KC_F3',
    'F4': 'KC_F4',
    'F5': 'KC_F5',
    'F6': 'KC_F6',
    'F7': 'KC_F7',
    'F8': 'KC_F8',
    'F9': 'KC_F9',
    'F10': 'KC_F10',
    'NUMLOCK': 'KC_NUMLOCK',
    'SCROLLLOCK': 'KC_SCROLLLOCK',
    'KP7': 'KC_KP_7',
    'KP8': 'KC_KP_8',
    'KP9': 'KC_KP_9',
    'KPMINUS': 'KC_KPM_INUS',
    'KP4': 'KC_KP_4',
    'KP5': 'KC_KP_5',
    'KP6': 'KC_KP_6',
    'KPPLUS': 'KC_KP_PLUS',
    'KP1': 'KC_KP_1',
    'KP2': 'KC_KP_2',
    'KP3': 'KC_KP_3',
    'KP0': 'KC_KP_0',
    'KPDOT': 'KC_KP_DOT',
    'ZENKAKUHANKAKU': 'KC_LANG5',
    '102ND': '', # ?!
    'F11': 'KC_F11',
    'F12': 'KC_F12',
    'RO': 'KC_INT1',
    'KATAKANA': 'KC_LANG3',
    'HIRAGANA': 'KC_LANG4',
    'HENKAN': 'KC_INT4',
    'KATAKANAHIRAGANA': 'KC_INT2',
    'MUHENKAN': 'KC_INT5',
    'KPJPCOMMA': 'KC_INT6',
    'KPENTER': 'KC_KP_ENTER',
    'RIGHTCTRL': 'KC_RCTRL',
    'KPSLASH': 'KC_KP_SLASH',
    'SYSRQ': 'KC_SYSREQ',
    'RIGHTALT': 'KC_RALT',
    'LINEFEED': '', # TODO
    'HOME': 'KC_HOME',
    'UP': 'KC_UP',
    'PAGEUP': 'KC_PGUP',
    'LEFT': 'KC_LEFT',
    'RIGHT': 'KC_RIGHT',
    'END': 'KC_END',
    'DOWN': 'KC_DOWN',
    'PAGEDOWN': 'KC_PGDOWN',
    'INSERT': 'KC_INSERT',
    'DELETE': 'KC_DELETE',
    'MACRO': '', # TODO
    'MUTE': 'KC__MUTE',
    'VOLUMEDOWN': 'KC__VOLDOWN',
    'VOLUMEUP': 'KC__VOLUP',
    'POWER': 'KC_POWER',
    'KPEQUAL': 'KC_KP_EQUAL',
    'KPPLUSMINUS': '', # TODO
    'PAUSE': 'KC_PAUSE',
    'SCALE': '', # TODO
    'KPCOMMA': 'KC_KP_COMMA',
    'HANGUEL': 'KC_LANG1',
    'HANJA': 'KC_LANG2',
    'YEN': 'KC_INT3',
    'LEFTMETA': 'KC_LGUI',
    'RIGHTMETA': 'KC_RGUI',
    'COMPOSE': '', # TODO
}

gmk_2_norns = {v: k for k, v in norns_2_gmk.items()}

qmk_aliases = {
    ## Punctuation
    'KC_ENT': 'KC_ENTER',
    'KC_ESC': 'KC_ESCAPE',
    'KC_BSPC': 'KC_BSPACE',
    'KC_SPC': 'KC_SPACE',
    'KC_MINS': 'KC_MINUS',
    'KC_EQL': 'KC_EQUAL',
    'KC_LBRC': 'KC_LBRACKET',
    'KC_RBRC': 'KC_RBRACKET',
    'KC_BSLS': 'KC_BSLASH',
    'KC_NUHS': 'KC_NONUS_HASH',
    'KC_SCLN': 'KC_SCOLON',
    'KC_QUOT': 'KC_QUOTE',
    'KC_GRV': 'KC_GRAVE',
    'KC_COMM': 'KC_COMMA',
    'KC_SLSH': 'KC_SLASH',
    'KC_NUBS': 'KC_NONUS_BSLASH',

    ## Lock Keys
    'KC_CLCK': 'KC_CAPSLOCK',
    'KC_CAPS': 'KC_CAPSLOCK',
    'KC_SLCK': 'KC_SCROLLLOCK',
    'KC_NLCK': 'KC_NUMLOCK',
    'KC_LCAP': 'KC_LOCKING_CAPS',
    'KC_LNUM': 'KC_LOCKING_NUM',
    'KC_LSCR': 'KC_LOCKING_SCROLL',

    ## Commands
    'KC_PSCR': 'KC_PSCREEN',
    'KC_PAUS': 'KC_PAUSE',
    'KC_BRK': 'KC_PAUSE',
    'KC_INS': 'KC_INSERT',
    'KC_DEL': 'KC_DELETE',
    'KC_PGDN': 'KC_PGDOWN',
    'KC_RGHT': 'KC_RIGHT',
    'KC_APP': 'KC_APPLICATION',
    'KC_EXEC': 'KC_EXECUTE',
    'KC_SLCT': 'KC_SELECT',
    'KC_AGIN': 'KC_AGAIN',
    'KC_PSTE': 'KC_PASTE',
    'KC_ERAS': 'KC_ALT_ERASE',
    'KC_CLR': 'KC_CLEAR',

    ## Keypad
    'KC_PSLS': 'KC_KP_SLASH',
    'KC_PAST': 'KC_KP_ASTERISK',
    'KC_PMNS': 'KC_KP_MINUS',
    'KC_PPLS': 'KC_KP_PLUS',
    'KC_PENT': 'KC_KP_ENTER',
    'KC_P1': 'KC_KP_1',
    'KC_P2': 'KC_KP_2',
    'KC_P3': 'KC_KP_3',
    'KC_P4': 'KC_KP_4',
    'KC_P5': 'KC_KP_5',
    'KC_P6': 'KC_KP_6',
    'KC_P7': 'KC_KP_7',
    'KC_P8': 'KC_KP_8',
    'KC_P9': 'KC_KP_9',
    'KC_P0': 'KC_KP_0',
    'KC_PDOT': 'KC_KP_DOT',
    'KC_PEQL': 'KC_KP_EQUAL',
    'KC_PCMM': 'KC_KP_COMMA',

    ## Japanese specific
    'KC_ZKHK': 'KC_GRAVE',
    'KC_RO': 'KC_INT1',
    'KC_KANA': 'KC_INT2',
    'KC_JYEN': 'KC_INT3',
    'KC_HENK': 'KC_INT4',
    'KC_MHEN': 'KC_INT5',

    ## Korean specific
    'KC_HAEN': 'KC_LANG1',
    'KC_HANJ': 'KC_LANG2',

    ## Modifiers
    'KC_LCTL': 'KC_LCTRL',
    'KC_LSFT': 'KC_LSHIFT',
    'KC_LOPT': 'KC_LALT',
    'KC_LCMD': 'KC_LGUI',
    'KC_LWIN': 'KC_LGUI',
    'KC_RCTL': 'KC_RCTRL',
    'KC_RSFT': 'KC_RSHIFT',
    'KC_ALGR': 'KC_RALT',
    'KC_ROPT': 'KC_RALT',
    'KC_RCMD': 'KC_RGUI',
    'KC_RWIN': 'KC_RGUI',

    ## Generic Desktop Page (0x01)
    'KC_PWR': 'KC_SYSTEM_POWER',
    'KC_SLEP': 'KC_SYSTEM_SLEEP',
    'KC_WAKE': 'KC_SYSTEM_WAKE',

    ## Consumer Page (0x0C)
    'KC_MUTE': 'KC_AUDIO_MUTE',
    'KC_VOLU': 'KC_AUDIO_VOL_UP',
    'KC_VOLD': 'KC_AUDIO_VOL_DOWN',
    'KC_MNXT': 'KC_MEDIA_NEXT_TRACK',
    'KC_MPRV': 'KC_MEDIA_PREV_TRACK',
    'KC_MSTP': 'KC_MEDIA_STOP',
    'KC_MPLY': 'KC_MEDIA_PLAY_PAUSE',
    'KC_MSEL': 'KC_MEDIA_SELECT',
    'KC_EJCT': 'KC_MEDIA_EJECT',
    'KC_CALC': 'KC_CALCULATOR',
    'KC_MYCM': 'KC_MY_COMPUTER',
    'KC_WSCH': 'KC_WWW_SEARCH',
    'KC_WHOM': 'KC_WWW_HOME',
    'KC_WBAK': 'KC_WWW_BACK',
    'KC_WFWD': 'KC_WWW_FORWARD',
    'KC_WSTP': 'KC_WWW_STOP',
    'KC_WREF': 'KC_WWW_REFRESH',
    'KC_WFAV': 'KC_WWW_FAVORITES',
    'KC_MFFD': 'KC_MEDIA_FAST_FORWARD',
    'KC_MRWD': 'KC_MEDIA_REWIND',
    'KC_BRIU': 'KC_BRIGHTNESS_UP',
    'KC_BRID': 'KC_BRIGHTNESS_DOWN',

    ## System Specific
    'KC_BRMU': 'KC_PAUSE',
    'KC_BRMD': 'KC_SCROLLLOCK',
}


## norns/lua/core/keymap/us.lua

default_keymap = {
    'SPACE': ' ',

    'A': 'a',
    'B': 'b',
    'C': 'c',
    'D': 'd',
    'E': 'e',
    'F': 'f',
    'G': 'g',
    'H': 'h',
    'I': 'i',
    'J': 'j',
    'K': 'k',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'O': 'o',
    'P': 'p',
    'Q': 'q',
    'R': 'r',
    'S': 's',
    'T': 't',
    'U': 'u',
    'V': 'v',
    'W': 'w',
    'X': 'x',
    'Y': 'y',
    'Z': 'z',

    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',

    'GRAVE': '`',
    'MINUS': '-',
    'EQUAL': '=',
    'LEFTBRACE': '[',
    'RIGHTBRACE': ']',
    'BACKSLASH': '\\',
    'SEMICOLON': ';',
    'APOSTROPHE': '\'',
    'COMMA': ',',
    'DOT': '.',
    'SLASH': '/',
}

default_keymap_shift = {
    'SPACE': ' ',

    'A': 'A',
    'B': 'B',
    'C': 'C',
    'D': 'D',
    'E': 'E',
    'F': 'F',
    'G': 'G',
    'H': 'H',
    'I': 'I',
    'J': 'J',
    'K': 'K',
    'L': 'L',
    'M': 'M',
    'N': 'N',
    'O': 'O',
    'P': 'P',
    'Q': 'Q',
    'R': 'R',
    'S': 'S',
    'T': 'T',
    'U': 'U',
    'V': 'V',
    'W': 'W',
    'X': 'X',
    'Y': 'Y',
    'Z': 'Z',

    '0': ')',
    '1': '!',
    '2': '@',
    '3': '#',
    '4': '$',
    '5': '%',
    '6': '^',
    '7': '&',
    '8': '*',
    '9': '(',

    'GRAVE': '~',
    'MINUS': '_',
    'EQUAL': '+',
    'LEFTBRACE': '{',
    'RIGHTBRACE': '}',
    'BACKSLASH': '|',
    'SEMICOLON': ':',
    'APOSTROPHE': '"',
    'COMMA': '<',
    'DOT': '>',
    'SLASH': '?',
}

default_keymap_altgr = {}
default_keymap_shift_altgr = {}

## ------------------------------------------------------------------------
## HELPER FNS

aliases = {}

def get_norns_keycode(keycode):
    global aliases
    while keycode in aliases:
        DEBUG and print('  ' + keycode + ' -> ' + aliases[keycode])
        keycode = aliases[keycode]
    if keycode in qmk_aliases:
        DEBUG and print('  ' + keycode + ' -> ' + qmk_aliases[keycode])
        keycode = qmk_aliases[keycode]
    if keycode in gmk_2_norns:
        DEBUG and print('  ' + keycode + ' -> ' + gmk_2_norns[keycode])
        return gmk_2_norns[keycode]
    else:
        DEBUG and print('  ' + 'NO MATCH!')
        pass

def escape_str(s):
    if s in ["'", '\\']:
        s = '\\' + s
    return s


## ------------------------------------------------------------------------
## MAIN

with open(args.src, 'r') as f:
    for line in f:
        DEBUG and print(line)
        match = re.match('^#define +(?P<alias>\w+) +(?P<keycode>\w+) +// +(?P<char>.)', line)
        if match:
            v = match.groupdict()
            aliases[v['alias']] = v['keycode']
            keycode = get_norns_keycode(v['keycode'])
            DEBUG and print('-------------')
            if keycode and keycode in default_keymap:
                DEBUG and print(v['keycode']  + " -> " + keycode + " = " + v['char'])
                if re.match('^[A-Z]$', v['char']):
                    default_keymap[keycode] = v['char'].lower()
                    default_keymap_shift[keycode] = v['char']
                else:
                    default_keymap[keycode] = v['char']


        shift_match = re.match('^#define +(?P<alias>\w+) +S\((?P<keycode>\w+)\) +// +(?P<char>.)', line)
        if shift_match:
            v = shift_match.groupdict()
            aliases[v['alias']] = v['keycode']
            keycode = get_norns_keycode(v['keycode'])
            DEBUG and print('-------------')
            if keycode and keycode in default_keymap_shift:
                DEBUG and print(v['keycode']  + " -> " + keycode + " = " + v['char'])
                default_keymap_shift[keycode] = v['char']

        altgr_match = re.match('^#define +(?P<alias>\w+) +ALGR\((?P<keycode>\w+)\) +// +(?P<char>.)', line)
        if altgr_match:
            v = altgr_match.groupdict()
            aliases[v['alias']] = v['keycode']
            keycode = get_norns_keycode(v['keycode'])
            if keycode:
                DEBUG and print('-------------')
                DEBUG and print(v['keycode']  + " -> " + keycode + " = " + v['char'])
                default_keymap_altgr[keycode] = v['char']

        shift_altgr_match = re.match('^#define +(?P<alias>\w+) +S\(ALGR\((?P<keycode>\w+)\)\) +// +(?P<char>.)', line)
        if shift_altgr_match:
            v = shift_altgr_match.groupdict()
            aliases[v['alias']] = v['keycode']
            keycode = get_norns_keycode(v['keycode'])
            if keycode:
                DEBUG and print('-------------')
                DEBUG and print(v['keycode']  + " -> " + keycode + " = " + v['char'])
                default_keymap_shift_altgr[keycode] = v['char']

with open(args.dest, 'w') as f:
    f.write('''

local char_modifier = require 'core/keymap/char_modifier'

local k = {}

k[char_modifier.NONE] = {}
k[char_modifier.SHIFT] = {}
''')

    if default_keymap_altgr:
        f.write('k[char_modifier.ALTGR] = {}' + "\n")
    if default_keymap_shift_altgr:
        f.write('k[char_modifier.SHIFT | char_modifier.ALTGR]] = {}' + "\n")
    f.write("\n")

    for k, v in default_keymap.items():
        k_path = '.' + k
        if re.match('^\d$', k):
            k_path = "['" + k + "']"
        if v.isascii():
            f.write( 'k[char_modifier.NONE]' + k_path + ' = ' + "'" + escape_str(v) + "'" + "\n")
    for k, v in default_keymap_shift.items():
        k_path = '.' + k
        if re.match('^\d$', k):
            k_path = "['" + k + "']"
        if v.isascii():
            f.write( 'k[char_modifier.SHIFT]' + k_path + ' = ' + "'" + escape_str(v) + "'" + "\n")
    for k, v in default_keymap_altgr.items():
        k_path = '.' + k
        if re.match('^\d$', k):
            k_path = "['" + k + "']"
        if v.isascii():
            f.write( 'k[char_modifier.ALTGR]' + k_path + ' = ' + "'" + escape_str(v) + "'" + "\n")
    for k, v in default_keymap_shift_altgr.items():
        k_path = '.' + k
        if re.match('^\d$', k):
            k_path = "['" + k + "']"
        if v.isascii():
            f.write( 'k[char_modifier.SHIFT | char_modifier.ALTGR]' + k_path + ' = ' + "'" + escape_str(v) + "'" + "\n")

    f.write('''

return k
''')
