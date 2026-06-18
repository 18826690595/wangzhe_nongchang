"""
FriendPage - 好友页面对象
封装好友相关操作：祝福、访问好友农场等
"""
from typing import List, Optional
from loguru import logger

from .base_page import BasePage


class FriendPage(BasePage):
    """
    好友页面对象
    """
    
    # 页面标识定位器
    PAGE_IDENTIFIER = "friend_page"
    
    def __init__(self):
        super().__init__()
        self.bless_count = 0
    
    # ==================== 页面验证 ====================
    
    def is_on_page(self) -> bool:
        """判断是否在好友页面"""
        return self.is_element_present(self.PAGE_IDENTIFIER, timeout=3.0)
    
    def wait_for_page_load(self, timeout: float = 10.0) -> bool:
        """等待页面加载完成"""
        return self.wait_for_element(self.PAGE_IDENTIFIER, timeout) is not None
    
    # ==================== 祝福 ====================
    
    def bless_all_friends(self, max_count: int = 20) -> int:
        """
        祝福所有好友
        
        Args:
            max_count: 最大祝福数量
        
        Returns:
            祝福数量
        """
        logger.info("开始祝福好友...")
        count = 0
        
        # 进入好友列表
        if not self.click_element("friend_list_btn", timeout=5.0):
            return 0
        
        self.wait(1.0)
        
        # 遍历祝福
        for _ in range(max_count):
            if self.click_element("bless_btn", timeout=3.0):
                count += 1
                self.wait(0.5)
                
                # 滑动查找更多好友
                self.swipe("down", 0.3)
                self.wait(0.5)
            else:
                break
        
        # 关闭好友列表
        self.go_back()
        
        self.bless_count += count
        logger.info(f"祝福 {count} 个好友，累计 {self.bless_count}")
        return count
    
    def bless_friend(self, friend_name: str) -> bool:
        """
        祝福指定好友
        
        Args:
            friend_name: 好友名称
        
        Returns:
            是否成功
        """
        logger.info(f"祝福好友: {friend_name}")
        
        # TODO: 需要OCR识别好友名称
        
        return self.click_element("bless_btn", timeout=3.0)
    
    # ==================== 好友列表 ====================
    
    def get_friend_list(self) -> List[str]:
        """
        获取好友列表
        
        Returns:
            好友名称列表
        """
        # TODO: 需要OCR识别
        
        friends = []
        
        # 进入好友列表
        if not self.click_element("friend_list_btn", timeout=5.0):
            return friends
        
        self.wait(1.0)
        
        # OCR识别好友名称
        screenshot = self.driver.screenshot()
        # self.vision.recognize_text(screenshot, region=...)
        
        self.go_back()
        return friends
    
    # ==================== 统计 ====================
    
    def get_stats(self) -> dict:
        """
        获取祝福统计
        
        Returns:
            统计数据
        """
        return {
            "bless": self.bless_count,
        }