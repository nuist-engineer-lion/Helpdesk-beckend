from typing import (
    Annotated,
    Any,
    cast,
    get_args,
    get_origin,
    TypeVar,
    Union  # type: ignore  # 为了向后兼容性保留 Union 支持
)
import types
import collections.abc
from functools import reduce
import operator

def _extract_union_types(type_hint: Any) -> set[Any]:
    """
    提取联合类型中的所有具体类型
    
    参数:
        type_hint: 类型提示，可能是简单类型或复杂的联合类型
    
    返回:
        set[Any]: 包含所有具体类型的集合
    """
    result: set[Any] = set()
    
    # 获取类型的原始类型和参数
    origin = get_origin(type_hint)
    args = get_args(type_hint)
    
    # 处理联合类型
    if origin is Union or isinstance(type_hint, types.UnionType):  # type: ignore
        for arg in args:
            result.update(_extract_union_types(arg))
        return result
    
    # 处理 Annotated 类型
    if origin is Annotated:
        actual_type = args[0] if args else Any
        return _extract_union_types(actual_type)
    
    # 如果是具体类型，直接返回
    if isinstance(type_hint, type):
        result.add(type_hint)
    else:
        # 处理泛型类型（如 list[str], dict[str, int] 等）
        # 这些类型不是 type 的实例，但仍然是有效的类型
        result.add(type_hint)
    
    return result

def _check_type_compatibility(obj_type: type, target_type: Any) -> bool:
    """
    检查类型兼容性，特别处理复杂的联合类型
    
    参数:
        obj_type: 要检查的对象类型
        target_type: 目标类型（可能是复杂的联合类型）
    
    返回:
        bool: 是否兼容
    """
    # 获取类型的原始类型和参数
    origin = get_origin(target_type)
    args = get_args(target_type)
    
    # 处理联合类型
    if origin is Union or isinstance(target_type, types.UnionType):  # type: ignore
        return any(_check_type_compatibility(obj_type, arg) for arg in args)
    
    # 处理 Annotated 类型
    if origin is Annotated:
        actual_type = args[0] if args else Any
        return _check_type_compatibility(obj_type, actual_type)
    
    # 如果是具体类型，检查继承关系
    if isinstance(target_type, type):
        try:
            return issubclass(obj_type, target_type)
        except TypeError:
            return False
    
    # 其他情况返回 False
    return False

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
    
    # 处理联合类型 (Union 和 |)
    if origin is Union or isinstance(type_hint, types.UnionType):  # type: ignore  # 为了向后兼容性保留 Union 支持
        return any(enhanced_isinstance(obj, t) for t in args)
    
    # 处理 Annotated 类型
    if origin is Annotated:
        # 提取实际类型 (第一个参数)
        actual_type = args[0] if args else Any
        # 递归处理可能嵌套的 Annotated
        return enhanced_isinstance(obj, actual_type)
    
    # 处理泛型容器 (List[int], Dict[str, int] 等)
    if origin is not None and hasattr(type_hint, "__origin__"):
        # 特殊处理 type[X] 情况 - 不需要检查 isinstance(obj, type)
        if origin is type:
            # 检查是否为类型对象或泛型别名
            if isinstance(obj, type):
                # 如果参数是 Any，则只需检查是否为类型对象
                if args[0] is Any:
                    return True
                
                # 处理复杂联合类型的情况
                # 提取目标类型中的所有具体类型
                target_types = _extract_union_types(args[0])
                
                # 如果目标类型集合为空，说明是复杂的类型注解，需要特殊处理
                if not target_types:
                    # 对于复杂的联合类型，直接检查类型关系
                    return _check_type_compatibility(obj, args[0])
                
                # 检查 obj 是否是目标类型中的任一类型或其子类
                try:
                    return any(issubclass(obj, target_type) for target_type in target_types if isinstance(target_type, type))
                except TypeError:
                    # 如果 issubclass 失败，尝试用兼容性检查
                    return _check_type_compatibility(obj, args[0])
                
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

