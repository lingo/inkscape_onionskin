#
# @author Luke Hudson <github@speak.geek.nz>
# @license GPLv2 See LICENCE file
#
import sys
sys.path.append("/usr/share/inkscape/extensions")
import inkex, simplestyle
import gettext
_ = gettext.gettext
import traceback
import nzgs
import lxml.etree as etree
from cStringIO import StringIO


class NZGSCustom(nzgs.NZGSEffect):
    # DEBUG = True

    def __init__(self):
        nzgs.NZGSEffect.__init__(self)
        self.OptionParser.add_option("--background",
                        type="inkbool", dest="background", default=False,
                        help="Set layer as background for animation")
        self.OptionParser.add_option("--invisible",
                        type="inkbool", dest="invisible", default=False,
                        help="Set layer as invisible in the animation")

    def reparse(self):
        """Filter and reParse document in specified file or on stdin"""
        try:
            try:
                stream = open(file,'r')
            except:
                stream = open(self.svg_file,'r')
        except:
            stream = sys.stdin
        data          = stream.read()
        data          = data.replace('<svg', "<svg\nxmlns:nzgs=\"%s\" " % self.NSS['nzgs'])
        self.document = etree.parse(StringIO(data)) #element.getroottree()
        self.getposinlayer()
        self.getselected()
        self.getdocids()
        stream.close()

    def effect(self):
        if not self.document.getroot().nsmap.has_key('nzgs'):
            self.reparse()
        # self.document.getroot().attrib['xmlns:nzgs'] = self.NSS['nzgs']
        # attr = self.addNS('background','nzgs')
        # self.debug(attr)
        layer = self.current_layer
        if (layer.tag == self.addNS('g','svg')):
            if self.options.background:
                self.set_attr(layer, 'nzgs:background', 'true');
            elif self.options.invisible:
                self.set_attr(layer, 'nzgs:invisible', 'true');
        else:
            self.debug("Please select a layer to use as background for animation")

if __name__ == '__main__':
    try:
        e = NZGSCustom()
        e.affect()
    except:
        inkex.errormsg("Exception: %s" % traceback.format_exc())
