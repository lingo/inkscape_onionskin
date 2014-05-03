#
# @author Luke Hudson <github@speak.geek.nz>
# @license GPLv2 See LICENCE file
#
import sys,os
import subprocess
import tempfile
sys.path.append("/usr/share/inkscape/extensions")
import inkex, simplestyle
import gettext
_ = gettext.gettext
import traceback
import nzgs

class NZGSPreview(nzgs.NZGSEffect):
    # DEBUG = True

    def __init__(self):
        nzgs.NZGSEffect.__init__(self)
        self.OptionParser.add_option("--preview-path",
                        type="string", dest="path", default="/home/lucas/code/inkscape/inkscape_reanimator/build/releases/inkscape_reanimator/linux64/inkscape_reanimator/inkscape_reanimator",
                        help="Path to inkscape_reanimator")
        self.savelayer = {}

    def prep_layers(self):
        for layer in self.get_layers():
            self.savelayer[layer.attrib['id']] = {
                "style": self.get_layer_style(layer),
                "locked": self.get_layer_lock(layer)
            }
            bg_key       = self.addNS('background','nzgs')
            invis_key    = self.addNS('invisible','nzgs')
            is_bg        = layer.attrib.has_key(bg_key) and layer.attrib[bg_key] == 'true'
            is_invis     = layer.attrib.has_key(invis_key) and layer.attrib[invis_key] == 'true'
            if is_invis:
                self.hide_layer(layer)
            elif not is_bg:
                self.show_layer(layer, full_opaque = True)

    def restore_layers(self):
        for layer in self.get_layers():
            saved = self.savelayer[layer.attrib['id']]
            self.modify_layer_style(layer, saved['style'])
            self.set_layer_lock(layer, saved['locked'])

    def effect(self):
        self.prep_layers()

        svgFileDesc, svgFile = tempfile.mkstemp(suffix=".svg", prefix="nzgs__")
        self.document.write(os.fdopen(svgFileDesc, "wb"))

        cmd = self.options.path + ' ' + svgFile
        self.debug(cmd)
        proc = subprocess.Popen([cmd],
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_value, stderr_value = proc.communicate()
        self.restore_layers()

if __name__ == '__main__':
    try:
        e = NZGSPreview()
        e.affect()
    except:
        inkex.errormsg("Exception: %s" % traceback.format_exc())
