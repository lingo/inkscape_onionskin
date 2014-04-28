#
# @author Luke Hudson <github@speak.geek.nz>
# @license GPLv2 See LICENCE file
#
import sys, inkex, simplestyle
import gettext
import nzgs
_ = gettext.gettext


class Onionskin(nzgs.NZGSEffect):
    def __init__(self):
        nzgs.NZGSEffect.__init__(self)
        self.OptionParser.add_option("--onion-layers",
                        type="int", dest="onion_layers", default=2, 
                        help="# of visible onion skin layers")
        self.OptionParser.add_option("--onion-base",
                        type="int", dest="onion_base", default=70, 
                        help="Opacity(%) of first onionskin layer")
        self.OptionParser.add_option("--onion-clear",
                        type="inkbool", dest="onion_clear", default=False, 
                        help="Overrides other options and removes all onionskins")


    def effect(self):
        layers = self.get_layers()
        current = self.current_layer
        if current is None:
            self.debug('No current_layer found')
            return
        if current.tag != inkex.addNS('g', 'svg'):
            self.debug("current_layer wasn't a svg:g tag (Found %s)" % current.tag)
            return

        if self.options.onion_clear:
            for l in layers:
                self.show_layer(l, full_opaque=True)
                self.set_layer_lock(l, unlock=True)
            return

        # Determine the index of the current layer
        current_index = -1
        for i in range(0, len(layers)):
            layer = layers[i]
            if layer == current:
                current_index = i

        self.debug("Luke: %d layers, current is %d : %s" % (len(layers), current_index, [self.get_layer_name(x) for x in layers]))

        if current_index < 0:
            return

        # Hide any layers above the current one
        for i in range(len(layers)-1, current_index, -1):
            self.set_layer_opacity(layers[i], 1)
            self.hide_layer(layers[i])
            self.set_layer_lock(layers[i])

        self.show_layer(current, full_opaque=True)
        self.set_layer_lock(current, unlock=True)


        # Fade out layers below current
        onion_base  = self.options.onion_base / 100.0
        opacity     = onion_base
        fade_factor = onion_base / (self.options.onion_layers)

        self.debug("start at index %d, %.2f, fading by %.2f" % (current_index-1,opacity, fade_factor))

        for i in range(current_index-1, -1, -1):
            layer = layers[i]
            self.set_layer_lock(layer)
            if opacity <= 0:
                self.set_layer_opacity(layer, 1)
                self.hide_layer(layer)
            else:
                self.set_layer_opacity(layer, opacity)
                self.show_layer(layer)
            opacity -= fade_factor

if __name__ == '__main__':
    try:
        e = Onionskin()
        e.affect()
    except:
        inkex.errormsg("Exception: %s" % sys.exc_info()[0])
