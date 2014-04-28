#
# @author Luke Hudson <github@speak.geek.nz>
# @license GPLv2 See LICENCE file
#
import traceback, copy
import sys, inkex, simplestyle
import gettext
import nzgs
_ = gettext.gettext
import nzgsonionskin as nzgso


class NZGSNewFrame(nzgso.Onionskin):
    def __init__(self):
        nzgso.Onionskin.__init__(self)

    # Copied from pathmodifier.py and hacked at
    def clone_layer(self, nodes, new_parent):
        clones={}
        for id,node in nodes.iteritems():
            clone = copy.deepcopy(node)
            myid  = node.id
            clone.set("id", self.uniqueId(myid))
            new_parent().append(clone)
            clones[clone.get("id")]=clone
        return(clones)

    def add_frame(self):
        ''' ref_layer is the layer we will duplicate '''
        layers    = self.get_layers()
        lastLayer = layers[-1]
        children  = lastLayer.getchildren()
        newLayer  = copy.deepcopy(lastLayer)
        label     = self.get_attr(lastLayer, 'inkscape:label')
        try:
            label = int(label) + 1
        except ValueError, e:
            label = "0"
        self.set_attr(newLayer, 'inkscape:label', label)
        self.set_attr(newLayer, 'id', 'layer%d' % len(layers))
        lastLayer.getparent().append(newLayer)
        self.set_current_layer(newLayer)
        self.current_layer = newLayer

    def effect(self):
        self.add_frame()
        # Call superclass method with sensible defaults
        self.options.onion_clear  = False
        self.options.onion_base   = 50
        self.options.onion_lock   = True
        self.options.onion_layers = 2
        super(NZGSNewFrame, self).effect()


if __name__ == '__main__':
    try:
        e = NZGSNewFrame()
        e.affect()
    except:
        inkex.errormsg("Exception: %s" % traceback.format_exc())