"""
Run - PO模式入口文件
简洁的命令行接口，调用业务流程执行自动化
"""
import argparse
import sys
from loguru import logger

from core.driver import driver
from flows.farm_flow import FarmFlow
from flows.bless_flow import BlessFlow
from config.locators import Locators


def setup_logger():
    """配置日志"""
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="{time:HH:mm:ss} | {level} | {message}")
    logger.add("logs/run.log", level="DEBUG", rotation="10 MB")


def main():
    """主函数"""
    setup_logger()
    
    parser = argparse.ArgumentParser(
        description="王者荣耀农场自动化 - PO模式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run.py --connect 7555           # 连接设备
  python run.py --once                   # 执行一次完整流程
  python run.py --harvest                # 只收菜
  python run.py --plant                  # 只种菜
  python run.py --steal                  # 只偷菜
  python run.py --bless                  # 只祝福
  python run.py --daemon 300             # 守护进程，间隔300秒
  python run.py --list-locators          # 列出所有定位器
        """
    )
    
    parser.add_argument("--connect", type=int, default=7555, help="连接设备，指定ADB端口")
    parser.add_argument("--once", action="store_true", help="执行一次完整流程")
    parser.add_argument("--harvest", action="store_true", help="只执行收菜")
    parser.add_argument("--plant", action="store_true", help="只执行种菜")
    parser.add_argument("--steal", action="store_true", help="只执行偷菜")
    parser.add_argument("--bless", action="store_true", help="只执行祝福")
    parser.add_argument("--daemon", type=int, help="守护进程模式，指定间隔秒数")
    parser.add_argument("--crop", type=str, default="default", help="种植作物名称")
    parser.add_argument("--max-steal", type=int, default=10, help="最大偷菜好友数")
    parser.add_argument("--max-bless", type=int, default=20, help="最大祝福数")
    parser.add_argument("--list-locators", action="store_true", help="列出所有定位器")
    
    args = parser.parse_args()
    
    # 列出定位器
    if args.list_locators:
        print("\n所有定位器:")
        Locators.print_all()
        return
    
    # 连接设备
    if not driver.connect(args.connect):
        logger.error("连接设备失败")
        sys.exit(1)
    
    # 创建流程对象
    farm_flow = FarmFlow()
    bless_flow = BlessFlow()
    
    # 执行操作
    try:
        if args.once:
            farm_flow.run_full_cycle(
                crop_name=args.crop,
                max_steal_friends=args.max_steal,
                max_bless=args.max_bless
            )
            print(f"\n统计: {farm_flow.get_stats()}")
        
        elif args.harvest:
            count = farm_flow.harvest_only()
            print(f"\n收获: {count}")
        
        elif args.plant:
            count = farm_flow.plant_only(args.crop)
            print(f"\n种植: {count}")
        
        elif args.steal:
            count = farm_flow.steal_only(args.max_steal)
            print(f"\n偷菜: {count}")
        
        elif args.bless:
            count = bless_flow.run(args.max_bless)
            print(f"\n祝福: {count}")
        
        elif args.daemon:
            farm_flow.run_daemon(args.daemon)
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        logger.info("用户中断")
    
    finally:
        driver.disconnect()
        logger.info("程序结束")


if __name__ == "__main__":
    main()