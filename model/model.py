class OracleInstance:
    def __init__(self, **kwargs) -> None:
        self.ip = kwargs.get("ip", "")
        self.region = kwargs.get("region", "")
        self.display_name = kwargs.get("display_name", "")
        self.time_created = kwargs.get("time_created", "")
        self.lifecycle_state = kwargs.get("lifecycle_state", "")
        self.processor_description= kwargs.get("processor_description", "")