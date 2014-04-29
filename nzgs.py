#
# @author Luke Hudson <github@speak.geek.nz>
# @license GPLv2 See LICENCE file
#
import sys, inkex, simplestyle
import gettext
_ = gettext.gettext


class NZGSEffect(inkex.Effect,object):
    DEBUG = False
    DEBUG_PRINT = False

    def __init__(self):
        inkex.Effect.__init__(self)

    def debug(self, arg):
        if self.DEBUG:
            inkex.debug(arg)
        if self.DEBUG_PRINT:
            print arg

    def effect(self):
        pass # override in sub-classes

    def set_current_layer(self, layer):
        viewData = self.document.xpath('//sodipodi:namedview', namespaces=inkex.NSS)[0]
        self.set_attr(viewData, 'inkscape:current-layer', layer.attrib['id'])

    def get_layers(self, recursive=False):
        separator = ''
        if recursive:
            separator = '/'
        xpath = '/svg:svg/%ssvg:g[@inkscape:groupmode="layer"]' % (separator)
        layers = self.document.xpath(xpath, namespaces=inkex.NSS)
        return layers

    def friendly_tag(self, name):
        for k,v in inkex.NSS.items():
            name = name.replace('{%s}' % v, k + ':')
        return name

    def get_attr(self, obj, attr):
        try:
            ns,attr = attr.split(':')
            attr = inkex.addNS(attr, ns)
        except ValueError, e:
            pass
        return obj.attrib[attr]

    def set_attr(self, obj, attr, val):
        try:
            ns,attr = attr.split(':')
            attr = inkex.addNS(attr, ns)
        except ValueError, e:
            pass
        obj.attrib[attr] = str(val)

    def get_layer_name(self, layer):
        return layer.attrib[inkex.addNS('label', 'inkscape')]

    def get_selector_path(self, item):
        path = [self.friendly_tag(ans.tag) for ans in item.iterancestors()]
        path.reverse()
        return path

    def get_selector(self, item):
        path = [self.friendly_tag(ans.tag) for ans in item.iterancestors()]
        path.reverse()
        return ' > '.join(path)

    def is_toplevel_layer(self, layer):
        return layer.getparent and layer.getparent().tag == inkex.addNS('svg','svg')

    def modify_layer_style(self, layer, style):
        if (layer.attrib.has_key('style')):
            currentStyle = simplestyle.parseStyle(layer.attrib['style'])
            for k,v in style.items():
                if v == None:
                    if currentStyle.has_key(k):
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
