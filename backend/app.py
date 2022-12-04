from flask import Flask, request
import docker
import json
from flask_cors import CORS, cross_origin
from playwright.sync_api import sync_playwright
import time

app = Flask(__name__)
cors = CORS(app)


client = docker.from_env()
containers = client.containers.list()


@app.route('/')
@cross_origin()
def hello_world():
    return {"data": "Hello, World!"}

@app.route('/start/<id>')
@cross_origin()
def start_container(id):
    for container in containers:
        if container.id == id:
            container.unpause()
    return "Container started"

@app.route('/stop/<id>')
@cross_origin()
def stop_container(id):
    for container in containers:
        if container.id == id:
            container.pause()
    return "Container paused"

@app.route('/kill/<id>')
@cross_origin()
def kill_container(id):
    for container in containers:
        if container.id == id:
            container.kill()
    return "Container killed"     

@app.route('/containers')
@cross_origin()
def docker_stats():
    containers = client.containers.list(all=True)
    stats = [{'status': container.status, 'id': container.id, 'name': container.name, 'stats': container.stats(stream=False), 'logs': container.logs(tail=1).decode()} for container in containers]
    return stats

######################################
# GPT stuff

# PLAY = sync_playwright().start()
# BROWSER = PLAY.chromium.launch(
#         # 指定本机用户缓存地址
#         # user_data_dir=__USER_DATE_DIR_PATH__,
#         # 指定本机google客户端exe的路径
#         # executable_path='/Applications/Google Chrome.app.',
#         # 要想通过这个下载文件这个必然要开  默认是False
#         # accept_downloads=True,
#         # 设置不是无头模式
#         headless=False,
#         # bypass_csp=True,
#         slow_mo=10,
#         # 跳过检测
#         args=['--disable-blink-features=AutomationControlled']
#     )
# PAGE = BROWSER.new_page()

# def get_input_box():
#     """Get the child textarea of `PromptTextarea__TextareaWrapper`"""
#     return PAGE.query_selector("textarea")

# def is_logged_in():
#     # See if we have a textarea with data-id="root"
#     return get_input_box() is not None

# def send_message(message):
#     # Send the message
#     box = get_input_box()
#     box.click()
#     box.fill(message)
#     box.press("Enter")

# def get_last_message():
#     """Get the latest message"""
#     page_elements = PAGE.query_selector_all("div[class*='ConversationItem__Message']")
#     last_element = page_elements[-1]
#     return last_element.inner_text()

@app.route("/chat", methods=["GET"])
def chat():
    message = flask.request.args.get("q")
    time.sleep(10) # TODO: there are about ten million ways to be smarter than this
    response = seleniumScript(message)
    print("Response: ", response)
    return response



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import platform
from webdriver_manager.chrome import ChromeDriverManager

def seleniumScript():
    PLATFORM = 'https://chat.openai.com/'
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    driver.get(PLATFORM)
    return "Hello"
    # op.add_argument('headless') 


# def start_browser():
#     PAGE.goto("https://chat.openai.com/")
#     if not is_logged_in():
#         print("Please log in to OpenAI Chat")
#         print("Press enter when you're done")
#         # input()
#     else:
#         print("Logged in")
#         # send_message('Hello')
#         # print(get_last_message())
#         # APP.run(port=5001, threaded=False)

################

if __name__ in "__main__":
    # start_browser()
    app.run(host="0.0.0.0", port=5000, debug=True)