class _MutableCallableMeta(type):
    """
    MutableCallable 的元类，支持方括号语法进行类型参数化
    """
    
    def __getitem__(cls, params: Any | tuple[Any, ...]) -> Any:
        """
        支持 MutableCallable[utype, v] 语法
        
        参数:
            params: 类型参数，可能是单个类型或元组
                   - 如果是元组，则 params[0] 为 utype，params[1] 为 v
                   - 如果是单个类型，则视为 utype，v 默认为 Any
        
        返回:
            type: 可调用类型的联合
        """
        if isinstance(params, tuple):
            # 使用 cast 明确告诉类型检查器 params 的类型
            params_tuple = cast(tuple[Any, ...], params)
            if len(params_tuple) == 2:
                utype, v = params_tuple[0], params_tuple[1]
            elif len(params_tuple) == 1:
                utype, v = params_tuple[0], Any
            else:
                raise TypeError(f"MutableCallable 期望 1-2 个类型参数，得到 {len(params_tuple)} 个")
        else:
            utype, v = params, Any
        
        return reduce(operator.or_, [collections.abc.Callable[[t], v] for t in _extract_union_types(utype)])


class MutableCallable(metaclass=_MutableCallableMeta):
    """
    创建一个可变参数类型的可调用类型联合
    
    支持两种调用方式：
    1. 方括号语法：MutableCallable[utype, v] 或 MutableCallable[utype]
    2. 函数调用语法：MutableCallable(utype, v)（为了向后兼容）
    
    该类根据提供的联合类型创建一个可调用类型的联合，允许函数接受联合类型中的任意一种类型作为参数，
    并返回指定的返回值类型。
    
    功能说明:
    - 提取联合类型中的所有具体类型
    - 为每个具体类型创建对应的可调用类型 Callable[[T], V]
    - 使用 | 操作符将所有可调用类型组合成一个联合类型
    
    参数:
        utype (Any): 联合类型，包含多个可能的参数类型
                    例如: int | str | bool
        v (Any): 返回值类型，所有生成的可调用类型都将返回此类型
                例如: str, dict, Any 等。如果未提供，默认为 Any
    
    返回:
        type: 可调用类型的联合，形如:
             Callable[[T1], V] | Callable[[T2], V] | ... | Callable[[Tn], V]
             其中 T1, T2, ..., Tn 是从 utype 中提取的所有具体类型
    
    使用示例:
        >>> # 新式方括号语法（推荐）
        >>> handler_type = MutableCallable[int | str, dict]
        >>> # 或者只指定参数类型，返回值默认为 Any
        >>> handler_type = MutableCallable[int | str]
        >>> 
        >>> # 等价于: Callable[[int], dict] | Callable[[str], dict]
        >>> 
        >>> # 可以用于类型注解
        >>> def process_data(handler: MutableCallable[int | str, dict]) -> None:
        ...     result = handler(42)      # 可以传入 int
        ...     result = handler("text")  # 也可以传入 str
        ...     # result 的类型都是 dict
        
        >>> # 复杂联合类型示例
        >>> complex_type = MutableCallable[list[str] | dict[str, int] | tuple[int, ...], bool]
        >>> # 等价于:
        >>> # Callable[[list[str]], bool] | 
        >>> # Callable[[dict[str, int]], bool] | 
        >>> # Callable[[tuple[int, ...]], bool]
        
        >>> # 向后兼容的函数调用语法
        >>> legacy_type = MutableCallable(int | str, dict)
    
    实现原理:
        1. 使用元类 _MutableCallableMeta 支持方括号语法
        2. 使用 _extract_union_types() 函数提取联合类型中的所有具体类型
        3. 为每个具体类型 t 创建 collections.abc.Callable[[t], v]
        4. 使用 reduce(operator.or_, ...) 将所有可调用类型用 | 操作符组合
    
    注意事项:
        - 如果 utype 不是联合类型，类仍会正确处理，返回单一的可调用类型
        - 返回值类型 v 对所有生成的可调用类型都是相同的
        - 生成的类型可以用于类型注解和运行时类型检查
        - 推荐使用新式的方括号语法，函数调用语法保留用于向后兼容
        
    相关函数:
        - _extract_union_types(): 提取联合类型中的具体类型
        - enhanced_isinstance(): 增强的类型检查函数
    """
    
    def __new__(cls, utype: Any, v: Any = Any) -> Any:
        """
        为了向后兼容，支持函数调用语法
        
        参数:
            utype (Any): 联合类型
            v (Any): 返回值类型，默认为 Any
        
        返回:
            type: 可调用类型的联合
        """
        return reduce(operator.or_, [collections.abc.Callable[[t], v] for t in _extract_union_types(utype)])
