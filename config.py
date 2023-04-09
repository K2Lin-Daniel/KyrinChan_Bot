from __future__ import annotations
from typing import List, Union, Literal, Dict, Optional
from pydantic import BaseModel, BaseConfig, Extra
from charset_normalizer import from_bytes
from loguru import logger
import os
import sys
import toml


class Onebot(BaseModel):
    qq: int
    """Bot 的 QQ 号"""
    manager_qq: int = 0
    """机器人管理员的 QQ 号"""
    reverse_ws_host: str = "0.0.0.0"
    """go-cqhttp 的 反向 ws 主机号"""
    reverse_ws_port: Optional[int] = None
    """go-cqhttp 的 反向 ws 端口号，填写后开启 反向 ws 模式"""


class Mirai(BaseModel):
    qq: int
    """Bot 的 QQ 号"""
    manager_qq: int = 0
    """机器人管理员的 QQ 号"""
    api_key: str = "1234567890"
    """mirai-api-http 的 verifyKey"""
    http_url: str = "http://localhost:8080"
    """mirai-api-http 的 http 适配器地址"""
    ws_url: str = "http://localhost:8080"
    """mirai-api-http 的 ws 适配器地址"""
    reverse_ws_host: str = "0.0.0.0"
    """mirai-api-http 的 反向 ws 主机号"""
    reverse_ws_port: Optional[int] = None
    """mirai-api-http 的 反向 ws 端口号，填写后开启 反向 ws 模式"""


class TelegramBot(BaseModel):
    bot_token: str
    """Bot 大爹给的 token"""
    proxy: Optional[str] = None
    """可选的代理地址，留空则检测系统代理"""
    manager_chat: Optional[int] = None
    """管理员的 chat id"""


class DiscordBot(BaseModel):
    bot_token: str
    """Discord Bot 的 token"""


class HttpService(BaseModel):
    host: str = "0.0.0.0"
    """0.0.0.0则不限制访问地址"""
    port: int = 8080
    """Http service port, 默认8080"""
    debug: bool = False
    """是否开启debug，错误时展示日志"""


class OpenAIGPT3Params(BaseModel):
    temperature: float = 0.5
    max_tokens: int = 4000
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    min_tokens: int = 1000


class OpenAIAuths(BaseModel):
    browserless_endpoint: Optional[str] = None
    """自定义无浏览器登录模式的接入点"""
    api_endpoint: Optional[str] = None
    """自定义 OpenAI API 的接入点"""

    gpt3_params: OpenAIGPT3Params = OpenAIGPT3Params()

    accounts: List[Union[OpenAIEmailAuth, OpenAISessionTokenAuth, OpenAIAccessTokenAuth, OpenAIAPIKey]] = []


class OpenAIAuthBase(BaseModel):
    mode: str = "browserless"
    """OpenAI 的登录模式，可选的值：browserless - 无浏览器登录 browser - 浏览器登录"""
    proxy: Union[str, None] = None
    """可选的代理地址"""
    driver_exec_path: Union[str, None] = None
    """可选的 Chromedriver 路径"""
    browser_exec_path: Union[str, None] = None
    """可选的 Chrome 浏览器路径"""
    conversation: Union[str, None] = None
    """初始化对话所使用的UUID"""
    paid: bool = False
    """使用 ChatGPT Plus"""
    gpt4: bool = False
    """使用 GPT-4"""
    model: Optional[str] = None
    """使用的默认模型，此选项优先级最高"""
    verbose: bool = False
    """启用详尽日志模式"""
    title_pattern: str = ""
    """自动修改标题，为空则不修改"""
    auto_remove_old_conversations: bool = False
    """自动删除旧的对话"""

    class Config(BaseConfig):
        extra = Extra.allow


class OpenAIEmailAuth(OpenAIAuthBase):
    email: str
    """OpenAI 注册邮箱"""
    password: str
    """OpenAI 密码"""
    isMicrosoftLogin: bool = False
    """是否通过 Microsoft 登录"""


class OpenAISessionTokenAuth(OpenAIAuthBase):
    session_token: str
    """OpenAI 的 session_token"""


class OpenAIAccessTokenAuth(OpenAIAuthBase):
    access_token: str
    """OpenAI 的 access_token"""


class OpenAIAPIKey(OpenAIAuthBase):
    api_key: str
    """OpenAI 的 api_key"""


class PoeCookieAuth(BaseModel):
    p_b: str
    """登陆 poe.com 后 Cookie 中 p_b 的值"""
    proxy: Optional[str] = None
    """可选的代理地址，留空则检测系统代理"""


class BingCookiePath(BaseModel):
    cookie_content: str
    """Bing 的 Cookie 文件内容"""
    proxy: Optional[str] = None
    """可选的代理地址，留空则检测系统代理"""


