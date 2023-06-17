from aiogram import Dispatcher, types

from tgbot.models.user import User


async def detect_block(member: types.ChatMemberUpdated) -> None:
    if member.new_chat_member.status == types.ChatMemberStatus.KICKED:
        user = await User.get(member.chat.id)
        await user.update(is_banned=True).apply()


def register(dp: Dispatcher) -> None:
    dp.register_my_chat_member_handler(detect_block)
