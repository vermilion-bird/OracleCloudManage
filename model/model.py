from dataclasses import dataclass, field, asdict


@dataclass
class OracleInstance:
    """Oracle Cloud 实例数据模型"""
    ip: str = ""
    region: str = ""
    display_name: str = ""
    time_created: str = ""
    lifecycle_state: str = ""
    processor_description: str = ""
    instance_id: str = ""
    account_index: int | None = None

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return asdict(self)