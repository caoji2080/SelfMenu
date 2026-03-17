"""
事件总线 - 用于模块间通信的事件系统
"""
from typing import Callable, Dict, List
from collections import defaultdict


class Event:
    """事件基类"""
    def __init__(self, event_type: str, data=None):
        self.type = event_type
        self.data = data


class EventBus:
    """事件总线单例"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """初始化事件总线"""
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件"""
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        """取消订阅"""
        if callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def publish(self, event: Event):
        """发布事件"""
        for callback in self._listeners[event.type]:
            try:
                callback(event)
            except Exception as e:
                print(f"事件处理错误：{e}")

    def clear(self):
        """清空所有订阅者"""
        self._listeners.clear()


# 预定义的事件类型
class RecipeEvents:
    """菜谱相关事件"""
    RECIPE_CREATED = "recipe.created"
    RECIPE_UPDATED = "recipe.updated"
    RECIPE_DELETED = "recipe.deleted"
    RECIPE_VIEWED = "recipe.viewed"
    RECIPES_LOADED = "recipes.loaded"


class CategoryEvents:
    """类别相关事件"""
    CATEGORY_CREATED = "category.created"
    CATEGORY_UPDATED = "category.updated"
    CATEGORY_DELETED = "category.deleted"
    CATEGORIES_LOADED = "categories.loaded"


class AppEvents:
    """应用相关事件"""
    APP_STARTED = "app.started"
    APP_CLOSING = "app.closing"
    DATA_REFRESHED = "data.refreshed"
    PAGE_CHANGED = "page.changed"
