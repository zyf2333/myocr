import base64
from datetime import datetime
from typing import Dict

import ddddocr
import uvicorn
from fastapi import FastAPI, Body, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse

app = FastAPI(title='文档', description='', version="1.0.4")
app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    # allow_origins=["*"],
    allow_origin_regex='https?://.*',  # 改成用正则就行了
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=True,
    # allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    # expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc):
    print("{}".format(request.headers))
    ip = request.headers.get("remote-host")
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('{} | IP地址= {}'.format(time, ip))
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/device", summary="test", description="test", tags=[""])
async def device(request: Request, data: Dict):
    print("{}".format(request.headers))
    ip = request.headers.get("remote-host")
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('device:{} | IP地址={} | {}'.format(time, ip, data))
    return "success"


@app.post("/ocr/code", summary='识别图片内文字/字母', description='普通图片验证码识别，上传图片的Base64编码', tags=['图片验证码识别'])
async def identify_GeneralCAPTCHA(request: Request, img: str = Body(..., title='验证码图片Bse64文本', embed=True)):
    print("{}".format(request.headers))
    ip = request.headers.get("remote-host")
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    base64_data = base64.b64decode(img)
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(base64_data)
    print('{} | IP地址={} | 识别结果:{}'.format(time, ip, res))
    return res


@app.post("/math", summary='识别算术验证码', description='算术题验证码识别，上传图片的Base64编码，提供两个返回，solution_result为识别结果',
          tags=['图片验证码识别'])
async def identify_ArithmeticCAPTCHA(img: str = Body(..., title='验证码图片Bse64文本', embed=True)):
    base64_data = base64.b64decode(img)
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(base64_data)
    print("res:---------->" + res)
    if "+" or '-' or 'x' or '/' or '÷' or '*' not in res:
        zhi = "Calculation error"
    if '+' in res:
        a = res.split('+')[0]
        b = res.split('+')[1]
        zhi = int(a) + int(b)
    if '-' in res:
        a = res.split('-')[0]
        b = res.split('-')[1]
        zhi = int(a) - int(b)
    if 'x' in res:
        a = res.split('x')[0]
        b = res.split('x')[1]
        zhi = int(a) * int(b)
    if '/' in res:
        a = res.split('/')[0]
        b = res.split('/')[1]
        zhi = int(a) / int(b)
    if '÷' in res:
        a = res.split('÷')[0]
        b = res.split('÷')[1]
        zhi = int(a) / int(b)
    if '*' in res:
        a = res.split('*')[0]
        b = res.split('*')[1]
        zhi = int(a) * int(b)

    return {"solution_result": zhi,
            "raw_result": res
            }


if __name__ == '__main__':
    uvicorn.run(app, port=6688, host="0.0.0.0")
