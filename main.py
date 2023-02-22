from colorama import Fore, init
from os import environ as env
from bs4 import BeautifulSoup
import requests
import random
import time
import re
import os

init(autoreset=True)


class FindHook:
    def __init__(this):
        this.regex = "https:\/\/.+\/api\/webhooks\/.+\/[\w-]{68}"
        this.session = requests.Session()
        this.inp = 0
        this.lang = "Python"
        this.git = f"https://github.com/search?l={this.lang}&o=desc&p=12&q=discord.com%2Fapi%2F&s=indexed&type=Code"
        this.page = 0

    def cont(this):
        web_cont = this.session.get(
            this.git,
            cookies={
                "_gh_sess": env["sess"],
                "_octo": env["octo"],
                "user_session": env["u_sess"],
            },
        ).text
        return web_cont

    def _soup(this):
        soup = BeautifulSoup(this.cont(), "html.parser")
        try:
            for x in soup.find_all("a"):
                this.page += 1
                base = str(soup.find_all("a")[this.page]["href"])
                if ".py" in base:
                    if (
                        f'https://raw.githubusercontent.com{base.replace("/blob", "").split("#")[0]}'
                        in open("./data/urls.txt", "r").read()
                    ):
                        pass
                    else:
                        open("./data/urls.txt", "a").write(
                            f'https://raw.githubusercontent.com{base.replace("/blob", "").split("#")[0]}\n'
                        )

                else:
                    pass

        except Exception as e:
            print(e)

    def _verify_hook(this):
        while True:
            prox = random.choice(open("./data/proxies.txt", "r").read().splitlines()).strip()
            uri = random.choice(open("./data/urls.txt", "r").read().splitlines())
            ii = this.session.get(
                uri,
                cookies={
                    "_gh_sess": env["sess"],
                    "_octo": env["octo"],
                    "user_session": env["u_sess"],
                },
            ).text
            base = re.findall(this.regex, ii)
            for x in base:
                time.sleep(1.5)
                req = this.session.get(
                  x, 
                  proxies={
                    "http": f"https://{random.choice(prox)}"
                  }, 
                  timeout=10
                ).status_code
                if req == 200:
                    if x in open("./data/valid.txt", "r").read():
                        print(
                            f"{Fore.RESET}>> hook: {Fore.MAGENTA}{x}\n{Fore.RESET}>> source: {Fore.MAGENTA}{uri}"
                        )
                    else:
                        print(
                            f"{Fore.RESET}>> hook: {Fore.GREEN}{x}\n{Fore.RESET}>> source: {Fore.GREEN}{uri}"
                        )
                        open("./data/valid.txt", "a").write(f"{x}:{uri}\n")

                if req == 404:
                    print(
                        f"{Fore.RESET}>> hook: {Fore.RED}{x}\n{Fore.RESET}>> source: {Fore.RED}{uri}"
                    )

                if req == 429:
                    print(
                        f"{Fore.RESET}>> hook: {Fore.YELLOW}{x}\n{Fore.RESET}>> source: {Fore.YELLOW}{uri}"
                    )


if __name__ == "__main__":
    menu = input("[1] Check Webhooks\n[2] Scrape URLs\n-> ")
    os.system("clear")  
    if menu == "1":
        FindHook()._verify_hook()
    elif menu == "2":
        FindHook()._soup()
