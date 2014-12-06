__author__ = 'yairgrosu'

import yaml
from csc import CascadingConfig, OpAdd, OpDel


class YamlCascadingConfig(CascadingConfig):
    def __init__(self, text=None, flname=None):
        CascadingConfig.__init__(self )

        if isinstance(text, str) and len(text) > 0:
            self.add_dicts(yaml.load(text))
        if isinstance(flname, str):
            self.add_dicts(yaml.load(open(flname).read()))


class YamlOpAdd(OpAdd, yaml.YAMLObject):
    yaml_tag = u'!Add'


class YamlOpDel(OpDel, yaml.YAMLObject):
    yaml_tag = u'!Del'