class BardCookiePath(BaseModel):
    cookie_content: str
    """Bard 的 Cookie 文件内容"""
    proxy: Optional[str] = None
    """可选的代理地址，留空则检测系统代理"""


class PoeAuths(BaseModel):
    accounts: List[PoeCookieAuth] = []
    """Poe 的账号列表"""


class TTSAccounts(BaseModel):
    speech_key: str
    """TTS KEY"""
    speech_service_region: str
    """TTS 地区"""
    proxy: Optional[str] = None
    """可选的代理地址，留空则检测系统代理"""


class BingAuths(BaseModel):
    show_suggestions: bool = True
    """在 Bing 的回复后加上猜你想问"""
    show_references: bool = True
    """在 Bing 的回复前加上引用资料"""
    wss_link: str = "wss://sydney.bing.com/sydney/ChatHub"
    """Bing 的 Websocket 接入点"""
    bing_endpoint: str = "https://edgeservices.bing.com/edgesvc/turing/conversation/create"
    """Bing 的会话创建接入点"""
    accounts: List[BingCookiePath] = []
    """Bing 的账号列表"""
    max_messages: int = 20
    """Bing 的最大消息数，仅展示用"""


class BardAuths(BaseModel):
    accounts: List[BardCookiePath] = []
    """Bard 的账号列表"""


class YiyanCookiePath(BaseModel):
    cookie_content: str
    """"文心一言网站的 Cookie 内容"""
    proxy: Optional[str] = None
    """可选的代理地址，留空则检测系统代理"""


class YiyanAuths(BaseModel):
    accounts: List[YiyanCookiePath] = []
    """文心一言的账号列表"""


class ChatGLMAPI(BaseModel):
    api_endpoint: str
    """自定义 ChatGLM API 的接入点"""
    max_turns: int = 10
    """最大对话轮数"""
    timeout: int = 120
    """请求超时时间（单位：秒）"""


class ChatGLMAuths(BaseModel):
    accounts: List[ChatGLMAPI] = []
    """ChatGLM的账号列表"""


class TextToImage(BaseModel):
    always: bool = False
    """强制开启，设置后所有的会话强制以图片发送"""
    default: bool = False
    """默认开启，设置后新会话默认以图片模式发送"""
    font_size: int = 30
    """字号"""
    width: int = 1000
    """生成图片宽度"""
    font_path: str = "fonts/sarasa-mono-sc-regular.ttf"
    """字体路径"""
    offset_x: int = 50
    """横坐标"""
    offset_y: int = 50
    """纵坐标"""
    wkhtmltoimage: Union[str, None] = None


class TextToSpeech(BaseModel):
    always: bool = False
    """设置后所有的会话都会转语音再发一次"""
    engine: str = "azure"
    """文字转语音引擎选择，当前有azure和vits"""
    default: str = "zh-CN-XiaoyanNeural"
    """默认设置为Azure语音音色"""


class AzureConfig(BaseModel):
    tts_speech_key: Optional[str] = None
    """TTS KEY"""
    tts_speech_service_region: Optional[str] = None
    """TTS 地区"""


class VitsConfig(BaseModel):
    api_url: str = ""
    """VITS API 地址，目前仅支持基于MoeGoe的API"""
    lang: str = "zh"
    """VITS_API目标语言"""
    speed: float = 1.4
    """VITS语言语速"""
    timeout: int = 30
    """语音生成超时时间"""




class Trigger(BaseModel):
    prefix: List[str] = [""]
    """全局的触发响应前缀，同时适用于私聊和群聊，默认不需要"""
    prefix_friend: List[str] = []
    """私聊中的触发响应前缀，默认不需要"""
    prefix_group: List[str] = []
    """群聊中的触发响应前缀，默认不需要"""

    prefix_ai: Dict[str, List[str]] = {}
    """特定类型 AI 的前缀，以此前缀开头将直接发消息至指定 AI 会话"""

    require_mention: Literal["at", "mention", "none"] = "at"
    """群内 [需要 @ 机器人 / 需要 @ 或以机器人名称开头 / 不需要 @] 才响应（请注意需要先 @ 机器人后接前缀）"""
    reset_command: List[str] = ["重置会话"]
    """重置会话的命令"""
    rollback_command: List[str] = ["回滚会话"]
    """回滚会话的命令"""
    prefix_image: List[str] = ["画", "看"]
    """图片创建前缀"""
    switch_model: str = r"切换模型 (.+)"
    """切换当前上下文的模型"""
    switch_command: str = r"切换AI (.+)"
    """切换AI的命令"""
    switch_voice: str = r"切换语音 (.+)"
    """切换tts语音音色的命令"""
    mixed_only_command: List[str] = ["图文混合模式"]
    """切换至图文混合模式"""
    image_only_command: List[str] = ["图片模式"]
    """切换至图片回复模式"""
    text_only_command: List[str] = ["文本模式"]
    """切换至文本回复模式"""
    ignore_regex: List[str] = []
    """忽略满足条件的正则表达式"""
    allowed_models: List[str] = [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
        "text-davinci-002-render-sha",
        "text-davinci-002-render-paid"
    ]
    """允许普通用户切换的模型列表"""
    allow_switching_ai: bool = True
    """允许普通用户切换AI"""



