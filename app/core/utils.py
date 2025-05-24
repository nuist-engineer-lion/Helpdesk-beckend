from typing import (
    Annotated,
    Any,
    get_args,
    get_origin,
    TypeVar
)
import types
import collections.abc

def enhanced_isinstance(obj: Any, type_hint: Any) -> bool:
    """
    增强版 isinstance() 函数，支持更复杂的类型检查
    
    功能:
    - 支持常规类型检查 (如 isinstance(obj, int))
    - 支持 Annotated 类型 (如 Annotated[int, ...])
    - 支持 Union/| 类型 (如 int | str)
    - 支持泛型容器 (如 list[int], dict[str, int])
    - 支持嵌套泛型类型 (如 list[type[type]], dict[str, type[Any]])
    - 支持 type[X] 泛型别名检查 (如 type[str], type[type])
    - 支持 TypeVar
    - 支持抽象基类 (如 collections.abc.Sequence)
    
    特殊支持:
    - 正确处理 types.GenericAlias 对象 (如 type[str] 匹配 type[type])
    - 支持多层嵌套的类型检查
    - 兼容 Python 3.10+ 的新式联合类型语法
    
    参数:
        obj: 要检查的对象
        type_hint: 类型提示 (可以是普通类型或复杂类型注解)
    
    返回:
        bool: 对象是否符合类型提示
        
    示例:
        >>> enhanced_isinstance([type[str], type[int]], list[type[type]])
        True
        >>> enhanced_isinstance(42, int | str)
        True
        >>> enhanced_isinstance([1, "2", 3], list[int | str])
        True
    """
    # 处理 TypeVar
    if isinstance(type_hint, TypeVar):
        return True  # TypeVar 不做具体检查，或者可以添加约束检查
    
    # 获取类型的原始类型和参数
    origin = get_origin(type_hint)
    args = get_args(type_hint)
    
    # 递归处理复杂类型
    if origin is not None:
        if origin is Annotated:
            # 提取实际类型 (第一个参数)
            actual_type = args[0] if args else Any
            # 递归处理可能嵌套的 Annotated
            return enhanced_isinstance(obj, actual_type)
        
    # 处理联合类型 (|)
    if isinstance(type_hint, types.UnionType):
        return any(enhanced_isinstance(obj, t) for t in args)
    
    # 处理泛型容器 (List[int], Dict[str, int] 等)
    if origin is not None and hasattr(type_hint, "__origin__"):
        # 特殊处理 type[X] 情况 - 不需要检查 isinstance(obj, type)
        if origin is type:
            # 检查是否为类型对象或泛型别名
            if isinstance(obj, type):
                # 如果参数是 Any，则只需检查是否为类型对象
                if args[0] is Any:
                    return True
                # 否则检查是否匹配指定类型
                return obj is args[0]
            elif hasattr(obj, '__origin__') and get_origin(obj) is type:
                # 处理 type[X] 泛型别名的情况
                if args[0] is Any:
                    return True
                # 检查泛型别名的参数是否匹配
                obj_args = get_args(obj)
                if obj_args:
                    # 如果期望的参数也是 type，那么需要检查 obj_args[0] 是否为类型对象
                    if args[0] is type:
                        return isinstance(obj_args[0], type)
                    else:
                        return enhanced_isinstance(obj_args[0], args[0])
                return False
            return False
        
        # 对于其他容器，先检查是否是容器的实例
        if not isinstance(obj, origin):
            return False
        
        # 特殊处理常见容器
        if origin in (list, collections.abc.Sequence):
            return all(enhanced_isinstance(x, args[0]) for x in obj)
        elif origin in (dict, collections.abc.Mapping):
            return (
                all(enhanced_isinstance(k, args[0]) for k in obj.keys()) and
                all(enhanced_isinstance(v, args[1]) for v in obj.values())
            )
        elif origin is tuple:
            # 处理空元组类型 tuple[()]
            if not args:
                return len(obj) == 0
            elif len(args) == 2 and args[1] == ...:  # 不定长元组 Tuple[T, ...]
                return all(enhanced_isinstance(x, args[0]) for x in obj)
            else:  # 定长元组 Tuple[T1, T2, ...]
                return (
                    len(obj) == len(args) and
                    all(enhanced_isinstance(x, t) for x, t in zip(obj, args))
                )
        elif origin is set:
            return all(enhanced_isinstance(x, args[0]) for x in obj)
        
        # 其他泛型类型暂不深入检查
        return True
    
    # 特殊处理 Any 类型，Any 匹配任何类型
    if type_hint is Any:
        return True

    # 特殊处理 None (因为 isinstance(None, type(None)) 比 isinstance(None, None) 更好)
    if type_hint is type(None):
        return obj is None
    
    # 普通类型检查
    try:
        return isinstance(obj, type_hint)
    except TypeError:
        # 处理一些特殊情况，比如抽象基类
        if isinstance(type_hint, type):
            return isinstance(obj, type_hint)
        return False
