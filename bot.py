import discord
import asyncio
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# --- configuracion ---
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
MUDAE_ID = 432610292342587392 
# ---------------------

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'logeado como {self.user} ')
        self.loop.create_task(self.cronometro_precision())

    async def on_message(self, message):
        if message.channel.id != CHANNEL_ID:
            return

        if message.author.id != MUDAE_ID:
            return

        # check normal message content
        contenido = message.content.lower()
        
        # also check embed descriptions for "belongs to" (⸝⸝ᵕᴗᵕ⸝⸝)
        embed_contenido = ""
        if message.embeds:
            for embed in message.embeds:
                if embed.description:
                    embed_contenido += embed.description.lower()

        # check if either the message or the embed has the trigger text
        if "wished by" in contenido or "belongs to" in embed_contenido:
            print(f'¡objetivo detectado! intentando click... (๑♡⌓♡๑)')
            
            if message.components:
                for row in message.components:
                    for component in row.children:
                        if isinstance(component, discord.Button):
                            try:
                                # careful with sleep, might be too slow for high-roll servers!
                                await asyncio.sleep(1)
                                
                                await component.click()
                                print('¡clic realizado!')
                                return 
                            except Exception as e:
                                print(f'no pude hacer clic: {e}')

    async def cronometro_precision(self):
        while True:
            ahora = datetime.datetime.now()
            proximo = ahora.replace(minute=5, second=0, microsecond=0)
            if ahora >= proximo:
                proximo += datetime.timedelta(hours=1)
            
            espera = (proximo - ahora).total_seconds()
            print(f'[reloj] esperando a las {proximo.strftime("%H:%M")}... (｡-ω-)zzZ')
            
            await asyncio.sleep(espera)
            await self.enviar_tanda()

    async def enviar_tanda(self):
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            print(f'lanzando tanda de las {datetime.datetime.now().strftime("%H:%M")}...')
            for i in range(11):
                try:
                    await channel.send('$wa')
                    print(f'   -> $wa {i+1}/10')
                except Exception as e:
                    print(f'error: {e}')
                
                # espera fija de 1 segundo entre cada $wa
                await asyncio.sleep(1)
            print('tanda terminada. volviendo a esperar... ')

client = MyClient()
client.run(TOKEN)