from webargs.fields import DelimitedList, List


def patched_field2parameter(self, field, *, name, location):
    ret = {'in': location, 'name': name, 'required': field.required}

    prop = self.field2property(field)
    multiple = isinstance(field, List)

    if self.openapi_version.major < 3:
        if multiple:
            ret['collectionFormat'] = 'multi'
        ret.update(prop)
    else:
        if multiple:
            ret['explode'] = True
            ret['style'] = 'form'
        if isinstance(field, DelimitedList):
            ret['explode'] = False
        if prop.get('description', None):
            ret['description'] = prop.pop('description')
        ret['schema'] = prop
    return ret
