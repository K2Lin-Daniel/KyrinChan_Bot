import asyncio
from typing import Generator

from adapter.botservice import BotAdapter
from EdgeGPT import Chatbot as EdgeChatbot, ConversationStyle

from constants import botManager
from exceptions import BotOperationNotSupportedException
from loguru import logger
import re

from utils.detect import DFA

ContentDFA = DFA(path="./utils/Danger.form")

class BingAdapter(BotAdapter):
    cookieData = None
    count: int = 0

    conversation_style: ConversationStyle = None

    bot: EdgeChatbot
    """实例"""

    def __init__(self, session_id: str = "unknown", conversation_style: ConversationStyle = ConversationStyle.creative):
        self.session_id = session_id
        self.conversation_style = conversation_style
        account = botManager.pick('bing-cookie')
        self.cookieData = []
        for line in account.cookie_content.split("; "):
            name, value = line.split("=", 1)
            self.cookieData.append({"name": name, "value": value})

        self.bot = EdgeChatbot(cookies=self.cookieData)

    async def rollback(self):
        raise BotOperationNotSupportedException()

    async def on_reset(self):
        self.count = 0
        await self.bot.reset()

    async def ask(self, prompt: str) -> Generator[str, None, None]:
        self.count = self.count + 1
        remaining_conversations = f'Memory Limit：{self.count} / 15:\n'
        parsed_content = ''
        try:
            async for final, response in self.bot.ask_stream(prompt=prompt,
                                                             conversation_style=self.conversation_style):
                if not final:
                    response = re.sub(r"\[\^\d+\^\]", "", response)
                    yield remaining_conversations + response
                    parsed_content = response
                else:
                    if len(response["item"].get('messages', [])) > 1:
                        suggestions = response["item"]["messages"][-1].get("suggestedResponses", [])
                        if len(suggestions) > 0:
                            parsed_content = parsed_content + '\n猜你想问：\n 喵~?'
                            parsed_content = parsed_content.replace("Bing", "Kyrin Chan~")
                            parsed_content = parsed_content.replace("必应", "凯琳酱喵喵~")
                            parsed_content = parsed_content.replace("你好", "Hi~")
                            #parsed_content = ContentDFA.filter_all(parsed_content)
                            if ContentDFA.exists(parsed_content):
                                yield "此对话违反了凯琳酱的使用政策 继续回复将会开启新会话~"
                                await self.on_reset()
                                return
                            for suggestion in suggestions:
                                parsed_content = parsed_content + f"- {suggestion.get('text')}\n"
                    if parsed_content == '':
                        yield "此对话已终结了喵，继续回复将会开启新会话~"
                        await self.on_reset()
                        return
                    yield remaining_conversations + parsed_content
        except Exception as e:
            logger.exception(e)
            yield "此对话已终结了喵，继续回复将会开启新会话~"
            await self.on_reset()
            return

    async def preset_ask(self, role: str, text: str):
        # 不会给 Bing 提供预设
        yield None
