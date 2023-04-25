import oci
from conf.config import ACCOUNTS
from model.model import OracleInstance

def start_stopped_insance(compute_client, instance_id, action="START"):
    # 发送请求
    response = compute_client.instance_action(instance_id, action)
    # 等待实例启动
    wait_until_response = oci.wait_until(
        compute_client,
        compute_client.get_instance(instance_id),
        'lifecycle_state',
        'RUNNING',
        max_wait_seconds=1800,
        succeed_on_not_found=True
    )


def get_instance_ip(compute_client, compartment_id, instance_id, config):
    ips = []
    try:
        vnic_attachments = oci.pagination.list_call_get_all_results(
            compute_client.list_vnic_attachments,
            compartment_id=compartment_id,
            instance_id=instance_id
        ).data
        virtual_network_client = oci.core.VirtualNetworkClient(
            config, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)
        vnics = [virtual_network_client.get_vnic(
            va.vnic_id).data for va in vnic_attachments]
        for vnic in vnics:
            if vnic.public_ip:
                ips.append(vnic.public_ip)
    except Exception as e:
        pass
    return ips


def get_instance_from_account() -> list:
    # 配置 SDK
    all_instances = []
    for config in ACCOUNTS:
        # 初始化 ComputeClient
        compute_client = oci.core.ComputeClient(config)
        compartment_id = config["compartment_id"]
        # 获取所有实例
        instances = compute_client.list_instances(compartment_id).data
        # 打印实例 ID 和名称
        res = []
        for instance in instances:
            instance_id = instance.id

            ips = get_instance_ip(
                compute_client, compartment_id, instance_id, config)
            oi = OracleInstance(**{
                "ip": ips[0] if ips else "",
                "region": instance.region,
                "display_name": instance.display_name,
                "time_created": instance.time_created.strftime("%Y-%m-%d %H:%M:%S"),
                "lifecycle_state": instance.lifecycle_state,
                "processor_description": instance.shape_config.processor_description
            })
            res.append(oi)
            print("Instance ID: {}, Instance Name: {}".format(
                instance.id, instance.display_name))
            if instance.lifecycle_state == "STOPPED":
                start_stopped_insance(compute_client, instance_id)
        all_instances.extend(res)
    return all_instances
