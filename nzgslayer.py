#
# @author Luke Hudson <github@speak.geek.nz>
# @license GPLv2 See LICENCE file
#
import sys, inkex, simplestyle
import gettext
_ = gettext.gettext
import traceback
import nzgs

class NZGSLayer(nzgs.NZGSEffect):
    # DEBUG = True

    def __init__(self):
        nzgs.NZGSEffect.__init__(self)
        self.OptionParser.add_option("--layers-show",
                        type="string", dest="show_all", default="ignore",
                        help="Show all layers")
        self.OptionParser.add_option("--layers-lock",
                        type="string", dest="lock_all", default="ignore",
                        help="Lock all layers")
        self.OptionParser.add_option("--layers-change-opacity",
                        type="inkbool", dest="change_opacity", default=False,
                        help="Affect opacity")
        self.OptionParser.add_option("--opacity-tab",
                        action="store", type="string", dest="tab",
                        help="This is ignored")
        self.OptionParser.add_option("--layers-opacity",
                        type="int", dest="opacity", default=100,
                        help="If opacity is affected, change it to this value")
        self.OptionParser.add_option("--layers-recursive",
                        type="inkbool", dest="recursive", default=False,
                        help="Act on sublayers too")
        self.OptionParser.add_option("--layers-relabel",
                        type="inkbool", dest="rename", default=False,
                        help="Rename layers sequentially")

    def effect(self):
        self.debug(self.options)
        change_vis     = self.options.show_all != 'ignore'
        change_lock    = self.options.lock_all != 'ignore'
        change_opacity = self.options.change_opacity

        show_all       = self.options.show_all == "show"
        lock_all       = self.options.lock_all == "lock"

        layers         = self.get_layers(recursive = self.options.recursive)
        frameLabel     = -1
        for layer in layers:
            if change_vis:
                if show_all:
                    self.show_layer(layer)
                else:
                    self.hide_layer(layer)
            if change_lock:
                if lock_all:
                    self.set_layer_lock(layer)
                else:
                    self.set_layer_lock(layer, unlock=True)

            if change_opacity:
                self.modify_layer_style(layer, {"opacity": self.options.opacity / 100.0})

            if self.options.rename:
                if self.is_toplevel_layer(layer):
                    frameLabel += 1
                name = '%04d' % frameLabel
                if not self.is_toplevel_layer(layer) and self.options.recursive:
                    depth = len(self.get_selector_path(layer)) - 1
                    name = name + '.' + str(depth)
                key = inkex.addNS('label', 'inkscape')
                layer.attrib[key] = name

if __name__ == '__main__':
    try:
        e = NZGSLayer()
        e.affect()
    except:
        inkex.errormsg("Exception: %s" % traceback.format_exc())
