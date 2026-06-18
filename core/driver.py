"""
Driver - 设备驱动类
封装ADB操作，作为PO模式的基础驱动层
"""
import time
from typing import Tuple, Optional
from loguru import logger

try:
    import uiautomator2 as u2
except ImportError:
    logger.warning("uiautomator2 未安装")
    u2 = None


class Driver:
    """
    设备驱动类
    封装所有ADB操作
    """
    
    def __init__(self):
        self._device: Optional[u2.Device] = None
        self._screen_size: Optional[Tuple[int, int]] = None
        self._is_connected: bool = False
    
    # ==================== 连接 ====================
    
    def connect(self, adb_port: int = 7555) -> bool:
        """
        连接设备
        
        Args:
            adb_port: ADB端口
        
        Returns:
            是否成功
        """
        if u2 is None:
            logger.error("uiautomator2 未安装，无法连接设备")
            return False
        
        try:
            logger.info(f"连接设备: 127.0.0.1:{adb_port}")
            self._device = u2.connect(f"127.0.0.1:{adb_port}")
            
            # 获取屏幕尺寸
            info = self._device.device_info
            self._screen_size = (info.get("displayWidth", 1280), info.get("displayHeight", 720))
            
            self._is_connected = True
            logger.info(f"连接成功，屏幕尺寸: {self._screen_size}")
            return True
            
        except Exception as e:
            logger.error(f"连接失败: {e}")
            self._is_connected = False
            return False
    
    def disconnect(self) -> None:
        """断开连接"""
        self._device = None
        self._is_connected = False
        logger.info("已断开连接")
    
    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._is_connected
    
    @property
    def screen_size(self) -> Tuple[int, int]:
        """屏幕尺寸"""
        return self._screen_size or (1280, 720)
    
    @property
    def device(self) -> Optional[u2.Device]:
        """获取设备对象"""
        return self._device
    
    # ==================== 截图 ====================
    
    def screenshot(self) -> any:
        """
        截取屏幕
        
        Returns:
            OpenCV图像格式
        """
        if not self._is_connected:
            logger.error("设备未连接")
            return None
        
        try:
            return self._device.screenshot(format="opencv")
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    # ==================== 点击 ====================
    
    def tap(self, x: int, y: int) -> bool:
        """
        点击坐标
        
        Args:
            x: x坐标
            y: y坐标
        
        Returns:
            是否成功
        """
        if not self._is_connected:
            logger.error("设备未连接")
            return False
        
        try:
            self._device.click(x, y)
            logger.debug(f"点击: ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"点击失败: {e}")
            return False
    
    def tap_by_ratio(self, ratio_x: float, ratio_y: float) -> bool:
        """
        按比例点击
        
        Args:
            ratio_x: x比例 (0-1)
            ratio_y: y比例 (0-1)
        
        Returns:
            是否成功
        """
        x, y = self.ratio_to_pixel(ratio_x, ratio_y)
        return self.tap(x, y)
    
    def ratio_to_pixel(self, ratio_x: float, ratio_y: float) -> Tuple[int, int]:
        """
        比例转像素
        
        Args:
            ratio_x: x比例
            ratio_y: y比例
        
        Returns:
            像素坐标
        """
        width, height = self.screen_size
        x = int(width * ratio_x)
        y = int(height * ratio_y)
        return (x, y)
    
    # ==================== 长按 ====================
    
    def long_press(self, x: int, y: int, duration: float = 2.0) -> bool:
        """
        长按
        
        Args:
            x: x坐标
            y: y坐标
            duration: 持续时间
        
        Returns:
            是否成功
        """
        if not self._is_connected:
            return False
        
        try:
            self._device.swipe(x, y, x, y, duration)
            logger.debug(f"长按: ({x}, {y}), {duration}秒")
            return True
        except Exception as e:
            logger.error(f"长按失败: {e}")
            return False
    
    # ==================== 滑动 ====================
    
    def swipe(self, direction: str, distance: float = 0.5) -> bool:
        """
        滑动屏幕
        
        Args:
            direction: 方向 (up/down/left/right)
            distance: 滑动距离比例
        
        Returns:
            是否成功
        """
        if not self._is_connected:
            return False
        
        width, height = self.screen_size
        center_x = width // 2
        center_y = height // 2
        
        try:
            if direction == "up":
                self._device.swipe(center_x, center_y + int(height * distance * 0.5), 
                                   center_x, center_y - int(height * distance * 0.5), 0.5)
            elif direction == "down":
                self._device.swipe(center_x, center_y - int(height * distance * 0.5), 
                                   center_x, center_y + int(height * distance * 0.5), 0.5)
            elif direction == "left":
                self._device.swipe(center_x + int(width * distance * 0.5), center_y, 
                                   center_x - int(width * distance * 0.5), center_y, 0.5)
            elif direction == "right":
                self._device.swipe(center_x - int(width * distance * 0.5), center_y, 
                                   center_x + int(width * distance * 0.5), center_y, 0.5)
            
            logger.debug(f"滑动: {direction}")
            return True
            
        except Exception as e:
            logger.error(f"滑动失败: {e}")
            return False
    
    # ==================== 按键 ====================
    
    def back(self) -> bool:
        """返回键"""
        if not self._is_connected:
            return False
        
        try:
            self._device.press("back")
            logger.debug("按返回键")
            return True
        except Exception as e:
            logger.error(f"按键失败: {e}")
            return False
    
    def home(self) -> bool:
        """Home键"""
        if not self._is_connected:
            return False
        
        try:
            self._device.press("home")
            logger.debug("按Home键")
            return True
        except Exception as e:
            logger.error(f"按键失败: {e}")
            return False


# 全局驱动实例
driver = Driver()