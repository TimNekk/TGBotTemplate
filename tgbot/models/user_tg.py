import datetime
import typing

from aiogram import types, Bot
from aiogram.types import base
from aiogram.utils import exceptions
from aiogram.utils.markdown import hlink
from loguru import logger

from tgbot.models.user import User


class UserTG(User):
    bot: Bot

    @property
    def info(self) -> str | None:
        if self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        elif self.username:
            return self.username
        return None

    @property
    def link(self) -> str | None:
        if self.username:
            return f"@{self.username}"
        return hlink(self.info, self.url if self.url else self.id)

    @property
    def url(self) -> str:
        return f"tg://user?id={self.id}"

    async def _execute_telegram_send_action(
            self,
            action: typing.Callable,
            *args: typing.Any,
            **kwargs: typing.Any
    ) -> types.Message | base.Boolean | None:
        try:
            return await action(self.id, *args, **kwargs)
        except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated) as e:
            logger.debug(f"{self}: {e.match}")
            await self.update(is_banned=True).apply()
        except exceptions.TelegramAPIError as e:
            logger.exception(f"{self}: {e}")
        return None

    async def _execute_telegram_edit_action(
            self,
            action: typing.Callable,
            *args: typing.Any,
            **kwargs: typing.Any
    ) -> types.Message | base.Boolean | None:
        try:
            return await action(*args, **kwargs)
        except (exceptions.MessageToEditNotFound, exceptions.MessageCantBeEdited, exceptions.MessageNotModified) as e:
            logger.debug(f"{self}: {e.match}")
            raise e
        except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated) as e:
            logger.debug(f"{self}: {e.match}")
            await self.update(is_banned=True).apply()
        except exceptions.TelegramAPIError as e:
            logger.exception(f"{self}: {e}")
        return None

    async def send_message(
            self,
            text: base.String,
            parse_mode: typing.Optional[base.String] = None,
            entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            disable_web_page_preview: typing.Optional[base.Boolean] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_message,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_photo(
            self,
            photo: typing.Union[base.InputFile, base.String],
            caption: typing.Optional[base.String] = None,
            parse_mode: typing.Optional[base.String] = None,
            caption_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_photo,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_document(
            self,
            document: typing.Union[base.InputFile, base.String],
            thumb: typing.Union[base.InputFile, base.String, None] = None,
            caption: typing.Optional[base.String] = None,
            parse_mode: typing.Optional[base.String] = None,
            caption_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            disable_content_type_detection: typing.Optional[base.Boolean] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply,
            None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_document,
            document=document,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_chat_action(
            self,
            action: base.String) -> base.Boolean:
        return await self._execute_telegram_send_action(
            self.bot.send_chat_action,
            action)

    async def send_video(
            self,
            video: typing.Union[base.InputFile, base.String],
            duration: typing.Optional[base.Integer] = None,
            width: typing.Optional[base.Integer] = None,
            height: typing.Optional[base.Integer] = None,
            thumb: typing.Union[base.InputFile, base.String, None] = None,
            caption: typing.Optional[base.String] = None,
            parse_mode: typing.Optional[base.String] = None,
            caption_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            supports_streaming: typing.Optional[base.Boolean] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_video,
            video=video,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            supports_streaming=supports_streaming,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_audio(
            self,
            audio: typing.Union[base.InputFile, base.String],
            caption: typing.Optional[base.String] = None,
            parse_mode: typing.Optional[base.String] = None,
            caption_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            duration: typing.Optional[base.Integer] = None,
            performer: typing.Optional[base.String] = None,
            title: typing.Optional[base.String] = None,
            thumb: typing.Union[base.InputFile, base.String, None] = None,
            disable_content_type_detection: typing.Optional[base.Boolean] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_audio,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_animation(
            self,
            animation: typing.Union[base.InputFile, base.String],
            duration: typing.Optional[base.Integer] = None,
            width: typing.Optional[base.Integer] = None,
            height: typing.Optional[base.Integer] = None,
            thumb: typing.Union[typing.Union[base.InputFile, base.String], None] = None,
            caption: typing.Optional[base.String] = None,
            parse_mode: typing.Optional[base.String] = None,
            caption_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            disable_content_type_detection: typing.Optional[base.Boolean] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply], None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_animation,
            animation=animation,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_voice(
            self,
            voice: typing.Union[base.InputFile, base.String],
            caption: typing.Optional[base.String] = None,
            parse_mode: typing.Optional[base.String] = None,
            caption_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            duration: typing.Optional[base.Integer] = None,
            disable_content_type_detection: typing.Optional[base.Boolean] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_voice,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_dice(
            self,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            emoji: typing.Optional[base.String] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_dice,
            message_thread_id=message_thread_id,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_contact(
            self,
            phone_number: base.String,
            first_name: base.String,
            last_name: typing.Optional[base.String] = None,
            vcard: typing.Optional[base.String] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_contact,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_location(
            self,
            latitude: base.Float,
            longitude: base.Float,
            horizontal_accuracy: typing.Optional[base.Float] = None,
            live_period: typing.Optional[base.Integer] = None,
            heading: typing.Optional[base.Integer] = None,
            proximity_alert_radius: typing.Optional[base.Integer] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_location,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_venue(
            self,
            latitude: base.Float,
            longitude: base.Float,
            title: base.String,
            address: base.String,
            foursquare_id: typing.Optional[base.String] = None,
            foursquare_type: typing.Optional[base.String] = None,
            google_place_id: typing.Optional[base.String] = None,
            google_place_type: typing.Optional[base.String] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_venue,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_game(
            self,
            game_short_name: base.String,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Optional[types.InlineKeyboardMarkup] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_game,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_media_group(
            self,
            media: typing.Union[types.MediaGroup, typing.List],
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
    ) -> typing.List[types.Message] | None:
        return await self._execute_telegram_send_action(
            self.bot.send_media_group,
            media=media,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply)

    async def send_poll(
            self,
            question: base.String,
            options: typing.List[base.String],
            is_anonymous: typing.Optional[base.Boolean] = None,
            type: typing.Optional[base.String] = None,
            allows_multiple_answers: typing.Optional[base.Boolean] = None,
            correct_option_id: typing.Optional[base.Integer] = None,
            explanation: typing.Optional[base.String] = None,
            explanation_parse_mode: typing.Optional[base.String] = None,
            explanation_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            open_period: typing.Optional[base.Integer] = None,
            close_date: typing.Union[base.Integer, datetime.datetime, datetime.timedelta, None] = None,
            is_closed: typing.Optional[base.Boolean] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_poll,
            question=question,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_sticker(
            self,
            sticker: typing.Union[base.InputFile, base.String],
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_sticker,
            sticker=sticker,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_invoice(
            self,
            title: base.String,
            description: base.String,
            payload: base.String,
            provider_token: base.String,
            currency: base.String,
            prices: typing.List[types.LabeledPrice],
            max_tip_amount: typing.Optional[base.Integer] = None,
            suggested_tip_amounts: typing.Optional[typing.List[base.Integer]] = None,
            start_parameter: typing.Optional[base.String] = None,
            provider_data: typing.Optional[typing.Dict] = None,
            photo_url: typing.Optional[base.String] = None,
            photo_size: typing.Optional[base.Integer] = None,
            photo_width: typing.Optional[base.Integer] = None,
            photo_height: typing.Optional[base.Integer] = None,
            need_name: typing.Optional[base.Boolean] = None,
            need_phone_number: typing.Optional[base.Boolean] = None,
            need_email: typing.Optional[base.Boolean] = None,
            need_shipping_address: typing.Optional[base.Boolean] = None,
            send_phone_number_to_provider: typing.Optional[base.Boolean] = None,
            send_email_to_provider: typing.Optional[base.Boolean] = None,
            is_flexible: typing.Optional[base.Boolean] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Optional[types.InlineKeyboardMarkup] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_invoice,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def send_video_note(
            self,
            video_note: typing.Union[base.InputFile, base.String],
            duration: typing.Optional[base.Integer] = None,
            length: typing.Optional[base.Integer] = None,
            thumb: typing.Union[base.InputFile, base.String, None] = None,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
            reply_to_message_id: typing.Optional[base.Integer] = None,
            allow_sending_without_reply: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply, None] = None,
    ) -> types.Message:
        return await self._execute_telegram_send_action(
            self.bot.send_video_note,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)

    async def edit_message_text(
            self,
            text: base.String,
            message_id: typing.Optional[base.Integer] = None,
            inline_message_id: typing.Optional[base.String] = None,
            parse_mode: typing.Optional[base.String] = None,
            entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            disable_web_page_preview: typing.Optional[base.Boolean] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup, None] = None,
    ) -> typing.Union[types.Message, base.Boolean]:
        try:
            return await self._execute_telegram_edit_action(
                self.bot.edit_message_text,
                text=text,
                chat_id=self.id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup)
        except (exceptions.MessageToEditNotFound, exceptions.MessageCantBeEdited):
            return await self.send_message(
                text=text,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup)

    async def edit_message_caption(
            self,
            message_id: typing.Optional[base.Integer] = None,
            inline_message_id: typing.Optional[base.String] = None,
            caption: typing.Optional[base.String] = None,
            parse_mode: typing.Optional[base.String] = None,
            caption_entities: typing.Optional[typing.List[types.MessageEntity]] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup, None] = None
    ) -> typing.Union[types.Message, base.Boolean]:
        try:
            return await self._execute_telegram_edit_action(
                self.bot.edit_message_caption,
                chat_id=self.id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                reply_markup=reply_markup)
        except (exceptions.MessageToEditNotFound, exceptions.MessageCantBeEdited):
            return await self.send_message(
                text=caption,
                parse_mode=parse_mode,
                entities=caption_entities,
                reply_markup=reply_markup)

    async def edit_message_media(
            self,
            media: types.InputMedia,
            message_id: typing.Optional[base.Integer] = None,
            inline_message_id: typing.Optional[base.String] = None,
            reply_markup: typing.Optional[types.InlineKeyboardMarkup] = None,
    ) -> typing.Union[types.Message, typing.List[types.Message], base.Boolean]:
        try:
            return await self._execute_telegram_edit_action(
                self.bot.edit_message_media,
                media=media,
                chat_id=self.id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                reply_markup=reply_markup)
        except (exceptions.MessageToEditNotFound, exceptions.MessageCantBeEdited):
            return await self.send_media_group(media=list(media))

    async def edit_message_reply_markup(
            self,
            message_id: typing.Optional[base.Integer] = None,
            inline_message_id: typing.Optional[base.String] = None,
            reply_markup: typing.Union[types.InlineKeyboardMarkup, None] = None
    ) -> typing.Union[types.Message, base.Boolean]:
        return await self._execute_telegram_edit_action(
            self.bot.edit_message_reply_markup,
            chat_id=self.id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup)

    async def edit_message_live_location(
            self,
            latitude: base.Float,
            longitude: base.Float,
            message_id: typing.Optional[base.Integer] = None,
            inline_message_id: typing.Optional[base.String] = None,
            horizontal_accuracy: typing.Optional[base.Float] = None,
            heading: typing.Optional[base.Integer] = None,
            proximity_alert_radius: typing.Optional[base.Integer] = None,
            reply_markup: typing.Optional[types.InlineKeyboardMarkup] = None,
    ) -> typing.Union[types.Message, base.Boolean]:
        try:
            return await self._execute_telegram_edit_action(
                self.bot.edit_message_live_location,
                latitude=latitude,
                longitude=longitude,
                chat_id=self.id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                horizontal_accuracy=horizontal_accuracy,
                heading=heading,
                proximity_alert_radius=proximity_alert_radius,
                reply_markup=reply_markup)
        except (exceptions.MessageToEditNotFound, exceptions.MessageCantBeEdited):
            return await self.send_location(
                latitude=latitude,
                longitude=longitude,
                horizontal_accuracy=horizontal_accuracy,
                heading=heading,
                proximity_alert_radius=proximity_alert_radius,
                reply_markup=reply_markup)

    async def delete_message(
            self,
            message_id: typing.Optional[base.Integer] = None,
    ) -> base.Boolean | None:
        try:
            return await self.bot.delete_message(chat_id=self.id, message_id=message_id)
        except (exceptions.MessageToDeleteNotFound, exceptions.MessageCantBeDeleted) as e:
            logger.exception(f"{self}: {e.match}")
        except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated) as e:
            logger.debug(f"{self}: {e.match}")
            await self.update(is_banned=True).apply()
        except exceptions.TelegramAPIError as e:
            logger.exception(f"{self}: {e}")
        return None

    async def answer_callback_query(
            self,
            callback_query_id: base.String,
            text: typing.Optional[base.String] = None,
            show_alert: typing.Optional[base.Boolean] = None,
            url: typing.Optional[base.String] = None,
            cache_time: typing.Optional[base.Integer] = None,
    ) -> base.Boolean | None:
        try:
            return await self.bot.answer_callback_query(
                callback_query_id=callback_query_id,
                text=text,
                show_alert=show_alert,
                url=url,
                cache_time=cache_time)
        except exceptions.InvalidQueryID as e:
            logger.exception(f"{self}: {e.match}")
        except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated) as e:
            logger.debug(f"{self}: {e.match}")
            await self.update(is_banned=True).apply()
        except exceptions.TelegramAPIError as e:
            logger.exception(f"{self}: {e}")
        return None

    async def forward_message(
            self,
            chat_id: typing.Union[base.Integer, base.String],
            from_chat_id: typing.Union[base.Integer, base.String],
            message_id: base.Integer,
            message_thread_id: typing.Optional[base.Integer] = None,
            disable_notification: typing.Optional[base.Boolean] = None,
            protect_content: typing.Optional[base.Boolean] = None,
    ) -> types.Message | None:
        try:
            return await self.bot.forward_message(
                chat_id=chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id,
                message_thread_id=message_thread_id,
                disable_notification=disable_notification,
                protect_content=protect_content)
        except (exceptions.MessageToForwardNotFound, exceptions.MessageCantBeForwarded) as e:
            logger.exception(f"{self}: {e.match}")
        except (exceptions.BotBlocked, exceptions.ChatNotFound, exceptions.UserDeactivated) as e:
            logger.debug(f"{self}: {e.match}")
            await self.update(is_banned=True).apply()
        except exceptions.TelegramAPIError as e:
            logger.exception(f"{self}: {e}")
        return None
