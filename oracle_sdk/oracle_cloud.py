import oci
import logging
from conf.config import ACCOUNTS
from model.model import OracleInstance

logger = logging.getLogger(__name__)


def get_all_accounts():
    """返回所有账户配置"""
    return ACCOUNTS


def stop_instance(compute_client, instance_id, action="STOP"):
    """停止实例"""
    response = compute_client.instance_action(instance_id, action)
    instance = oci.wait_until(
        compute_client,
        compute_client.get_instance(instance_id),
        'lifecycle_state',
        'STOPPED',
        max_wait_seconds=1800,
        succeed_on_not_found=True
    )
    return instance.data


def start_instance(compute_client, instance_id, action="START"):
    """启动实例"""
    response = compute_client.instance_action(instance_id, action)
    instance = oci.wait_until(
        compute_client,
        compute_client.get_instance(instance_id),
        'lifecycle_state',
        'RUNNING',
        max_wait_seconds=1800,
        succeed_on_not_found=True
    )
    return instance.data


def get_instance_ip(compute_client, compartment_id, instance_id, config):
    """获取实例的公网 IP 地址"""
    ips = []
    try:
        vnic_attachments = oci.pagination.list_call_get_all_results(
            compute_client.list_vnic_attachments,
            compartment_id=compartment_id,
            instance_id=instance_id
        ).data
        virtual_network_client = oci.core.VirtualNetworkClient(
            config, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)
        vnics = [virtual_network_client.get_vnic(va.vnic_id).data for va in vnic_attachments]
        for vnic in vnics:
            if vnic.public_ip:
                ips.append(vnic.public_ip)
    except Exception as e:
        logger.warning(f"获取实例 {instance_id} 的 IP 失败: {e}")
    return ips


def _create_oracle_instance(instance, ips, instance_id, account_idx):
    """创建 OracleInstance 对象的辅助函数"""
    return OracleInstance(
        ip=ips[0] if ips else "",
        region=instance.region,
        display_name=instance.display_name,
        time_created=instance.time_created.strftime("%Y-%m-%d %H:%M:%S"),
        lifecycle_state=instance.lifecycle_state,
        processor_description=instance.shape_config.processor_description,
        instance_id=instance_id,
        account_index=account_idx
    )


def get_instance_by_id(instance_id, account_index=None):
    """按实例 ID 获取单个实例详情"""
    accounts = ACCOUNTS if account_index is None else [ACCOUNTS[account_index]]
    start_idx = 0 if account_index is None else account_index
    for idx, config in enumerate(accounts):
        compute_client = oci.core.ComputeClient(config)
        compartment_id = config["compartment_id"]
        try:
            instance = compute_client.get_instance(instance_id).data
            ips = get_instance_ip(compute_client, compartment_id, instance_id, config)
            return _create_oracle_instance(instance, ips, instance_id, start_idx + idx)
        except oci.exceptions.ServiceError as e:
            logger.debug(f"在账户 {start_idx + idx} 中未找到实例 {instance_id}: {e}")
        except Exception as e:
            logger.warning(f"获取实例 {instance_id} 时发生错误: {e}")
    return None


def list_instances(account_index=None) -> list[OracleInstance]:
    """列出所有实例，返回结构化数据"""
    accounts = ACCOUNTS if account_index is None else [ACCOUNTS[account_index]]
    all_instances = []
    for idx, config in enumerate(accounts):
        try:
            compute_client = oci.core.ComputeClient(config)
            compartment_id = config["compartment_id"]
            instances = compute_client.list_instances(compartment_id).data
            account_idx = idx if account_index is None else account_index
            for instance in instances:
                instance_id = instance.id
                ips = get_instance_ip(compute_client, compartment_id, instance_id, config)
                oi = _create_oracle_instance(instance, ips, instance_id, account_idx)
                all_instances.append(oi)
        except Exception as e:
            logger.error(f"从账户 {idx} 获取实例列表失败: {e}")
    return all_instances


def get_instance_from_account() -> list[OracleInstance]:
    """获取所有账户的实例，并自动启动停止的实例"""
    all_instances = []
    for idx, config in enumerate(ACCOUNTS):
        try:
            compute_client = oci.core.ComputeClient(config)
            compartment_id = config["compartment_id"]
            instances = compute_client.list_instances(compartment_id).data
            res = []
            for instance in instances:
                instance_id = instance.id
                ips = get_instance_ip(compute_client, compartment_id, instance_id, config)
                oi = OracleInstance(
                    ip=ips[0] if ips else "",
                    region=instance.region,
                    display_name=instance.display_name,
                    time_created=instance.time_created.strftime("%Y-%m-%d %H:%M:%S"),
                    lifecycle_state=instance.lifecycle_state,
                    processor_description=instance.shape_config.processor_description
                )
                res.append(oi)
                logger.info(f"Instance ID: {instance.id}, Instance Name: {instance.display_name}")
                if instance.lifecycle_state == "STOPPED":
                    start_instance(compute_client, instance_id)
            all_instances.extend(res)
        except Exception as e:
            logger.error(f"从账户 {idx} 获取实例失败: {e}")
    return all_instances