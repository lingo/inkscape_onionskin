#
# @author Luke Hudson <github@speak.geek.nz>
# @license GPLv2 See LICENCE file
#
import sys, inkex, simplestyle
import gettext
_ = gettext.gettext


class Onionskin(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--onion-layers",
                        type="int", dest="onion_layers", default=2, 
                        help="# of visible onion skin layers")
        self.OptionParser.add_option("--onion-base",
                        type="int", dest="onion_base", default=70, 
                        help="Opacity(%) of first onionskin layer")
        self.OptionParser.add_option("--onion-clear",
                        type="inkbool", dest="onion_clear", default=False, 
                        help="Overrides other options and removes all onionskins")

    def debug(self, arg):
        # print arg
        # return inkex.debug(arg)
        pass

    def effect(self):
        layers = self.document.xpath('/svg:svg/svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
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

    def get_layer_name(self, layer):
        return layer.attrib[inkex.addNS('label', 'inkscape')]

    def modify_layer_style(self, layer, style):
        if (layer.attrib.has_key('style')):
            currentStyle = simplestyle.parseStyle(layer.attrib['style'])
            for k,v in style.items():
                if v == None and currentStyle.has_key(k):
                    del currentStyle[k]
                else:
                    currentStyle[k] = style[k]
            style = currentStyle
        layer.attrib['style'] = simplestyle.formatStyle(style)

    def set_layer_opacity(self, layer, opacity):
        self.debug('set_layer_opacity "%s" %.2f' % (self.get_layer_name(layer), opacity))
        self.modify_layer_style(layer, {"opacity": opacity})

    def set_layer_lock(self, layer, unlock=False):
        insensitive = inkex.addNS('insensitive', 'sodipodi')
        if unlock:
            try:
                del layer.attrib[insensitive]
            except KeyError, e:
                pass
        else:
            layer.attrib[insensitive] = 'true'


    def hide_layer(self, layer):
        self.debug('hide_layer "%s"' % self.get_layer_name(layer))
        self.modify_layer_style(layer, {"display": 'none'})

    def show_layer(self, layer, full_opaque=False):
        self.debug('show_layer "%s"' % self.get_layer_name(layer))
        style = {"display": None}
        if full_opaque:
            style['opacity'] = 1
        self.modify_layer_style(layer, style)

if __name__ == '__main__':
    try:
        e = Onionskin()
        e.affect()
    except:
        inkex.errormsg("Exception: %s" % sys.exc_info()[0])
