"""
自定义异常类 - 定义应用中使用的各种异常
"""


class MenuAppException(Exception):
    """应用基础异常类"""
    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.message = message
        self.code = code or 'UNKNOWN_ERROR'


class RecipeException(MenuAppException):
    """菜谱相关异常"""
    pass


class RecipeNotFoundException(RecipeException):
    """菜谱未找到异常"""
    def __init__(self, recipe_id: int):
        super().__init__(f"菜谱未找到 (ID: {recipe_id})", 'RECIPE_NOT_FOUND')


class RecipeValidationError(RecipeException):
    """菜谱验证异常"""
    pass


class CategoryException(MenuAppException):
    """类别相关异常"""
    pass


class CategoryNotFoundException(CategoryException):
    """类别未找到异常"""
    def __init__(self, category_id: int):
        super().__init__(f"类别未找到 (ID: {category_id})", 'CATEGORY_NOT_FOUND')


class CategoryValidationError(CategoryException):
    """类别验证异常"""
    pass


class DatabaseException(MenuAppException):
    """数据库相关异常"""
    pass


class DatabaseConnectionError(DatabaseException):
    """数据库连接错误"""
    def __init__(self, db_path: str):
        super().__init__(f"无法连接数据库：{db_path}", 'DB_CONNECTION_ERROR')


class DatabaseOperationError(DatabaseException):
    """数据库操作错误"""
    pass


class FileException(MenuAppException):
    """文件相关异常"""
    pass


class FileNotFoundError(FileException):
    """文件未找到异常"""
    def __init__(self, file_path: str):
        super().__init__(f"文件未找到：{file_path}", 'FILE_NOT_FOUND')


class FileFormatError(FileException):
    """文件格式错误"""
    pass


class ImportExportException(MenuAppException):
    """导入导出异常"""
    pass


class ImportError(ImportExportException):
    """导入错误"""
    pass


class ExportError(ImportExportException):
    """导出错误"""
    pass


class ValidationException(MenuAppException):
    """验证异常基类"""
    pass


class ShareException(MenuAppException):
    """分享相关异常"""
    pass
