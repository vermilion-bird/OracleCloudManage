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


# 配置说明
在Oracle Cloud Infrastructure（OCI）中，配置文件中的各项配置信息在OCI控制台中的位置如下：

user: user 项是你的OCI用户的 OCID（Oracle Cloud Identifier）。你可以在OCI控制台的用户详情页面找到这个信息。在OCI控制台中，点击左上角的用户图标，然后选择用户设置（User Settings），在用户设置页面中，你可以找到用户的OCID。

fingerprint: fingerprint 项对应于你的API密钥的指纹。API密钥是用于身份验证的密钥，你可以在OCI控制台的用户详情页面中的API密钥部分创建API密钥，并在创建时获取到指纹。

key_file: key_file 项是你的私钥的文件路径。私钥是用于身份验证的密钥，你需要将私钥存储在一个安全的地方。在OCI控制台中，当你创建API密钥时，你会下载一个包含私钥的PEM文件。你可以将这个文件保存在 ~/.oci/oci_api_key.pem 或其他安全的路径下，然后在配置文件中指定这个路径。

tenancy: tenancy 项是你的OCI租户的OCID。你可以在OCI控制台的主页上找到这个信息。在OCI控制台中，点击左上角的主页图标，然后在主页中可以看到你的租户的OCID。

region: region 项是你要使用的OCI区域的标识符。OCI的不同服务在不同的区域提供，你需要选择一个合适的区域。在OCI控制台的主页上，右上角会显示当前选择的区域。你也可以在控制台的顶部导航栏中切换区域。