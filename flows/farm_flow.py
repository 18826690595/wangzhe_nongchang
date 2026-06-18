"""
FarmFlow - 农场自动化业务流程
封装完整的农场自动化流程
"""
import time
from typing import Optional
from loguru import logger

from pages.game_page import GamePage
from pages.farm_page import FarmPage
from pages.friend_page import FriendPage
from core.driver import driver


class FarmFlow:
    """
    农场自动化业务流程
    """
    
    def __init__(self):
        self.game_page = GamePage()
        self.farm_page = FarmPage()
        self.friend_page = FriendPage()
        
        # 统计
        self.stats = {
            "harvest": 0,
            "plant": 0,
            "steal": 0,
            "bless": 0,
            "runs": 0,
        }
    
    # ==================== 完整流程 ====================
    
    def run_full_cycle(self, 
                       do_harvest: bool = True,
                       do_plant: bool = True,
                       do_steal: bool = True,
                       do_bless: bool = True,
                       crop_name: str = "default",
                       max_steal_friends: int = 10,
                       max_bless: int = 20) -> dict:
        """
        执行完整的农场自动化流程
        
        Args:
            do_harvest: 是否收菜
            do_plant: 是否种菜
            do_steal: 是否偷菜
            do_bless: 是否祝福
            crop_name: 种植作物名称
            max_steal_friends: 最大偷菜好友数
            max_bless: 最大祝福数
        
        Returns:
            统计数据
        """
        logger.info("====== 开始农场自动化流程 ======")
        
        try:
            # 1. 连接设备
            if not driver.is_connected:
                logger.error("设备未连接")
                return self.stats
            
            # 2. 处理弹窗
            self.game_page.handle_notifications()
            
            # 3. 进入农场
            if not self.game_page.enter_farm():
                logger.error("进入农场失败")
                return self.stats
            
            # 4. 等待农场加载
            self.farm_page.wait_for_page_load()
            
            # 5. 收菜
            if do_harvest:
                harvest_count = self.farm_page.harvest_all()
                self.stats["harvest"] += harvest_count
            
            # 6. 种菜
            if do_plant:
                plant_count = self.farm_page.plant(crop_name)
                self.stats["plant"] += plant_count
            
            # 7. 偷菜
            if do_steal:
                steal_count = self.farm_page.steal_all_friends(max_steal_friends)
                self.stats["steal"] += steal_count
            
            # 8. 祝福
            if do_bless:
                bless_count = self.friend_page.bless_all_friends(max_bless)
                self.stats["bless"] += bless_count
            
            # 9. 退出农场
            self.farm_page.exit_farm()
            
            # 更新运行次数
            self.stats["runs"] += 1
            
        except Exception as e:
            logger.error(f"流程执行失败: {e}")
        
        logger.info(f"====== 流程完成，统计: {self.stats} ======")
        return self.stats
    
    # ==================== 单独流程 ====================
    
    def harvest_only(self) -> int:
        """
        只执行收菜
        
        Returns:
            收获数量
        """
        logger.info("执行单独收菜流程")
        
        self.game_page.enter_farm()
        self.farm_page.wait_for_page_load()
        count = self.farm_page.harvest_all()
        self.farm_page.exit_farm()
        
        self.stats["harvest"] += count
        return count
    
    def plant_only(self, crop_name: str = "default") -> int:
        """
        只执行种菜
        
        Args:
            crop_name: 作物名称
        
        Returns:
            种植数量
        """
        logger.info("执行单独种菜流程")
        
        self.game_page.enter_farm()
        self.farm_page.wait_for_page_load()
        count = self.farm_page.plant(crop_name)
        self.farm_page.exit_farm()
        
        self.stats["plant"] += count
        return count
    
    def steal_only(self, max_friends: int = 10) -> int:
        """
        只执行偷菜
        
        Args:
            max_friends: 最大好友数
        
        Returns:
            偷菜数量
        """
        logger.info("执行单独偷菜流程")
        
        self.game_page.enter_farm()
        self.farm_page.wait_for_page_load()
        count = self.farm_page.steal_all_friends(max_friends)
        self.farm_page.exit_farm()
        
        self.stats["steal"] += count
        return count
    
    def bless_only(self, max_count: int = 20) -> int:
        """
        只执行祝福
        
        Args:
            max_count: 最大祝福数
        
        Returns:
            祝福数量
        """
        logger.info("执行单独祝福流程")
        
        # 祝福可能不需要进入农场
        count = self.friend_page.bless_all_friends(max_count)
        self.stats["bless"] += count
        return count
    
    # ==================== 定时执行 ====================
    
    def run_daemon(self, interval: int = 300, max_runs: int = 100) -> None:
        """
        守护进程模式执行
        
        Args:
            interval: 执行间隔（秒）
            max_runs: 最大执行次数
        """
        logger.info(f"启动守护进程模式，间隔 {interval} 秒")
        
        run_count = 0
        while run_count < max_runs:
            try:
                self.run_full_cycle()
                run_count += 1
                
                logger.info(f"第 {run_count} 次执行完成，等待 {interval} 秒")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("用户中断，退出守护进程")
                break
            except Exception as e:
                logger.error(f"执行出错: {e}")
                time.sleep(60)  # 出错后等待1分钟
    
    # ==================== 统计 ====================
    
    def get_stats(self) -> dict:
        """
        获取统计数据
        
        Returns:
            统计字典
        """
        return self.stats
    
    def reset_stats(self) -> None:
        """
        重置统计
        """
        for key in self.stats:
            self.stats[key] = 0