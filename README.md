# Spider

### 用到的库：

- scrapy
- pillow
- requests
- lxml
- itchat

### 项目结构：

```python
.
├── Crawler
│   ├── Crawler
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── spiders
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       ├── zhms.py
│   │       └── zhms_content.py
│   ├── Images
│   │   └── full
│   ├── Tools
│   │   ├── ProxyIP.py
│   │   ├── UserAgent.py
│   │   ├── __pycache__
│   │   ├── proxyip.json
│   │   └── user_agents.json
│   └── scrapy.cfg
├── ITChat
│   ├── Search.py
│   ├── __pycache__
│   └── main.py
└── README.md
```

