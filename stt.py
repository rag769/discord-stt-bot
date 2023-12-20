import asyncio
import discord
import speech_recognition as sr
import threading
import time

from discord.ext import commands, voice_recv
from discord.ext.voice_recv.extras import SpeechRecognitionSink


SILENT_FRAME = b"\xf8\xff\xfe"

class SpeechToText(commands.Cog):
    def __init__(self, bot: commands.Bot, wit_token: str):
        self.bot = bot
        self._wit_token = wit_token
        self._player = SilentPlayer()
        self._player.start()

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
            self._player.add(vc)
            await ctx.send("カン!カン!カン!!")
        else:
            await ctx.send("おおっと！もう別の文字起こしをしているみたいだな")

    @commands.command()
    async def kakanai(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_connected():
            try:
                self._player.delete(ctx.voice_client)
                await ctx.voice_client.disconnect()
                await ctx.send("久々に良い物が書けた。")
            except:
                ...


class SilentPlayer(threading.Thread):
    def __init__(self, interval: int = 10):
        super().__init__(daemon=True, name=f'silencespk-{id(self):x}')
        self._end: threading.Event = threading.Event()
        self._active: threading.Event = threading.Event()
        self._voice_clients = []
        self._interval: int = interval

    def start(self) -> None:
        self._end.clear()
        super().start()


    def stop(self) -> None:
        self._end.set()
        self.join(self._interval*2)

    def add(self, client: discord.VoiceClient):
        self._voice_clients.append(client)

    def delete(self, client: discord.VoiceClient):
        if client in self._voice_clients:
            self._voice_clients.remove(client)

    def run(self) -> None:
        try:
            self._do_run()
        except Exception as e:
            print(e)


    def _do_run(self) -> None:
        while not self._end.is_set():
            time.sleep(self._interval)
            for vc in self._voice_clients:
                vc.send_audio_packet(SILENT_FRAME, encode=False)