class Response(BaseModel):
    mode: str = "mixed"
    """响应模式，支持：mixed - 图文混合, for.ce-text  - 仅文字, force-image - 仅图片"""

    buffer_delay: float = 15
    """设置响应缓存时长（秒），机器人会提前返回部分文本"""

    default_ai: Union[str, None] = None
    """默认使用的 AI 类型，不填写时自动推测"""

    error_format: str = "出现故障！如果这个问题持续出现，请和我说“重置会话” 来开启一段新的会话，或者发送 “回滚对话” 来回溯到上一条对话，你上一条说的我就当作没看见。\n原因：{exc}"
    """发生错误时发送的消息，请注意可以插入 {exc} 作为异常占位符"""

    error_network_failure: str = "网络故障！连接 OpenAI 服务器失败，我需要更好的网络才能服务！\n{exc}"
    """发生网络错误时发送的消息，请注意可以插入 {exc} 作为异常占位符"""

    error_session_authenciate_failed: str = "身份验证失败！无法登录至 ChatGPT 服务器，请检查账号信息是否正确！\n{exc}"
    """发生网络错误时发送的消息，请注意可以插入 {exc} 作为异常占位符"""

    error_request_too_many: str = "糟糕！当前收到的请求太多了，我需要一段时间冷静冷静。你可以选择“重置会话”，或者过一会儿再来找我！\n预计恢复时间：{exc}\n"

    error_request_concurrent_error: str = "当前有其他人正在和我进行聊天，请稍后再给我发消息吧！"

    error_server_overloaded: str = "抱歉，当前服务器压力有点大，请稍后再找我吧！"
    """服务器提示 429 错误时的回复 """

    placeholder: str = (
        "您好！我是 Assistant，一个由 OpenAI 训练的大型语言模型。我不是真正的人，而是一个计算机程序，可以通过文本聊天来帮助您解决问题。如果您有任何问题，请随时告诉我，我将尽力回答。\n"
        "如果您需要重置我们的会话，请回复`重置会话`。"
    )
    """对空消息回复的占位符"""

    reset = "♻上下文的记忆已经被清除了喵~👋"
    """重置会话时发送的消息"""

    rollback_success = "已回滚至上一条对话，你刚刚发的我就忘记啦！"
    """成功回滚时发送的消息"""

    rollback_fail = "回滚失败，没有更早的记录了！如果你想要重新开始，请发送：{reset}"
    """回滚失败时发送的消息"""

    quote: bool = True
    """是否回复触发的那条消息"""

    timeout: float = 30.0
    """发送提醒前允许的响应时间"""

    timeout_format: str = "我还在思考中，请再等一下~"
    """响应时间过长时要发送的提醒"""

    max_timeout: float = 600.0
    """最长等待时间，超过此时间取消回应"""

    cancel_wait_too_long: str = "啊哦，这个问题有点难，让我想了好久也没想明白。试试换个问法？"
    """发送提醒前允许的响应时间"""

    max_queue_size: int = 10
    """等待处理的消息的最大数量，如果要关闭此功能，设置为 0"""

    queue_full: str = "抱歉！我现在要回复的人有点多，暂时没有办法接收新的消息了，请过会儿再给我发吧！"
    """队列满时的提示"""

    queued_notice_size: int = 3
    """新消息加入队列会发送通知的长度最小值"""

    queued_notice: str = "消息已收到！当前我还有{queue_size}条消息要回复，请您稍等。"
    """新消息进入队列时，发送的通知。 queue_size 是当前排队的消息数"""


class System(BaseModel):
    accept_group_invite: bool = False
    """自动接收邀请入群请求"""

    accept_friend_request: bool = False
    """自动接收好友请求"""


class BaiduCloud(BaseModel):
    check: bool = False
    """是否启动百度云内容安全审核"""
    baidu_api_key: str = ""
    """百度云API_KEY 24位英文数字字符串"""
    baidu_secret_key: str = ""
    """百度云SECRET_KEY 32位的英文数字字符串"""
    prompt_message: str = "[百度云]请珍惜机器人，当前返回内容不合规"
    """不合规消息自定义返回"""




class Preset(BaseModel):
    command: str = r"加载预设 (\w+)"
    keywords: dict[str, str] = {}
    loaded_successful: str = "预设加载成功！"
    scan_dir: str = "./presets"
    hide: bool = False
    """是否禁止使用其他人 .预设列表 命令来查看预设"""



