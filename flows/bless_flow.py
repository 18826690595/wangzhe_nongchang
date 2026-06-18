"""
BlessFlow - 祝福业务流程
封装祝福相关的完整流程
"""
from loguru import logger

from pages.friend_page import FriendPage


class BlessFlow:
    """
    祝福业务流程
    """
    
    def __init__(self):
        self.friend_page = FriendPage()
        self.stats = {
            "bless": 0,
            "runs": 0,
        }
    
    def run(self, max_count: int = 20) -> int:
        """
        执行祝福流程
        
        Args:
            max_count: 最大祝福数量
        
        Returns:
            祝福数量
        """
        logger.info("执行祝福流程")
        
        count = self.friend_page.bless_all_friends(max_count)
        self.stats["bless"] += count
        self.stats["runs"] += 1
        
        return count
    
    def get_stats(self) -> dict:
        """获取统计"""
        return self.stats