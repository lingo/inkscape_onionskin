# Inkscape onionskin

## Author
Luke Hudson <github@speak.geek.nz>

## Installation

Place the following *.idx* and *.py* files from this package within your Inkscape extensions directory.
Then reload Inkscape. You should see new options in the menus: `Extensions > Animation > Onionskin`
### Files to copy to extensions directory
**Note** This didn't work for me within a subdirectory of extensions, I had to put the files directly in place.

- `nzgsonionskin.idx`
- `nzgsonionskin.py`

See also [Keyboard shortcuts](#user-content-keyboard-shortcuts)

This is probably one of the following:
- *Windows*: `C:\Program Files\Inkscape\share\extensions`
- *Linux*: `~/.config/inkscape/extensions` (or `/usr/share/inkscape/extensions`)
- *OS X*: `/Applications/Inkscape.app/Contents/Resources/extensions`

## Usage
I wrote this to make creation of animations easier in Inkscape.

This plugin provides a method of ['onion-skinning'](http://en.wikipedia.org/wiki/Onion_skinning) using Inkscape's layer opacity.

Run the plugin and it will hide any layers above the current layer, make the current layer fully opaque and progressively fade out previous layers.

## Keyboard shortcuts

You can assign a keyboard shortcut to this plugin to make your life easier.
To do this, you can copy the `default.xml` file from this package into the inkscape *keys* directory and change the key as desired.

The keys directory should be:

- *Windows*: `C:\Program Files\Inkscape\share\keys`
- *Linux*: `~/.config/inkscape/keys` (or `/usr/share/inkscape/keys`)
- *OS X*: `/Applications/Inkscape.app/Contents/Resources/keys`

If you already have a custom keys file, simply add two lines at the end (as shown below) before the `</keys>` tag.


~~~xml
   <bind key="l" modifiers="Alt,Shift" action="nz.geek.speak.animation" display="true"/>
   <bind key="L" modifiers="Alt,Shift" action="nz.geek.speak.animation" />
~~~

You may also wish to have a handy shortcut for repeating the last extension effect.  This is handy for onionskin as it doesn't show the dialog again.

~~~xml
 <bind key="l" modifiers="Ctrl,Alt,Shift" action="EffectLast" />
 <bind key="L" modifiers="Ctrl,Alt,Shift" action="EffectLast" />
~~~

## Screenshots

![Onionskin properties window](http://i.imgur.com/c1AXcdv.jpg)
