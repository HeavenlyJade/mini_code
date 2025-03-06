from kit.domain.field import ExtendedEnum

__all__ = ['EnumService']


class EnumService:
    def list(self, **args):
        enum_map = dict()
        for sub_class in ExtendedEnum.get_subclasses():
            try:
                name = ''.join(
                    ['_' + i.lower() if i.isupper() else i for i in sub_class.__name__]
                ).lstrip('_')
                enum_map[name] = dict(
                    maps={e.name: e.value for e in sub_class},
                    description=sub_class.desc(),
                )
            except AttributeError:
                ...
        return enum_map
