使用 Oracle Cloud Infrastructure Python SDK 来获取 Oracle 云主机的账户实例。以下是一些基本步骤：

1. 安装 Oracle Cloud Infrastructure Python SDK
```
pip install oci
```
1. 配置 SDK

您需要在 Oracle Cloud Infrastructure 控制台上创建一个 API 密钥对，以便在 Python 代码中进行身份验证。请按照以下步骤操作：

- 在 OCI 控制台上，导航到用户设置。
- 点击「添加密钥」。
- 选择「API 密钥对」，并为其命名。
- 下载密钥文件。

使用该密钥文件，您可以在 Python 代码中进行身份验证。请参阅下面的示例代码。

3. 编写 Python 代码

以下是获取 Oracle 云主机账户实例的示例 Python 代码：

```python
import oci

# 配置 SDK
config = oci.config.from_file("~/.oci/config", "DEFAULT")

# 初始化 ComputeClient
compute_client = oci.core.ComputeClient(config)

# 获取所有实例
instances = compute_client.list_instances(config["compartment_id"]).data

# 打印实例 ID 和名称
for instance in instances:
    print("Instance ID: {}, Instance Name: {}".format(instance.id, instance.display_name))
```

在此示例中，我们首先从配置文件中读取凭据信息，并使用这些凭据初始化 ComputeClient。然后，我们使用 `list_instances` 方法获取指定区域和区域内所有实例，并遍历所有实例以打印其 ID 和名称。

请注意，您需要将 `compartment_id` 替换为您要检索实例的区域 ID。

在 Oracle Cloud Infrastructure 控制台上查找您要检索的区域的 compartment ID。以下是一些步骤：

登录您的 Oracle Cloud Infrastructure 控制台。

导航到左侧菜单中的「Identity」（身份）。

点击「Compartments」（区域）。

在此页面上，您将看到列出的所有区域。您可以点击相应区域的名称以查看其 compartment ID。

您还可以通过 API 或 CLI 获取 compartment ID。有关如何使用 API 或 CLI 进行此操作的信息，请参阅 Oracle Cloud Infrastructure 文档。