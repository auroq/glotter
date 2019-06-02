def enum_from_string(name, enum_cls):
    for i in enum_cls:
        if name == i.name.lower():
            return i
    raise KeyError(f'{enum_cls.__name__} does not contain name "{name}"')
