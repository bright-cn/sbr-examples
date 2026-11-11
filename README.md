sbr-examples
============

使用常见浏览器控制库调用 Bright Data [抓取浏览器](https://www.bright.cn/products/scraping-browser)的示例。

- *-basic：对目标页面进行简单抓取
- *-captcha：打开页面并等待验证码破解
- *-advanced：检查抓取会话，并使用 JS 代码片段进行高级爬取
- *-proxy-location：抓取前更改代理位置
- *-file-download：获取浏览器下载的文件

如何运行示例
-------------------

你需要在控制面板中获取抓取浏览器的凭据。以 `USER:PASS` 格式将其作为环境变量 `AUTH` 传入

对于 Unix shell：
```bash
export AUTH=brd-customer-hl_01234567-zone-scraping_browser:abcdefghijkl
```

对于 Windows cmd：
```cmd
set AUTH=brd-customer-hl_01234567-zone-scraping_browser:abcdefghijkl
```

对于 PowerShell：
```powershell
$Env:AUTH = 'brd-customer-hl_01234567-zone-scraping_browser:abcdefghijkl'
```

你还可以传入环境变量 `TARGET_URL`，以更改默认目标网站。

nodejs
------

使用 npm 包管理器安装所需的库

```
$ cd nodejs/puppeteer-basic
.../puppeteer-basic$ npm install
.../puppeteer-basic$ node scrape.js
```

python
------

使用 pip 包管理器安装所需的库

```
$ cd python/playwright-async-basic
.../playwright-async-basic$ pip3 install -r requirements.txt
.../playwright-async-basic$ python3 scrape.py
```

csharp
------

使用 dotnet 工具安装所需的库、构建并运行

```
$ cd csharp/puppeteer-basic
.../puppeteer-basic$ dotnet run
```

java
----

使用 Maven 工具将程序与所需的库一起打包为可执行 JAR 文件

```
$ cd java/playwright-basic
.../playwright-basic$ mvn package
.../playwright-basic$ java -jar target/sbr-examples-1.0.jar
```

golang
------

使用 Go 工具链安装所需的库、构建并运行

```
$ cd golang/playwright-basic
.../golang/playwright-basic$ go get
.../golang/playwright-basic$ go run scrape.go
```

