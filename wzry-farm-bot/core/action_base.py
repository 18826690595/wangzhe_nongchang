"""
基礎操作 - 只封装底层操作，不含业务逻辑
"""
import time
import random
from loguru import logger
from typing import Optional, List, Tuple
from core.device import device_manager
from core.vision import VisionEngine
from config.template_config import template_config


class ActionBase:
    """
    基础操作类 - 只做底层封装
    
    不包含具体业务逻辑，只提供：
    - 点击模板
    - 点击坐标
    - 滑动
    - 等待
    等
    """
    
    def __init__(self, vision: VisionEngine, random_delay: bool = True):
        self.vision = vision
        self.random_delay = random_delay
        self.device = device_manager
        self._found_positions: List[Tuple[int, int]] = []
    
    def _delay(self, base: float = 0.5, variance: float = 0.3):
        """随机延迟"""
        if self.random_delay:
            delay = base + random.uniform(-variance, variance)
            delay = max(0.1, delay)
        else:
            delay = base
        time.sleep(delay)
    
    # ========== 点击操作 ==========
    
    def click_template(self, template_name: str, threshold: Optional[float] = None) -> bool:
        """点击模板图片"""
        info = template_config.get_info(template_name)
        img = template_config.get(template_name)
        
        if img is None:
            logger.warning(f"模板不存在: {template_name}")
            return False
        
        threshold = threshold or (info.threshold if info else 0.8)
        screenshot = self.device.screenshot()
        rect = self.vision.find_template(screenshot, template_name, threshold)
        
        if rect:
            center = self.vision.get_center(rect)
            self.device.tap(*center)
            self._delay(0.5)
            return True
        return False
    
    def click_position(self, x: int, y: int):
        """点击坐标"""
        self.device.tap(x, y)
        self._delay(0.3)
    
    def long_press(self, x: int, y: int, duration: float = 1.0):
        """长按"""
        self.device.long_press(x, y, duration)
        self._delay(0.3)
    
    # ========== 滑动操作 ==========
    
    def swipe(self, direction: str, distance: int = 300):
        """滑动"""
        width, height = self.device.screen_size
        center_x = width // 2
        center_y = height // 2
        
        if direction == "up":
            self.device.swipe((center_x, center_y), (center_x, center_y - distance))
        elif direction == "down":
            self.device.swipe((center_x, center_y), (center_x, center_y + distance))
        elif direction == "left":
            self.device.swipe((center_x, center_y), (center_x - distance, center_y))
        elif direction == "right":
            self.device.swipe((center_x, center_y), (center_x + distance, center_y))
        self._delay(0.3)
    
    # ========== 查找操作 ==========
    
    def find_all(self, template_name: str) -> List[Tuple[int, int]]:
        """查找所有匹配位置"""
        info = template_config.get_info(template_name)
        img = template_config.get(template_name)
        
        if img is None:
            return []
        
        screenshot = self.device.screenshot()
        threshold = info.threshold if info else 0.8
        rects = self.vision.find_all_templates(screenshot, template_name, threshold)
        positions = [self.vision.get_center(r) for r in rects]
        self._found_positions = positions
        
        logger.debug(f"找到 {len(positions)} 个 '{template_name}'")
        return positions
    
    def click_found(self, index: int = 0) -> bool:
        """点击已找到的位置"""
        if index >= len(self._found_positions):
            return False
        x, y = self._found_positions[index]
        self.device.tap(x, y)
        self._delay(0.5)
        return True
    
    # ========== 其他操作 ==========
    
    def wait(self, seconds: float):
        """等待"""
        time.sleep(seconds)
    
    def back(self):
        """返回键"""
        self.device.back()
        self._delay(0.3)
    
    def screenshot(self):
        """截图"""
        return self.device.screenshot()
