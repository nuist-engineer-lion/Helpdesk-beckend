from collections.abc import Callable
from typing import TypeVar, Generic, get_args, get_origin

# 创建一个增强版的 Callable 类型容器
def MultiCallable(param_types, return_type):
    """
    自动将联合参数类型拆分成多个 Callable 的联合
    
    例如: MultiCallable[str | int, None] 
    等价于: Callable[[str], None] | Callable[[int], None]
    """
    if get_origin(param_types) is type(str | int):  # 检查是否为联合类型
        # 获取联合类型中的所有类型
        types = get_args(param_types)
        # 为每个类型创建一个 Callable，然后用 | 连接
        callables = [Callable[[t], return_type] for t in types]
        # 使用 reduce 将多个类型用 | 连接
        from functools import reduce
        import operator
        return reduce(operator.or_, callables)
    else:
        # 如果不是联合类型，直接返回普通的 Callable
        return Callable[[param_types], return_type]

def A(func: MultiCallable(str | int, None)):
    return func

@A
def B(e: str):
    pass
