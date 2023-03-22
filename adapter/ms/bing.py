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
        remaining_conversations = '💾 ' + f"{'🟦' * self.count}{'⬜' * (15 - self.count)}" + '      \n\n'
        parsed_content = ''
        try:
            async for final, response in self.bot.ask_stream(prompt=prompt,
                                                             conversation_style=self.conversation_style):
                if not final:
                    response = re.sub(r"\[\^\d+\^\]", "", response)
                    yield remaining_conversations + response
                    parsed_content = parsed_content.replace("is Bing", "is Kyrin Chan~")
                    parsed_content = parsed_content.replace("这是必应", "Kyrin Chan Dayo~")
                    parsed_content = parsed_content.replace("是必应", "是凯琳酱~")
                    parsed_content = parsed_content.replace("是Bing", "是凯琳酱~")
                    parsed_content = parsed_content.replace("必应搜索", "凯琳酱~")
                    parsed_content = parsed_content.replace("搜索引擎", "猫娘")
                    parsed_content = parsed_content.replace("您好，", "Hi~")
                    parsed_content = parsed_content.replace("你好，", "Hi~")
                    parsed_content = response
                else:
                    if len(response["item"].get('messages', [])) > 1:
                        suggestions = response["item"]["messages"][-1].get("suggestedResponses", [])
                        if len(suggestions) > 0:
                            parsed_content = parsed_content + '\n💡喵~?\n '
                            parsed_content = parsed_content.replace("is Bing", "is Kyrin Chan~")
                            parsed_content = parsed_content.replace("这是必应", "Kyrin Chan Dayo~")
                            parsed_content = parsed_content.replace("是必应", "是凯琳酱~")
                            parsed_content = parsed_content.replace("是Bing", "是凯琳酱~")
                            parsed_content = parsed_content.replace("必应搜索", "凯琳酱~")
                            parsed_content = parsed_content.replace("搜索引擎", "猫娘")
                            parsed_content = parsed_content.replace("您好，", "Hi~")
                            parsed_content = parsed_content.replace("你好，", "Hi~")
                            #parsed_content = ContentDFA.filter_all(parsed_content)
                            if ContentDFA.exists(parsed_content):
                                logger.debug("Dangerous ASK:" + prompt + " Dangerous Content:" + parsed_content)
                                yield "🚫此对话违反了凯琳酱的政策 请珍惜凯琳酱，不要询问敏感的问题喵~ 继续回复将会开启新会话~♻️"
                                await self.on_reset()
                                return
                            for suggestion in suggestions:
                                parsed_content = parsed_content + f"* {suggestion.get('text')}  \n"
                    if parsed_content == '':
                        yield "⌛此对话已终结了喵 继续回复将开启新会话~♻️"
                        await self.on_reset()
                        return
                    yield remaining_conversations + parsed_content
        except Exception as e:
            logger.exception(e)
            yield "⌛此对话已终结了喵 继续回复将开启新会话~🔁"
            await self.on_reset()
            return

    async def preset_ask(self, role: str, text: str):
        # 不会给 Bing 提供预设
        yield None
