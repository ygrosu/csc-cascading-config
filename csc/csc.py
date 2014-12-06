
__author__ = 'yairgrosu'

# import yaml
from copy import deepcopy


class CascadingConfig:
    def __init__(self, items=None):
        self.__data_ = items if isinstance(items, dict) else dict()


    def add_dicts(self, items):
        if isinstance(items, dict):
            for item in items:
                if item in self.__data_:
                    self.__data_[item].update(items[item])
                else:
                    self.__data_[item] = items[item]
        else:
            raise ValueError("type:[%s],  %s"%(type(items), items))
    def get_dict(self, key):
        return self._get_recursive_dict(key)

    def _get_recursive_dict(self, key):
        kv = deepcopy(self.__data_[key])

        based_on = kv.pop('based_on') if 'based_on' in kv else None
        if based_on and based_on != key:
            (ref, ops) = (based_on, list()) if isinstance(based_on, str) else (based_on[0], based_on[1]) if isinstance(based_on, list) else None
            if ref is None:
                raise(ValueError("Bad based_on value: %s"%based_on))
            base = self._get_recursive_dict(ref)
            base.update(kv)
            for op in ops:
                base = op(base)
            return base
        return kv


def _migrate(wk_dest, path, type_to_create=None):
    (item, next_step) = (wk_dest, None)
    for step in path.split('/'):
        if next_step is None:
            next_step = step
        elif next_step not in item:
            item[next_step] = dict()
            item = item[next_step]
            next_step = step
        else:
            item = item[next_step]
            next_step = step
    else:
        if next_step not in item:
            if type_to_create:
                item[next_step] = type_to_create()
    return item, next_step



class OpBase:
    def __call__(self, dest):
        wk_dest = deepcopy(dest)
        (key, vals) = (self.__dict__.items()[0]) if 'path' not in self.__dict__ else (self.path, self.values if 'values' in self.__dict__ else None)
        item, next_step = _migrate(wk_dest, key, type_to_create=list)
        self.execute(item, next_step, vals)
        return wk_dest

    def execute(self, item, next_step, vals=None):
        raise(TypeError("should not get to OpBase execute"))



class OpAdd(OpBase):
    def execute(self, item, next_step, vals=None):
        item[next_step].extend(vals)


class OpDel(OpBase):
    def execute(self, item, next_step, vals=None):
        if vals is None:
            item.pop(next_step)
        else:
            for v in vals:
                if v in item[next_step]:
                    item[next_step].remove(v)

