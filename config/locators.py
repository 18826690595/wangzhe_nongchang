"""
Locators - 元素定位配置
所有页面元素的定位信息集中管理
"""

class Locators:
    """
    元素定位器配置类
    所有元素的定位信息在这里统一定义
    """
    
    # ==================== 定位器字典 ====================
    
    LOCATORS = {
        # ===== 游戏主页元素 =====
        "game_main_page": {
            "template": "game_main_page.png",
            "description": "游戏主页标识",
            "threshold": 0.8,
        },
        "farm_icon": {
            "template": "farm_icon.png",
            "description": "农场入口图标",
            "threshold": 0.8,
            "region": None,  # 全屏查找，或指定区域如 (0, 100, 200, 300)
        },
        "shop_icon": {
            "template": "shop_icon.png",
            "description": "商店入口",
            "threshold": 0.8,
        },
        "friends_icon": {
            "template": "friends_icon.png",
            "description": "好友入口",
            "threshold": 0.8,
        },
        
        # ===== 弹窗元素 =====
        "notification_close": {
            "template": "notification_close.png",
            "description": "通知关闭按钮",
            "threshold": 0.8,
        },
        "activity_close": {
            "template": "activity_close.png",
            "description": "活动弹窗关闭",
            "threshold": 0.8,
        },
        "reward_close": {
            "template": "reward_close.png",
            "description": "奖励弹窗关闭",
            "threshold": 0.8,
        },
        
        # ===== 农场页面元素 =====
        "farm_page": {
            "template": "farm_page.png",
            "description": "农场页面标识",
            "threshold": 0.8,
        },
        "harvest_btn": {
            "template": "harvest_btn.png",
            "description": "收获按钮",
            "threshold": 0.8,
            "region": None,
        },
        "harvest_confirm": {
            "template": "harvest_confirm.png",
            "description": "收获确认",
            "threshold": 0.8,
        },
        "empty_plot": {
            "template": "empty_plot.png",
            "description": "空地块",
            "threshold": 0.7,
        },
        "plant_confirm": {
            "template": "plant_confirm.png",
            "description": "种植确认",
            "threshold": 0.8,
        },
        
        # ===== 作物选择 =====
        "crop_default": {
            "template": "crop_default.png",
            "description": "默认作物",
            "threshold": 0.8,
        },
        "crop_wheat": {
            "template": "crop_wheat.png",
            "description": "小麦",
            "threshold": 0.8,
        },
        "crop_carrot": {
            "template": "crop_carrot.png",
            "description": "胡萝卜",
            "threshold": 0.8,
        },
        
        # ===== 好友相关 =====
        "friend_list_btn": {
            "template": "friend_list_btn.png",
            "description": "好友列表入口",
            "threshold": 0.8,
        },
        "friend_page": {
            "template": "friend_page.png",
            "description": "好友页面标识",
            "threshold": 0.8,
        },
        "friend_item": {
            "template": "friend_item.png",
            "description": "好友项",
            "threshold": 0.7,
        },
        "steal_btn": {
            "template": "steal_btn.png",
            "description": "偷菜按钮",
            "threshold": 0.8,
        },
        "bless_btn": {
            "template": "bless_btn.png",
            "description": "祝福按钮",
            "threshold": 0.8,
        },
        
        # ===== 其他功能 =====
        "water_tool": {
            "template": "water_tool.png",
            "description": "浇水工具",
            "threshold": 0.8,
        },
        "need_water_mark": {
            "template": "need_water_mark.png",
            "description": "需要浇水标记",
            "threshold": 0.7,
        },
    }
    
    # ==================== 查询方法 ====================
    
    @classmethod
    def get(cls, name: str) -> dict:
        """
        获取定位器配置
        
        Args:
            name: 定位器名称
        
        Returns:
            定位器配置字典
        """
        return cls.LOCATORS.get(name)
    
    @classmethod
    def add(cls, name: str, config: dict) -> None:
        """
        添加新定位器
        
        Args:
            name: 定位器名称
            config: 配置信息
        """
        cls.LOCATORS[name] = config
    
    @classmethod
    def update(cls, name: str, config: dict) -> None:
        """
        更新定位器配置
        
        Args:
            name: 定位器名称
            config: 新配置
        """
        if name in cls.LOCATORS:
            cls.LOCATORS[name].update(config)
        else:
            cls.LOCATORS[name] = config
    
    @classmethod
    def list_all(cls) -> list:
        """
        列出所有定位器
        
        Returns:
            定位器名称列表
        """
        return list(cls.LOCATORS.keys())
    
    @classmethod
    def print_all(cls) -> None:
        """
        打印所有定位器信息
        """
        for name, config in cls.LOCATORS.items():
            print(f"{name}: {config.get('description', 'N/A')}")


# ==================== 快速添加定位器 ====================

def add_locator(name: str, template: str, description: str = "", 
                threshold: float = 0.8, region: tuple = None):
    """
    快速添加定位器
    
    Args:
        name: 定位器名称
        template: 模板图片文件名
        description: 描述
        threshold: 匹配阈值
        region: 查找区域
    """
    Locators.add(name, {
        "template": template,
        "description": description,
        "threshold": threshold,
        "region": region,
    })