import pathlib
def get_module_name_by_path(path, base):
    path= pathlib.Path(path)
    base= pathlib.Path(base)
    return '.'.join(path.resolve().relative_to(base.resolve()).with_suffix('').parts)

