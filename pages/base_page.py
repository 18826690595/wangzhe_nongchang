"""
BasePage - 基础页面类
所有页面对象的父类，封装通用操作
"""
import time
from typing import Optional, Tuple, List
from loguru import logger

from core.driver import driver
from core.vision import vision_engine


class BasePage:
    """
    基础页面类
    封装所有页面通用的操作方法
    """
    
    def __init__(self):
        self.driver = driver
        self.vision = vision_engine
    
    # ==================== 元素查找 ====================
    
    def find_element(self, locator: str, timeout: float = 10.0) -> Optional[Tuple[int, int, int, int]]:
        """
        查找元素（模板图片）
        
        Args:
            locator: 定位器名称（在 locators.py 中定义）
            timeout: 超时时间
        
        Returns:
            元素坐标 (x1, y1, x2, y2) 或 None
        """
        from config.locators import Locators
        
        loc_info = Locators.get(locator)
        if not loc_info:
            logger.error(f"定位器不存在: {locator}")
            return None
        
        template = loc_info.get("template")
        region = loc_info.get("region")
        
        screenshot = self.driver.screenshot()
        result = self.vision.find_template(
            screenshot,
            template,
            region=region,
            threshold=loc_info.get("threshold", 0.8)
        )
        
        if result:
            logger.debug(f"找到元素: {locator}")
            return result
        
        logger.warning(f"未找到元素: {locator}")
        return None
    
    def find_elements(self, locator: str) -> List[Tuple[int, int, int, int]]:
        """
        查找所有匹配的元素
        
        Args:
            locator: 定位器名称
        
        Returns:
            元素坐标列表
        """
        from config.locators import Locators
        
        loc_info = Locators.get(locator)
        if not loc_info:
            return []
        
        screenshot = self.driver.screenshot()
        results = self.vision.find_all_templates(
            screenshot,
            loc_info.get("template"),
            region=loc_info.get("region"),
            threshold=loc_info.get("threshold", 0.8)
        )
        
        return results
    
    def is_element_present(self, locator: str, timeout: float = 5.0) -> bool:
        """
        判断元素是否存在
        
        Args:
            locator: 定位器名称
            timeout: 超时时间
        
        Returns:
            是否存在
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.find_element(locator, timeout=1.0):
                return True
            time.sleep(0.5)
        return False
    
    def wait_for_element(self, locator: str, timeout: float = 10.0) -> Optional[Tuple[int, int, int, int]]:
        """
        等待元素出现
        
        Args:
            locator: 定位器名称
            timeout: 超时时间
        
        Returns:
            元素坐标或None
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.find_element(locator, timeout=1.0)
            if result:
                return result
            time.sleep(0.5)
        
        logger.warning(f"等待元素超时: {locator}")
        return None
    
    # ==================== 点击操作 ====================
    
    def click_element(self, locator: str, timeout: float = 10.0) -> bool:
        """
        点击元素
        
        Args:
            locator: 定位器名称
            timeout: 超时时间
        
        Returns:
            是否成功
        """
        result = self.wait_for_element(locator, timeout)
        if not result:
            return False
        
        center = self.vision.get_center(result)
        self.driver.tap(center[0], center[1])
        logger.info(f"点击元素: {locator} at ({center[0]}, {center[1])}")
        return True
    
    def click_position(self, x: int, y: int) -> None:
        """
        点击坐标
        
        Args:
            x: x坐标
            y: y坐标
        """
        self.driver.tap(x, y)
        logger.debug(f"点击坐标: ({x}, {y})")
    
    def click_by_ratio(self, ratio_x: float, ratio_y: float) -> None:
        """
        按屏幕比例点击
        
        Args:
            ratio_x: x比例 (0-1)
            ratio_y: y比例 (0-1)
        """
        x, y = self.driver.ratio_to_pixel(ratio_x, ratio_y)
        self.click_position(x, y)
    
    def click_elements(self, locator: str, max_count: int = 10) -> int:
        """
        点击所有匹配的元素
        
        Args:
            locator: 定位器名称
            max_count: 最大点击数量
        
        Returns:
            实际点击数量
        """
        elements = self.find_elements(locator)
        count = 0
        
        for elem in elements[:max_count]:
            center = self.vision.get_center(elem)
            self.driver.tap(center[0], center[1])
            count += 1
            time.sleep(0.3)
        
        logger.info(f"点击 {count} 个元素: {locator}")
        return count
    
    # ==================== 滑动操作 ====================
    
    def swipe(self, direction: str, distance: float = 0.5) -> None:
        """
        滑动屏幕
        
        Args:
            direction: 方向 (up/down/left/right)
            distance: 滑动距离比例
        """
        self.driver.swipe(direction, distance)
        logger.debug(f"滑动: {direction}")
    
    def swipe_to_element(self, locator: str, direction: str = "down", max_swipes: int = 5) -> bool:
        """
        滑动直到找到元素
        
        Args:
            locator: 定位器名称
            direction: 滑动方向
            max_swipes: 最大滑动次数
        
        Returns:
            是否找到
        """
        for _ in range(max_swipes):
            if self.find_element(locator, timeout=2.0):
                return True
            self.swipe(direction)
            time.sleep(0.5)
        
        return False
    
    # ==================== 等待操作 ====================
    
    def wait(self, seconds: float) -> None:
        """
        等待
        
        Args:
            seconds: 等待秒数
        """
        time.sleep(seconds)
        logger.debug(f"等待 {seconds} 秒")
    
    def wait_for_page_load(self, timeout: float = 10.0) -> bool:
        """
        等待页面加载完成（子类实现）
        
        Args:
            timeout: 超时时间
        
        Returns:
            是否加载完成
        """
        raise NotImplementedError("子类需实现此方法")
    
    # ==================== 页面验证 ====================
    
    def is_on_page(self) -> bool:
        """
        判断是否在当前页面（子类实现）
        
        Returns:
            是否在当前页面
        """
        raise NotImplementedError("子类需实现此方法")
    
    # ==================== 截图 ====================
    
    def save_screenshot(self, name: str) -> str:
        """
        保存截图
        
        Args:
            name: 截图名称
        
        Returns:
            截图路径
        """
        screenshot = self.driver.screenshot()
        path = f"config/templates/buttons/{name}.png"
        import cv2
        cv2.imwrite(path, screenshot)
        logger.info(f"截图保存: {path}")
        return path
    
    def save_region_screenshot(self, name: str, region: Tuple[int, int, int, int]) -> str:
        """
        保存区域截图
        
        Args:
            name: 截图名称
            region: 区域 (x1, y1, x2, y2)
        
        Returns:
            截图路径
        """
        screenshot = self.driver.screenshot()
        cropped = screenshot[region[1]:region[3], region[0]:region[2]]
        
        path = f"config/templates/buttons/{name}.png"
        import cv2
        cv2.imwrite(path, cropped)
        logger.info(f"区域截图保存: {path}")
        return path