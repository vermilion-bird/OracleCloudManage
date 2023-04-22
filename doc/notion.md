## 申请api token

## 注意

#### 需要给page或Database添加链接
![image-20230422155321790](../image/image-20230422155321790.png)


### ###  创建Database
```
curl --location --request POST 'https://api.notion.com/v1/databases/' \
--header 'Authorization: Bearer '"$NOTION_API_KEY"'' \
--header 'Content-Type: application/json' \
--header 'Notion-Version: 2022-06-28' \
--data '{
    "parent": {
        "type": "page_id",
        "page_id": "98ad959b-2b6a-4774-80ee-00246fb0ea9b"
    },
    "icon": {
    	"type": "emoji",
			"emoji": "📝"
  	},
  	"cover": {
  		"type": "external",
    	"external": {
    		"url": "https://website.domain/images/image.png"
    	}
  	},
    "title": [
        {
            "type": "text",
            "text": {
                "content": "Grocery List",
                "link": null
            }
        }
    ],
    "properties": {
        "Name": {
            "title": {}
        },
        "Description": {
            "rich_text": {}
        },
        "In stock": {
            "checkbox": {}
        },
        "Food group": {
            "select": {
                "options": [
                    {
                        "name": "🥦Vegetable",
                        "color": "green"
                    },
                    {
                        "name": "🍎Fruit",
                        "color": "red"
                    },
                    {
                        "name": "💪Protein",
                        "color": "yellow"
                    }
                ]
            }
        },
        "Price": {
            "number": {
                "format": "dollar"
            }
        },
        "Last ordered": {
            "date": {}
        },
        "Meals": {
          "relation": {
            "database_id": "668d797c-76fa-4934-9b05-ad288df2d136",
            "single_property": {}
          }
    		},
        "Number of meals": {
          "rollup": {
            "rollup_property_name": "Name",
            "relation_property_name": "Meals",
            "function": "count"
          }
        },
        "Store availability": {
            "type": "multi_select",
            "multi_select": {
                "options": [
                    {
                        "name": "Duc Loi Market",
                        "color": "blue"
                    },
                    {
                        "name": "Rainbow Grocery",
                        "color": "gray"
                    },
                    {
                        "name": "Nijiya Market",
                        "color": "purple"
                    },
                    {
                        "name": "Gus'\''s Community Market",
                        "color": "yellow"
                    }
                ]
            }
        },
        "+1": {
            "people": {}
        },
        "Photo": {
            "files": {}
        }
    }
}'
```

###  更新行

```
curl https://api.notion.com/v1/pages/c478cf15-6ww4225f9-ba06-2e4bb9df8b27   -H 'Authorization: Bearer $NOTION_API_KEY'   -H "Content-Type: application/json"   -H "Notion-Version: 2022-06-28"   -X PATCH  --data '{
  "properties": {
    "display_name": { "title": [
                    {
                        "text": {
                            "content": "instance.display_name"
                        }
                    }
                ] }
  }
}'


```
###  新增行

```json
{"parent": {"type": "page_id","page_id": "c7ce0d3e60ff40508bes32fda39ff3c"},"icon": {"type": "emoji","emoji": "📝"},"cover": {"type": "external","external": {"url": "https://website.domain/images/image.png"}},"title": [{"type": "text","text": {"content": "Grocery List","link": None}}],"properties": {"Name": {"title": {}}}
}
```



