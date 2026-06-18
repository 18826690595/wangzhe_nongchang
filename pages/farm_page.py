"""
FarmPage - 农场页面对象
封装农场的所有操作：收菜、种菜、偷菜等
"""
from typing import List, Tuple, Optional
from loguru import logger

from .base_page import BasePage


class FarmPage(BasePage):
    """
    农场页面对象
    """
    
    # 页面标识定位器
    PAGE_IDENTIFIER = "farm_page"
    
    def __init__(self):
        super().__init__()
        self.harvest_count = 0
        self.plant_count = 0
    
    # ==================== 页面验证 ====================
    
    def is_on_page(self) -> bool:
        """判断是否在农场页面"""
        return self.is_element_present(self.PAGE_IDENTIFIER, timeout=3.0)
    
    def wait_for_page_load(self, timeout: float = 10.0) -> bool:
        """等待页面加载完成"""
        return self.wait_for_element(self.PAGE_IDENTIFIER, timeout) is not None
    
    # ==================== 收菜 ====================
    
    def harvest_all(self) -> int:
        """
        收获所有成熟作物
        
        Returns:
            收获数量
        """
        logger.info("开始收菜...")
        count = 0
        
        # 循环点击收获按钮
        for _ in range(20):  # 最多点击20次
            if self.click_element("harvest_btn", timeout=2.0):
                count += 1
                self.wait(0.3)
            else:
                break
        
        self.harvest_count += count
        logger.info(f"收获 {count} 个作物，累计 {self.harvest_count}")
        return count
    
    def harvest_at_position(self, x: int, y: int) -> bool:
        """
        收获指定位置的作物
        
        Args:
            x: x坐标
            y: y坐标
        
        Returns:
            是否成功
        """
        # 点击作物位置
        self.click_position(x, y)
        self.wait(0.5)
        
        # 点击收获按钮
        return self.click_element("harvest_confirm", timeout=2.0)
    
    # ==================== 种菜 ====================
    
    def plant(self, crop_name: str = "default") -> int:
        """
        种植作物
        
        Args:
            crop_name: 作物名称
        
        Returns:
            种植数量
        """
        logger.info(f"开始种菜: {crop_name}")
        count = 0
        
        # 查找空地块
        empty_plots = self.find_elements("empty_plot")
        
        for plot in empty_plots:
            center = self.vision.get_center(plot)
            
            # 点击空地块
            self.click_position(center[0], center[1])
            self.wait(0.5)
            
            # 选择作物
            if self.click_element(f"crop_{crop_name}", timeout=2.0):
                # 确认种植
                self.click_element("plant_confirm", timeout=2.0)
                count += 1
                self.wait(0.5)
        
        self.plant_count += count
        logger.info(f"种植 {count} 个作物，累计 {self.plant_count}")
        return count
    
    def plant_at_position(self, x: int, y: int, crop_name: str = "default") -> bool:
        """
        在指定位置种植
        
        Args:
            x: x坐标
            y: y坐标
            crop_name: 作物名称
        
        Returns:
            是否成功
        """
        # 点击空地块
        self.click_position(x, y)
        self.wait(0.5)
        
        # 选择作物
        if not self.click_element(f"crop_{crop_name}", timeout=2.0):
            return False
        
        # 确认种植
        return self.click_element("plant_confirm", timeout=2.0)
    
    # ==================== 偷菜 ====================
    
    def steal_from_friend(self, friend_name: str) -> int:
        """
        从好友农场偷菜
        
        Args:
            friend_name: 好友名称
        
        Returns:
            偷菜数量
        """
        logger.info(f"去好友 {friend_name} 农场偷菜...")
        
        # 进入好友农场
        if not self.enter_friend_farm(friend_name):
            return 0
        
        count = 0
        
        # 偷菜
        for _ in range(10):
            if self.click_element("steal_btn", timeout=2.0):
                count += 1
                self.wait(0.3)
            else:
                break
        
        # 返回自己的农场
        self.go_back()
        
        logger.info(f"从 {friend_name} 偷了 {count} 个作物")
        return count
    
    def enter_friend_farm(self, friend_name: str) -> bool:
        """
        进入好友农场
        
        Args:
            friend_name: 好友名称
        
        Returns:
            是否成功
        """
        # 点击好友列表入口
        if not self.click_element("friend_list_btn", timeout=5.0):
            return False
        
        self.wait(1.0)
        
        # 查找好友并点击
        # TODO: 需要OCR识别好友名称
        if not self.click_element(f"friend_{friend_name}", timeout=5.0):
            logger.warning(f"未找到好友: {friend_name}")
            self.go_back()
            return False
        
        self.wait(2.0)
        return True
    
    def steal_all_friends(self, max_friends: int = 10) -> int:
        """
        遍历好友偷菜
        
        Args:
            max_friends: 最大好友数量
        
        Returns:
            总偷菜数量
        """
        logger.info("开始遍历好友偷菜...")
        total = 0
        
        # 进入好友列表
        if not self.click_element("friend_list_btn", timeout=5.0):
            return 0
        
        self.wait(1.0)
        
        # 遍历好友
        for i in range(max_friends):
            # 点击好友
            if self.click_element("friend_item", timeout=3.0):
                self.wait(2.0)
                
                # 偷菜
                stolen = 0
                for _ in range(5):
                    if self.click_element("steal_btn", timeout=2.0):
                        stolen += 1
                        self.wait(0.3)
                    else:
                        break
                
                total += stolen
                logger.info(f"偷菜 {stolen} 个")
                
                # 返回好友列表
                self.go_back()
                self.wait(1.0)
            else:
                break
        
        # 返回农场
        self.go_back()
        
        logger.info(f"偷菜完成，总计 {total} 个")
        return total
    
    # ==================== 浇水 ====================
    
    def water_all(self) -> int:
        """
        给所有作物浇水
        
        Returns:
            浇水数量
        """
        logger.info("开始浇水...")
        count = 0
        
        # 点击浇水工具
        if not self.click_element("water_tool", timeout=5.0):
            return 0
        
        self.wait(0.5)
        
        # 点击所有需要浇水的作物
        for _ in range(20):
            if self.click_element("need_water_mark", timeout=2.0):
                count += 1
                self.wait(0.3)
            else:
                break
        
        logger.info(f"浇水 {count} 次")
        return count
    
    # ==================== 统计 ====================
    
    def get_stats(self) -> dict:
        """
        获取农场统计
        
        Returns:
            统计数据
        """
        return {
            "harvest": self.harvest_count,
            "plant": self.plant_count,
        }
    
    # ==================== 退出农场 ====================
    
    def exit_farm(self) -> bool:
        """
        退出农场
        
        Returns:
            是否成功
        """
        self.driver.back()
        self.wait(1.0)
        return True