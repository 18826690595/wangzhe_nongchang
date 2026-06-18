"""
GamePage - 游戏主页面对象
封装游戏首页的所有操作
"""
from typing import Optional
from loguru import logger

from .base_page import BasePage


class GamePage(BasePage):
    """
    游戏主页面对象
    """
    
    # 页面标识定位器
    PAGE_IDENTIFIER = "game_main_page"
    
    def __init__(self):
        super().__init__()
    
    # ==================== 页面验证 ====================
    
    def is_on_page(self) -> bool:
        """判断是否在游戏主页"""
        return self.is_element_present(self.PAGE_IDENTIFIER, timeout=3.0)
    
    def wait_for_page_load(self, timeout: float = 15.0) -> bool:
        """等待页面加载完成"""
        return self.wait_for_element(self.PAGE_IDENTIFIER, timeout) is not None
    
    # ==================== 进入农场 ====================
    
    def enter_farm(self) -> bool:
        """
        进入农场
        
        Returns:
            是否成功
        """
        logger.info("进入农场...")
        
        # 点击农场入口
        if not self.click_element("farm_icon", timeout=10.0):
            logger.error("未找到农场入口")
            return False
        
        self.wait(2.0)
        
        # 验证是否进入农场
        if not self.is_element_present("farm_page", timeout=5.0):
            logger.warning("可能未成功进入农场")
        
        return True
    
    # ==================== 其他入口 ====================
    
    def enter_shop(self) -> bool:
        """进入商店"""
        return self.click_element("shop_icon", timeout=5.0)
    
    def enter_friends(self) -> bool:
        """进入好友列表"""
        return self.click_element("friends_icon", timeout=5.0)
    
    # ==================== 通知处理 ====================
    
    def handle_notifications(self) -> int:
        """
        处理通知弹窗
        
        Returns:
            处理的通知数量
        """
        count = 0
        
        # 关闭各种弹窗
        popup_locators = ["notification_close", "activity_close", "reward_close"]
        
        for locator in popup_locators:
            if self.click_element(locator, timeout=2.0):
                count += 1
                self.wait(0.5)
        
        if count > 0:
            logger.info(f"关闭 {count} 个弹窗")
        
        return count
    
    # ==================== 返回 ====================
    
    def go_back(self) -> None:
        """返回上一页"""
        self.driver.back()
        self.wait(1.0)