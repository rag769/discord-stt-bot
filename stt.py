import asyncio
import discord
import speech_recognition as sr

from discord.ext import commands, voice_recv
from discord.ext.voice_recv.extras import SpeechRecognitionSink


class SpeechToText(commands.Cog):
    def __init__(self, bot: commands.Bot, wit_token: str):
        self.bot = bot
        self._wit_token = wit_token

    @commands.command()
    async def kaku(self, ctx):
        def get_process_callback():
            def recognize_wit(
                recognizer: sr.Recognizer, audio: sr.AudioData, user: discord.Member
            ):
                if not user:
                    return None
                text = None
                try:
                    duration = (
                        len(audio.frame_data) / audio.sample_rate / audio.sample_width
                    )
                    print(f"stt from {user.name} ({duration} sec)")
                    if duration >= 1.0:
                        text = recognizer.recognize_wit(audio, key=self._wit_token)
                except sr.UnknownValueError:
                    print("ERROR: Couldn't understand.")
                except sr.RequestError as e:
                    print("ERROR: Could not request results from Wit.ai service; {0}".format(e))
                return text

            return recognize_wit

        def get_text_callback():
            def send(user: discord.Member, text: str):
                if not user:
                    return
                name = user.display_name
                if len(name) > 10:
                    name = name[:10] + "..."
                message = f"{name}: \n　{text}"
                asyncio.run_coroutine_threadsafe(
                    ctx.channel.send(message), self.bot.loop
                )

            return send

        if not ctx.author.voice:
            await ctx.send("どの装備を精錬するんだい？")
            return
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
            vc.listen(
                SpeechRecognitionSink(
                    process_cb=get_process_callback(), text_cb=get_text_callback()
                )
            )
            await ctx.send("カン!カン!カン!!")
        else:
            await ctx.send("おおっと！もう別の文字起こしをしているみたいだな")

    @commands.command()
    async def kakanai(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_connected():
            try:
                await ctx.voice_client.disconnect()
                await ctx.send("久々に良い物が書けた。")
            except:
                ...
