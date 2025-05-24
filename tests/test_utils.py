import pytest
from collections.abc import Sequence
from typing import (
    Annotated,
    Any,
    TypeVar
)
from app.core.utils import enhanced_isinstance

def test_basic_types():
    """测试基本类型检查"""
    assert enhanced_isinstance(42, int)
    assert enhanced_isinstance("hello", str)
    assert enhanced_isinstance(3.14, float)
    assert enhanced_isinstance(True, bool)
    assert enhanced_isinstance(None, type(None))
    assert not enhanced_isinstance(42, str)
    assert not enhanced_isinstance("hello", int)

def test_annotated_types():
    """测试注解类型检查"""
    # 基础注解
    assert enhanced_isinstance(42, Annotated[int, "positive"])
    assert enhanced_isinstance("hello", Annotated[str, "non-empty"])
    
    # 嵌套注解
    assert enhanced_isinstance(42, Annotated[Annotated[int, "positive"], "validated"])
    assert enhanced_isinstance(42, Annotated[Annotated[Annotated[int, "min"], "max"], "range"])
    
    # 带注解的容器
    assert enhanced_isinstance([1, 2, 3], list[Annotated[int, "positive"]])
    assert enhanced_isinstance({"a": 1}, dict[str, Annotated[int, "non-negative"]])

def test_union_types():
    """测试联合类型检查"""
    # Python 3.10+ 语法
    assert enhanced_isinstance(42, int | str)
    assert enhanced_isinstance("hello", int | str)
    assert not enhanced_isinstance(3.14, int | str)
    
    # 嵌套联合类型
    complex_type = list[int | str] | dict[str, float | int]
    assert enhanced_isinstance([1, "hello", 2], complex_type)
    assert enhanced_isinstance({"a": 1, "b": 3.14}, complex_type)
    assert not enhanced_isinstance([1.0, 2.0], complex_type)

def test_container_types():
    """测试容器类型检查"""
    # 列表
    assert enhanced_isinstance([1, 2, 3], list[int])
    assert not enhanced_isinstance([1, "2", 3], list[int])
    
    # 字典
    assert enhanced_isinstance({"a": 1, "b": 2}, dict[str, int])
    assert not enhanced_isinstance({"a": 1, "b": "2"}, dict[str, int])
    
    # 集合
    assert enhanced_isinstance({1, 2, 3}, set[int])
    assert not enhanced_isinstance({1, "2", 3}, set[int])
    
    # 元组
    assert enhanced_isinstance((1, "hello", True), tuple[int, str, bool])
    assert not enhanced_isinstance((1, "hello"), tuple[int, str, bool])
    
    # 不定长元组
    assert enhanced_isinstance((1, 2, 3), tuple[int, ...])
    assert not enhanced_isinstance((1, "2", 3), tuple[int, ...])

def test_nested_container_types():
    """测试嵌套容器类型检查"""
    # 嵌套列表
    assert enhanced_isinstance([[1, 2], [3, 4]], list[list[int]])
    assert not enhanced_isinstance([[1, "2"], [3, 4]], list[list[int]])
    
    # 复杂嵌套
    complex_dict: dict[str, list[int] | list[tuple[int, str]] | set[int | str | float]] = {
        "nums": [1, 2, 3],
        "pairs": [(1, "one"), (2, "two")],
        "mixed": {1, "two", 3.0}
    }
    assert enhanced_isinstance(
        complex_dict,
        dict[str, list[int] | list[tuple[int, str]] | set[int | str | float]]
    )

def test_type_var():
    """测试类型变量"""
    T = TypeVar('T')
    assert enhanced_isinstance(42, T)
    assert enhanced_isinstance("hello", T)
    assert enhanced_isinstance([1, 2, 3], T)

def test_abstract_base_classes():
    """测试抽象基类"""
    # 序列类型
    assert enhanced_isinstance([1, 2, 3], Sequence[int])
    assert enhanced_isinstance((1, 2, 3), Sequence[int])
    assert not enhanced_isinstance({1, 2, 3}, Sequence[int])

def test_edge_cases():
    """测试边缘情况"""
    # Any 类型
    assert enhanced_isinstance(42, Any)
    assert enhanced_isinstance("hello", Any)
    assert enhanced_isinstance(None, Any)
    
    # Optional 类型
    assert enhanced_isinstance(42, int | None)
    assert enhanced_isinstance(None, int | None)
    assert not enhanced_isinstance("42", int | None)
    
    # 空元组
    assert enhanced_isinstance((), tuple[()])
    assert not enhanced_isinstance((1,), tuple[()])
    
    # 复杂嵌套类型
    complex_type = list[dict[str, (int | list[Annotated[str, "metadata"]] | None)]]
    valid_data: list[dict[str, int | list[str] | None]] = [{"key": None}, {"key": 42}, {"key": ["hello", "world"]}]
    assert enhanced_isinstance(valid_data, complex_type)
    
    invalid_data = [{"key": 3.14}]  # float 不是允许的类型
    assert not enhanced_isinstance(invalid_data, complex_type)

def test_custom_types():
    """测试自定义类型"""
    class CustomType:
        pass
    
    class SubType(CustomType):
        pass
    
    obj = SubType()
    assert enhanced_isinstance(obj, CustomType)
    assert enhanced_isinstance(obj, SubType)
    assert not enhanced_isinstance(42, CustomType)

def test_type_nested():
    """测试 type[] 的嵌套情况"""
    # 基本 type[] 测试
    assert enhanced_isinstance(str, type[str])
    assert not enhanced_isinstance(int, type[str])
    assert enhanced_isinstance(int, type[int])
    
    # 容器中的 type[] 测试
    type_list: list[type[Any]] = [str, int]
    assert enhanced_isinstance(type_list, list[type])
    assert enhanced_isinstance(type_list, list[type[Any]])
    
    # 特定类型的列表测试
    str_type_list: list[type[str]] = [str]
    assert enhanced_isinstance(str_type_list, list[type[str]])
    assert not enhanced_isinstance([int], list[type[str]])
    
    # 字典中的 type[] 测试
    type_dict: dict[str, type[Any]] = {"string": str, "integer": int}
    assert enhanced_isinstance(type_dict, dict[str, type])
    assert enhanced_isinstance(type_dict, dict[str, type[Any]])
    
    # 多层嵌套测试
    nested_types: list[type[type]] = [type[str], type[int]]
    assert enhanced_isinstance(nested_types, list[type[type]])
    
    # type 的 type 测试
    assert enhanced_isinstance(type, type[type])
    assert enhanced_isinstance(str, type[Any])

if __name__ == '__main__':
    pytest.main([__file__])