class Ratelimit(BaseModel):
    warning_rate: float = 0.8
    """额度使用达到此比例时进行警告"""

    warning_msg: str = "\n\n警告：额度即将耗尽！\n目前已发送：{usage}条消息，最大限制为{limit}条消息/小时，请调整您的节奏。\n额度限制整点重置，当前服务器时间：{current_time}"
    """警告消息"""

    exceed: str = "已达到额度限制，请等待下一小时继续和我对话。"
    """超额消息"""


class Config(BaseModel):
    # === Platform Settings ===
    onebot: Optional[Onebot] = None
    mirai: Optional[Mirai] = None
    telegram: Optional[TelegramBot] = None
    discord: Optional[DiscordBot] = None
    http: Optional[HttpService] = None

    # === Account Settings ===
    openai: OpenAIAuths = OpenAIAuths()
    bing: BingAuths = BingAuths()
    bard: BardAuths = BardAuths()
    azure: AzureConfig = AzureConfig()
    yiyan: YiyanAuths = YiyanAuths()
    chatglm: ChatGLMAuths = ChatGLMAuths()
    poe: PoeAuths = PoeAuths()

    # === Response Settings ===
    text_to_image: TextToImage = TextToImage()
    text_to_speech: TextToSpeech = TextToSpeech()
    trigger: Trigger = Trigger()
    response: Response = Response()
    system: System = System()
    presets: Preset = Preset()
    ratelimit: Ratelimit = Ratelimit()
    baiducloud: BaiduCloud = BaiduCloud()
    vits: VitsConfig = VitsConfig()

    def scan_presets(self):
        for keyword, path in self.presets.keywords.items():
            if os.path.isfile(path):
                logger.success(f"检查预设：{keyword} <==> {path} [成功]")
            else:
                logger.error(f"检查预设：{keyword} <==> {path} [失败：文件不存在]")
        for root, _, files in os.walk(self.presets.scan_dir, topdown=False):
            for name in files:
                if not name.endswith(".txt"):
                    continue
                path = os.path.join(root, name)
                name = name.removesuffix('.txt')
                if name in self.presets.keywords:
                    logger.error(f"注册预设：{name} <==> {path} [失败：关键词已存在]")
                    continue
                self.presets.keywords[name] = path
                logger.success(f"注册预设：{name} <==> {path} [成功]")

    def load_preset(self, keyword):
        try:
            with open(self.presets.keywords[keyword], "rb") as f:
                if guessed_str := from_bytes(f.read()).best():
                    return str(guessed_str).replace('<|im_end|>', '').replace('\r', '').split('\n\n')
                else:
                    raise ValueError("无法识别预设的 JSON 格式，请检查编码！")

        except KeyError:
            raise ValueError("预设不存在！")
        except FileNotFoundError:
            raise ValueError("预设文件不存在！")
        except Exception as e:
            logger.exception(e)
            logger.error("配置文件有误，请重新修改！")

    OpenAIAuths.update_forward_refs()

    @staticmethod
    def __load_json_config() -> Config:
        try:
            import json
            with open("config.json", "rb") as f:
                if guessed_str := from_bytes(f.read()).best():
                    return Config.parse_obj(json.loads(str(guessed_str)))
                else:
                    raise ValueError("无法识别 JSON 格式！")
        except Exception as e:
            logger.exception(e)
            logger.error("配置文件有误，请重新修改！")
            exit(-1)

    @staticmethod
    def load_config() -> Config:
        try:
            import os
            if (
                not os.path.exists('config.cfg')
                or os.path.getsize('config.cfg') <= 0
            ) and os.path.exists('config.json'):
                logger.info("正在转换旧版配置文件……")
                Config.save_config(Config.__load_json_config())
                logger.warning("提示：配置文件已经修改为 config.cfg，原来的 config.json 将被重命名为 config.json.old。")
                try:
                    os.rename('config.json', 'config.json.old')
                except Exception as e:
                    logger.error(e)
                    logger.error("无法重命名配置文件，请自行处理。")
            with open("config.cfg", "rb") as f:
                if guessed_str := from_bytes(f.read()).best():
                    return Config.parse_obj(toml.loads(str(guessed_str)))
                else:
                    raise ValueError("无法识别配置文件，请检查是否输入有误！")
        except Exception as e:
            logger.exception(e)
            logger.error("配置文件有误，请重新修改！")
            exit(-1)

    @staticmethod
    def save_config(config: Config):
        try:
            with open("config.cfg", "wb") as f:
                parsed_str = toml.dumps(config.dict()).encode(sys.getdefaultencoding())
                f.write(parsed_str)
        except Exception as e:
            logger.exception(e)
            logger.warning("配置保存失败。")
