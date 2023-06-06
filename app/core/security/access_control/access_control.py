# -*- coding: utf-8 -*-
from functools import cache
from os import path

from casbin import Enforcer


@cache
def get_todos_enforcer() -> Enforcer:
    dir_ = path.dirname(__file__)
    return Enforcer(
        path.join(dir_, "model.conf"),
        path.join(dir_, "policies.csv"),
    )
