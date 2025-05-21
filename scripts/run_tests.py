#!/usr/bin/env python3
"""
运行单元测试的简单脚本
"""
import pytest
import sys

if __name__ == "__main__":
    # 运行所有测试
    if len(sys.argv) == 1:
        sys.exit(pytest.main(["-v", "tests"]))
    # 运行指定的测试
    else:
        sys.exit(pytest.main(["-v"] + sys.argv[1:]))
