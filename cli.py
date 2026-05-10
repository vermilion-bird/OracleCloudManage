#!/usr/bin/env python3
"""Oracle Cloud Instance CLI 工具"""
import argparse
import json
import logging
import oci
from oracle_sdk.oracle_cloud import (
    list_instances,
    get_instance_by_id,
    start_instance,
    stop_instance,
    get_all_accounts
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def cmd_list(args):
    """列出所有实例"""
    account_index = args.account if args.account is not None else None
    instances = list_instances(account_index)

    if args.format == "json":
        data = [i.to_dict() for i in instances]
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"共 {len(instances)} 个实例:")
        print("-" * 100)
        for i in instances:
            state_icon = "🟢" if i.lifecycle_state == "RUNNING" else "🔴" if i.lifecycle_state == "STOPPED" else "⚪"
            print(f"{state_icon} [{i.account_index}] {i.display_name}")
            print(f"   ID: {i.instance_id}")
            print(f"   IP: {i.ip}")
            print(f"   Region: {i.region}")
            print(f"   State: {i.lifecycle_state}")
            print(f"   Processor: {i.processor_description}")
            print(f"   Created: {i.time_created}")
            print("-" * 100)


def cmd_start(args):
    """启动实例"""
    accounts = get_all_accounts()
    account_index = args.account if args.account is not None else None

    if args.all_stopped:
        logger.info("启动所有停止的实例...")
        instances = list_instances(account_index)
        for i in instances:
            if i.lifecycle_state == "STOPPED":
                config = accounts[i.account_index]
                compute_client = oci.core.ComputeClient(config)
                logger.info(f"启动 {i.display_name} ({i.instance_id})...")
                start_instance(compute_client, i.instance_id)
                logger.info(f"✓ {i.display_name} 已启动")
        logger.info("完成")
    elif args.instance_id:
        instance = get_instance_by_id(args.instance_id, account_index)
        if instance:
            config = accounts[instance.account_index]
            compute_client = oci.core.ComputeClient(config)
            logger.info(f"启动 {instance.display_name} ({args.instance_id})...")
            start_instance(compute_client, args.instance_id)
            logger.info(f"✓ {instance.display_name} 已启动")
        else:
            logger.error(f"未找到实例: {args.instance_id}")
    else:
        logger.error("请指定 instance_id 或 --all-stopped")


def cmd_stop(args):
    """命停实例"""
    if not args.instance_id:
        logger.error("请指定实例 ID")
        return

    account_index = args.account if args.account is not None else None
    instance = get_instance_by_id(args.instance_id, account_index)
    if instance:
        accounts = get_all_accounts()
        config = accounts[instance.account_index]
        compute_client = oci.core.ComputeClient(config)
        logger.info(f"命停 {instance.display_name} ({args.instance_id})...")
        stop_instance(compute_client, args.instance_id)
        logger.info(f"✓ {instance.display_name} 已命停")
    else:
        logger.error(f"未找到实例: {args.instance_id}")


def cmd_info(args):
    """查看实例详情"""
    if not args.instance_id:
        logger.error("请指定实例 ID")
        return

    account_index = args.account if args.account is not None else None
    instance = get_instance_by_id(args.instance_id, account_index)
    if instance:
        print(f"实例: {instance.display_name}")
        print("-" * 50)
        print(f"ID: {args.instance_id}")
        print(f"IP: {instance.ip}")
        print(f"Region: {instance.region}")
        print(f"State: {instance.lifecycle_state}")
        print(f"Processor: {instance.processor_description}")
        print(f"Created: {instance.time_created}")
        print(f"Account Index: {instance.account_index}")
    else:
        logger.error(f"未找到实例: {args.instance_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Oracle Cloud Instance CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有实例")
    list_parser.add_argument("--account", type=int, help="指定账户索引")
    list_parser.add_argument("--format", choices=["table", "json"], default="table", help="输出格式")
    list_parser.set_defaults(func=cmd_list)

    # start 命令
    start_parser = subparsers.add_parser("start", help="启动实例")
    start_parser.add_argument("instance_id", nargs="?", help="实例 ID")
    start_parser.add_argument("--all-stopped", action="store_true", help="启动所有停止的实例")
    start_parser.add_argument("--account", type=int, help="指定账户索引")
    start_parser.set_defaults(func=cmd_start)

    # stop 命令
    stop_parser = subparsers.add_parser("stop", help="命停实例")
    stop_parser.add_argument("instance_id", help="实例 ID")
    stop_parser.add_argument("--account", type=int, help="指定账户索引")
    stop_parser.set_defaults(func=cmd_stop)

    # info 命令
    info_parser = subparsers.add_parser("info", help="查看实例详情")
    info_parser.add_argument("instance_id", help="实例 ID")
    info_parser.add_argument("--account", type=int, help="指定账户索引")
    info_parser.set_defaults(func=cmd_info)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()