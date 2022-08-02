
from sqlmodel import SQLModel
__all__ = ["create_schema","drop_all_schema"]
from testspace.log import logger
def create_schema(engine):
    import testspace
    from testspace.utils.libautoimport import Module
    _models = Module(testspace)["models"]
    for i in _models.iter_children():
        i.import_module()
        logger.info(f"add schema module [bold blue]{i.module_path}[/bold blue]")
    SQLModel.metadata.create_all(bind=engine,checkfirst=True)
def drop_all_schema(engine):
    SQLModel.metadata.drop_all(engine)
