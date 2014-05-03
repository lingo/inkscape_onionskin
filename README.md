# Inkscape onionskin plugin (and others)

## What's in the box?

- [Onionskin plugin](#onionskin-plugin)
- [Add frame plugin](#add-frame-plugin)
- [Layers actions plugin](#layers-actions-plugin)
- [Preview plugin](#preview-plugin) **(EXPERIMENTAL)**
- [Set preview attributes plugin](#set-preview-attributes-plugin) **(EXPERIMENTAL)**

## Installation

Place the files as indicated below within your Inkscape extensions directory, then reload Inkscape. You should see new options in the menu: `Extensions > Animation > ...`


### Files to copy to extensions directory

Copy the files shown under *Requirements*, then copy files for the plugins you want to activate, as shown below.

**Note** This didn't work for me within a subdirectory of extensions, I had to put the files directly in place.

#### Requirements
- `nzgs.py`

#### Onionskin
- `nzgsonionskin.inx`
- `nzgsonionskin.py`

#### Add new frame
- `nzgsnewframe.py`
- `nsgsnewframe.inx`

#### Layers actions
- `nzgslayer.py`
- `nzgslayer.inx`

#### Others (experimental)
- `nzgspreview.py`
- `nzgspreview.inx`
- `nzgscustom.py`
- `nzgscustom.inx`

See also [Keyboard shortcuts](#user-content-keyboard-shortcuts)

### Destination folder
You will have to copy these files into Inkscape's extensions directory, which will (probably) be one of the following folders:

- *Windows*: `%APPDATA%\inkscape\extensions\` or `%ProgramFiles%\Inkscape\share\extensions`
- *Linux*: `$HOME/.config/inkscape/extensions` (or `/usr/share/inkscape/extensions`)
- *OS X*: `/Applications/Inkscape.app/Contents/Resources/extensions`

## Onionskin plugin
I wrote this to make creation of animations easier in Inkscape.

This plugin provides a method of ['onion-skinning'](http://en.wikipedia.org/wiki/Onion_skinning) using Inkscape's layer opacity.

Run the plugin and it will hide any layers above the current layer, make the current layer fully opaque and progressively fade out previous layers.

### Steps to try out the plugin

0. Create a new document in Inkscape
1. Create a basic shape
2. Open the layers palette (Menu: `Layer -> Layers...`)
3. Select the layer containing the shape you created (Typically: `Layer `)
4. Duplicate this layer above and make a change to the shape
5. Repeat the above step several times in order to have 4-5 layers
6. Now select a layer and run the plugin
7. You should now see that the other layers are 'ghosted'
8. Each time you change layers, run the plugin to onionskin previous 'frames' (i.e. layers) (see [Keyboard shortcuts](#keyboard-shortcuts) to make this easier)


## Layers actions plugin

This allows for some batch-operations on layers.  Handy when you are preparing an animation with many layers.

## Add frame plugin

This is a shortcut plugin to duplicate the topmost layer of your document, increment it's label (assuming it's a frame number), and setup onion-skinning.

## Preview plugin
This works in conjunction with the [**inkscape_reanimator**](http://github.com/lingo/inkscape_reanimator) program.
The idea is to be able to preview your animation in progress via this program.
However, this is all in very early development.  Any comments or problems, please post to the [Issues page](https://github.com/lingo/inkscape_reanimator/issues).
This plugin will temporarily show and make opaque all layers except those you have marked using the plugin below.

## Set preview attributes plugin
This works with the Preview plugin.  The idea is that you can set a certain layer (or layers) to be a background for your animation.  The inkscape_reanimator will respect this and maintain this layer visible while animating the other layers.
You may also set a layer as invisible for the animation and the inkscape_reanimator will keep it hidden.

## Keyboard shortcuts

You can assign a keyboard shortcut to these plugin to make your life easier.
To do this, you can copy the `default.xml` file from this package into the inkscape *keys* directory and change the key as desired.

The keys directory should be:

- *Windows*: `C:\Program Files\Inkscape\share\keys`
- *Linux*: `~/.config/inkscape/keys` (or `/usr/share/inkscape/keys`)
- *OS X*: `/Applications/Inkscape.app/Contents/Resources/keys`

If you already have a custom keys file, simply add the following lines at the end (as shown below) before the `</keys>` tag.

These lines bind `Alt+Shift+L` to run the plugin, showing the dialog.
`Ctrl+Alt+Shift+L` will run the plugin without showing the dialog.

~~~xml
   <bind key="l" modifiers="Alt,Shift" action="nz.geek.speak.onionskin.noprefs" display="true"/>
   <bind key="L" modifiers="Alt,Shift" action="nz.geek.speak.onionskin.noprefs" />

   <bind key="l" modifiers="Ctrl,Alt,Shift" action="nz.geek.speak.onionskin" display="true"/>
   <bind key="L" modifiers="Ctrl,Alt,Shift" action="nz.geek.speak.onionskin" />
~~~

### Actions
These are the values you can use in `action` within the keyboard shortcuts file

- `nz.geek.speak.onionskin` Onionskin plugin
- `nz.geek.speak.inkscape.layers` Layers actions plugin
- `nz.geek.speak.inkscape.newframe` New frame plugin

You may also wish to have a handy shortcut for repeating the last effect used, without showing a dialog.  This is not specific to Onionskin.

~~~xml
 <bind key="l" modifiers="Ctrl,Alt,Shift" action="EffectLast" />
 <bind key="L" modifiers="Ctrl,Alt,Shift" action="EffectLast" />
~~~

## Screenshots

### Onionskin settings
![Onionskin properties window](http://i.imgur.com/c1AXcdv.jpg)
### Layers actions settings
![Layers actions window](http://i.imgur.com/btopFr5.jpg)
