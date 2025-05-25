# Onebot V11 & Napcat Ws协议

## 元事件

### 生命周期 连接
```json
{
  "time": 1746673610,
  "self_id": 3892215616,
  "post_type": "meta_event",
  "meta_event_type": "lifecycle",
  "sub_type": "connect"
}
```

### 心跳 间隔ms
```json
{
  "time": 1746673666,
  "self_id": 3892215616,
  "post_type": "meta_event",
  "meta_event_type": "heartbeat",
  "status": {
    "online": true,
    "good": true
  },
  "interval": 30000
}
```

## 私聊消息 接收
### 纯文本
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1746673640,
  "message_id": 1136053690,
  "message_seq": 1136053690,
  "real_id": 1136053690,
  "real_seq": "770",
  "message_type": "private",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": ""
  },
  "raw_message": "你好",
  "font": 14,
  "sub_type": "friend",
  "message": [
    {
      "type": "text",
      "data": {
        "text": "你好"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "target_id": 5079132
}
```

### 引用回复
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1746673981,
  "message_id": 2127648876,
  "message_seq": 2127648876,
  "real_id": 2127648876,
  "real_seq": "772",
  "message_type": "private",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": ""
  },
  "raw_message": "[CQ:reply,id=1136053690]aa",
  "font": 14,
  "sub_type": "friend",
  "message": [
    {
      "type": "reply",
      "data": {
        "id": "1136053690"
      }
    },
    {
      "type": "text",
      "data": {
        "text": "aa"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "target_id": 5079132
}
```

### 图文混排
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1746674878,
  "message_id": 1352199344,
  "message_seq": 1352199344,
  "real_id": 1352199344,
  "real_seq": "773",
  "message_type": "private",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": ""
  },
  "raw_message": "哈哈[CQ:image,file=2490A74D2F133CC4D491994263FA51A9.png,sub_type=0,url=https://multimedia.nt.qq.com.cn/download?appid=1406&amp;fileid=EhQ7zBU4i9BPJTs7Is8Z1hI03P0MhhigNyD-Cii5qJb99pKNAzIEcHJvZFoQCtlD7JGNXCz-J7GQthR1SHoCwOw&amp;rkey=CAQSMIWZoZblav5noN2bkE4qDbEk2GVQii_LWu9AtTRtZMKbTmJEER87ZQjBY0V0SRJ5eA,file_size=7072]啊啊",
  "font": 14,
  "sub_type": "friend",
  "message": [
    {
      "type": "text",
      "data": {
        "text": "哈哈"
      }
    },
    {
      "type": "image",
      "data": {
        "summary": "",
        "file": "2490A74D2F133CC4D491994263FA51A9.png",
        "sub_type": 0,
        "url": "https://multimedia.nt.qq.com.cn/download?appid=1406&fileid=EhQ7zBU4i9BPJTs7Is8Z1hI03P0MhhigNyD-Cii5qJb99pKNAzIEcHJvZFoQCtlD7JGNXCz-J7GQthR1SHoCwOw&rkey=CAQSMIWZoZblav5noN2bkE4qDbEk2GVQii_LWu9AtTRtZMKbTmJEER87ZQjBY0V0SRJ5eA",
        "file_size": "7072"
      }
    },
    {
      "type": "text",
      "data": {
        "text": "啊啊"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "target_id": 5079132
}
```

### 表情包
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1746676132,
  "message_id": 139470241,
  "message_seq": 139470241,
  "real_id": 139470241,
  "real_seq": "776",
  "message_type": "private",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": ""
  },
  "raw_message": "[CQ:image,summary=&#91;动画表情&#93;,file=E92B84F12C57E19094B70F8292AD6FC2.jpg,sub_type=1,url=https://multimedia.nt.qq.com.cn/download?appid=1406&amp;fileid=EhQZsypcodrgKhVUyqd0M7nHeL-WaxiyAyD-Cij49ZXT-5KNAzIEcHJvZFoQWW4zYudzLueILLec_mV9-3oC67Q&amp;rkey=CAQSMIWZoZblav5noN2bkE4qDbEk2GVQii_LWu9AtTRtZMKbTmJEER87ZQjBY0V0SRJ5eA,file_size=434]",
  "font": 14,
  "sub_type": "friend",
  "message": [
    {
      "type": "image",
      "data": {
        "summary": "[动画表情]",
        "file": "E92B84F12C57E19094B70F8292AD6FC2.jpg",
        "sub_type": 1,
        "url": "https://multimedia.nt.qq.com.cn/download?appid=1406&fileid=EhQZsypcodrgKhVUyqd0M7nHeL-WaxiyAyD-Cij49ZXT-5KNAzIEcHJvZFoQWW4zYudzLueILLec_mV9-3oC67Q&rkey=CAQSMIWZoZblav5noN2bkE4qDbEk2GVQii_LWu9AtTRtZMKbTmJEER87ZQjBY0V0SRJ5eA",
        "file_size": "434"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "target_id": 5079132
}
```

### 视频
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1746714122,
  "message_id": 1402027004,
  "message_seq": 1402027004,
  "real_id": 1402027004,
  "real_seq": "777",
  "message_type": "private",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": ""
  },
  "raw_message": "[CQ:video,file=e8996238c43fed13f729cc50fa63247e.mp4,url=https://multimedia.nt.qq.com.cn/download?appid=1413&amp;format=origin&amp;orgfmt=t264&amp;spec=0&amp;rkey=CAMSmAGl6TZaIgA9RLAyCen1vjFZ5kpF1d3PMHFagjRyu1w3ho5oETvf0k0jkA6467zu9ba5kW_-lK0hWBEVOtUGIqXPVE7DyohqMqCCoORV4ZrAhfoXBJQ7a73cZ-ZEw9kGVsXTumaiPtErgDO6ZVbBB5xQAs6ZyBVHgmTo2ZEVQc-ULH9Yk8Od7kCAqqyThGz4w364TlpSA8CA4Q,file_size=1445391]",
  "font": 14,
  "sub_type": "friend",
  "message": [
    {
      "type": "video",
      "data": {
        "file": "e8996238c43fed13f729cc50fa63247e.mp4",
        "url": "https://multimedia.nt.qq.com.cn/download?appid=1413&format=origin&orgfmt=t264&spec=0&rkey=CAMSmAGl6TZaIgA9RLAyCen1vjFZ5kpF1d3PMHFagjRyu1w3ho5oETvf0k0jkA6467zu9ba5kW_-lK0hWBEVOtUGIqXPVE7DyohqMqCCoORV4ZrAhfoXBJQ7a73cZ-ZEw9kGVsXTumaiPtErgDO6ZVbBB5xQAs6ZyBVHgmTo2ZEVQc-ULH9Yk8Od7kCAqqyThGz4w364TlpSA8CA4Q",
        "file_size": "1445391"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "target_id": 5079132
}
```

### 文件
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1746714192,
  "message_id": 857587672,
  "message_seq": 857587672,
  "real_id": 857587672,
  "real_seq": "778",
  "message_type": "private",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": ""
  },
  "raw_message": "[CQ:file,file=到底是谁发明的外包？！ &#91;BV147G1zQEri_p1&#93;.mp4,file_id=5c804d00f95b09df4de35ea1c783c368_f798da46-2c17-11f0-bf38-8307ae91f46d,file_size=14438085]",
  "font": 14,
  "sub_type": "friend",
  "message": [
    {
      "type": "file",
      "data": {
        "file": "到底是谁发明的外包？！ [BV147G1zQEri_p1].mp4",
        "file_id": "5c804d00f95b09df4de35ea1c783c368_f798da46-2c17-11f0-bf38-8307ae91f46d",
        "file_size": "14438085",
        "url": "https://tjc-download.ftn.qq.com/ftn_handler/f0f728248fe401d3ead06a53a885d62b5baa1d8a148f5ba9beaeba1e76c259fc4b7e13b6318a9aaae4a835cab852eea66f66ac7ce30a11eb6ddc1a63dce3547c/?fname="
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "target_id": 5079132
}
```

### b站小程序分享
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1746714488,
  "message_id": 2090718095,
  "message_seq": 2090718095,
  "real_id": 2090718095,
  "real_seq": "784",
  "message_type": "private",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": ""
  },
  "raw_message": "[CQ:json,data={\"ver\":\"1.0.0.19\"&#44;\"prompt\":\"&#91;QQ小程序&#93;【PARA2.0】笔记以行动成果组织，告别无效记录obsidian|Notion通用\"&#44;\"config\":{\"type\":\"normal\"&#44;\"width\":0&#44;\"height\":0&#44;\"forward\":1&#44;\"autoSize\":0&#44;\"ctime\":1746714484&#44;\"token\":\"7ef326742936a965a5342563dc01a1a1\"}&#44;\"needShareCallBack\":false&#44;\"app\":\"com.tencent.miniapp_01\"&#44;\"view\":\"view_8C8E89B49BE609866298ADDFF2DBABA4\"&#44;\"meta\":{\"detail_1\":{\"appid\":\"1109937557\"&#44;\"appType\":0&#44;\"title\":\"哔哩哔哩\"&#44;\"desc\":\"【PARA2.0】笔记以行动成果组织，告别无效记录obsidian|Notion通用\"&#44;\"icon\":\"http:\\/\\/miniapp.gtimg.cn\\/public\\/appicon\\/432b76be3a548fc128acaa6c1ec90131_200.jpg\"&#44;\"preview\":\"i0.hdslb.com\\/bfs\\/share_ttl\\/13a2f253cc6ab3222017e34c64c3d5a5ce200322.jpg\"&#44;\"url\":\"m.q.qq.com\\/a\\/s\\/ec067a18b434e9b477b11a80164f6924\"&#44;\"scene\":1036&#44;\"host\":{\"uin\":5079132&#44;\"nick\":\"东风寄千愁\"}&#44;\"shareTemplateId\":\"8C8E89B49BE609866298ADDFF2DBABA4\"&#44;\"shareTemplateData\":{}&#44;\"qqdocurl\":\"https:\\/\\/b23.tv\\/P3GHoaZ?share_medium=android&amp;share_source=qq&amp;bbid=XU2D94125BDD9E969D997FB7A5594A4C2C608&amp;ts=1746714483616\"&#44;\"showLittleTail\":\"\"&#44;\"gamePoints\":\"\"&#44;\"gamePointsUrl\":\"\"&#44;\"shareOrigin\":0}}}]",
  "font": 14,
  "sub_type": "friend",
  "message": [
    {
      "type": "json",
      "data": {
        "data": "{\"ver\":\"1.0.0.19\",\"prompt\":\"[QQ小程序]【PARA2.0】笔记以行动成果组织，告别无效记录obsidian|Notion通用\",\"config\":{\"type\":\"normal\",\"width\":0,\"height\":0,\"forward\":1,\"autoSize\":0,\"ctime\":1746714484,\"token\":\"7ef326742936a965a5342563dc01a1a1\"},\"needShareCallBack\":false,\"app\":\"com.tencent.miniapp_01\",\"view\":\"view_8C8E89B49BE609866298ADDFF2DBABA4\",\"meta\":{\"detail_1\":{\"appid\":\"1109937557\",\"appType\":0,\"title\":\"哔哩哔哩\",\"desc\":\"【PARA2.0】笔记以行动成果组织，告别无效记录obsidian|Notion通用\",\"icon\":\"http:\\/\\/miniapp.gtimg.cn\\/public\\/appicon\\/432b76be3a548fc128acaa6c1ec90131_200.jpg\",\"preview\":\"i0.hdslb.com\\/bfs\\/share_ttl\\/13a2f253cc6ab3222017e34c64c3d5a5ce200322.jpg\",\"url\":\"m.q.qq.com\\/a\\/s\\/ec067a18b434e9b477b11a80164f6924\",\"scene\":1036,\"host\":{\"uin\":5079132,\"nick\":\"东风寄千愁\"},\"shareTemplateId\":\"8C8E89B49BE609866298ADDFF2DBABA4\",\"shareTemplateData\":{},\"qqdocurl\":\"https:\\/\\/b23.tv\\/P3GHoaZ?share_medium=android&share_source=qq&bbid=XU2D94125BDD9E969D997FB7A5594A4C2C608&ts=1746714483616\",\"showLittleTail\":\"\",\"gamePoints\":\"\",\"gamePointsUrl\":\"\",\"shareOrigin\":0}}}"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "target_id": 5079132
}
```

## 群聊消息 接收
### 纯文本
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1747107314,
  "message_id": 2096329721,
  "message_seq": 2096329721,
  "real_id": 2096329721,
  "real_seq": "20471",
  "message_type": "group",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": "",
    "role": "admin"
  },
  "raw_message": "test",
  "font": 14,
  "sub_type": "normal",
  "message": [
    {
      "type": "text",
      "data": {
        "text": "test"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "group_id": 757951413
}
```
### 复杂混排
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1747107572,
  "message_id": 361878627,
  "message_seq": 361878627,
  "real_id": 361878627,
  "real_seq": "20472",
  "message_type": "group",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": "",
    "role": "admin"
  },
  "raw_message": "[CQ:reply,id=265662236][CQ:at,qq=all] test message[CQ:at,qq=1090558688][CQ:image,file=E8C195761CEDA1D66763414CB8EE494E.png,sub_type=0,url=https://multimedia.nt.qq.com.cn/download?appid=1407&amp;fileid=EhTeJv9whzV7da8HpZ1A_wPjgvK_ohjTSCD_CijvnL3xwp-NAzIEcHJvZFCAvaMBWhAepoWqDDM35uuv21_CACsGegLJ7g&amp;rkey=CAISMIPGBhlMPqo7xpuFl7uQs7MbOgWDdV0-0g5bo1WQdV54LtbgFiqjY4SrkyuvDe4i3g,file_size=9299][CQ:image,summary=&#91;动画表情&#93;,file=5B0370E3C9EA52C6A1104EC94EF92022.jpg,sub_type=1,url=https://multimedia.nt.qq.com.cn/download?appid=1407&amp;fileid=EhQDrEHWNBkaVkSIOxBLC8nSLckU8hjIvQkg_wooovS98cKfjQMyBHByb2RQgL2jAVoQLFxkU7oy1ehySnWg4wrZ63oCZPg&amp;rkey=CAISMIPGBhlMPqo7xpuFl7uQs7MbOgWDdV0-0g5bo1WQdV54LtbgFiqjY4SrkyuvDe4i3g,file_size=155336]",
  "font": 14,
  "sub_type": "normal",
  "message": [
    {
      "type": "reply",
      "data": {
        "id": "265662236"
      }
    },
    {
      "type": "at",
      "data": {
        "qq": "all"
      }
    },
    {
      "type": "text",
      "data": {
        "text": " test message"
      }
    },
    {
      "type": "at",
      "data": {
        "qq": "1090558688"
      }
    },
    {
      "type": "image",
      "data": {
        "summary": "",
        "file": "E8C195761CEDA1D66763414CB8EE494E.png",
        "sub_type": 0,
        "url": "https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=EhTeJv9whzV7da8HpZ1A_wPjgvK_ohjTSCD_CijvnL3xwp-NAzIEcHJvZFCAvaMBWhAepoWqDDM35uuv21_CACsGegLJ7g&rkey=CAISMIPGBhlMPqo7xpuFl7uQs7MbOgWDdV0-0g5bo1WQdV54LtbgFiqjY4SrkyuvDe4i3g",
        "file_size": "9299"
      }
    },
    {
      "type": "image",
      "data": {
        "summary": "[动画表情]",
        "file": "5B0370E3C9EA52C6A1104EC94EF92022.jpg",
        "sub_type": 1,
        "url": "https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=EhQDrEHWNBkaVkSIOxBLC8nSLckU8hjIvQkg_wooovS98cKfjQMyBHByb2RQgL2jAVoQLFxkU7oy1ehySnWg4wrZ63oCZPg&rkey=CAISMIPGBhlMPqo7xpuFl7uQs7MbOgWDdV0-0g5bo1WQdV54LtbgFiqjY4SrkyuvDe4i3g",
        "file_size": "155336"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "group_id": 757951413
}
```
### 私聊记录的合并转发
```json
{
  "self_id": 3892215616,
  "user_id": 5079132,
  "time": 1747497034,
  "message_id": 1418180990,
  "message_seq": 1418180990,
  "real_id": 1418180990,
  "real_seq": "20879",
  "message_type": "group",
  "sender": {
    "user_id": 5079132,
    "nickname": "东风寄千愁",
    "card": "",
    "role": "admin"
  },
  "raw_message": "[CQ:forward,id=7505442611578883339]",
  "font": 14,
  "sub_type": "normal",
  "message": [
    {
      "type": "forward",
      "data": {
        "id": "7505442611578883339"
      }
    }
  ],
  "message_format": "array",
  "post_type": "message",
  "group_id": 757951413
}
```

## 私聊消息 发送
### 请求
```json
{
    "action": "send_private_msg",
    "params": {
      "user_id": "5079132",
      "message": [
          {
            "type": "text",
            "data": {
                "text": "napcat"
            }
          }
      ]
    },
    "echo": "123"
}
```
### 响应
```json
{
  "status": "ok",
  "retcode": 0,
  "data": {
    "message_id": 123039305
  },
  "message": "",
  "wording": "",
  "echo": "123"
}
```
```json
{
  "status": "failed",
  "retcode": 1200,
  "data": null,
  "message": "无法获取用户信息",
  "wording": "无法获取用户信息",
  "echo": "123"
}
```