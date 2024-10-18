import requests
import json
import random
import os
import urllib.parse
from colorama import *
from datetime import datetime
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class PitchTalk:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.pitchtalk.app',
            'Origin': 'https://webapp.pitchtalk.app',
            'Pragma': 'no-cache',
            'Referer': 'https://webapp.pitchtalk.app/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }
        self.slugs = ['share-x', 'share-tiktok']
        self.current_slug_index = 0

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Pitch Talk - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            user_id = str(user_data['id'])
            username = str(user_data['username'])
            return user_id, username
        else:
            raise ValueError("User data not found in query.")

    def auth(self, query: str, user_id: str, username: str):
        url = 'https://api.pitchtalk.app/v1/api/auth'
        self.headers.update({'Content-Type': 'application/json'})
        data = json.dumps({
            'hash': query,
            'photoUrl': '',
            'referralCode': '3dbacc',
            'telegramId': user_id,
            'username': username
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def claim_refferal(self, token: str):
        url = 'https://api.pitchtalk.app/v1/api/users/claim-referral'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return None

    def farmings(self, token: str):
        url = 'https://api.pitchtalk.app/v1/api/farmings'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.session.get(url, headers=self.headers)

        if response.status_code != 200 or not response.text.strip():
            return None

        try:
            return response.json()
        except json.JSONDecodeError as e:
            self.log(f"[ JSON Error ]: {e}")
            return None
        
    def create_farming(self, token: str):
        url = 'https://api.pitchtalk.app/v1/api/users/create-farming'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def claim_farming(self, token: str):
        url = 'https://api.pitchtalk.app/v1/api/users/claim-farming'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def tasks(self, token: str):
        url = 'https://api.pitchtalk.app/v1/api/tasks'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def start_tasks(self, token: str, task_id: str):
        url = f'https://api.pitchtalk.app/v1/api/tasks/{task_id}/start'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
        data = {}

        response = self.session.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            return {}

    def verify_tasks(self, token: str):
        url = 'https://api.pitchtalk.app/v1/api/tasks/verify'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def generate_post_link(self, slug):
        randomNick = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
        randomId = str(random.randint(100000, 999999))

        if slug == 'share-x':
            return f"https://x.com/{randomNick}/status/{randomId}"
        elif slug == 'share-tiktok':
            return f"https://www.tiktok.com/@{randomNick}/video/{randomId}?is_from_webapp=1&sender_device=pc"

    def get_next_slug(self):
        slug = self.slugs[self.current_slug_index]
        self.current_slug_index = (self.current_slug_index + 1) % len(self.slugs)
        return slug

    def daily_tasks(self, token: str, slug: str, post_link: str):
        url = 'https://api.pitchtalk.app/v1/api/tasks/create-daily'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
        data = json.dumps({'slug': slug, 'proof': post_link})

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def question(self):
        while True:
            submit_daily = input("Submitted Daily Tasks? [y/n] -> ").strip().lower()
            if submit_daily in ["y", "n"]:
                submit_daily = submit_daily == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to submit or 'n' to skip.{Style.RESET_ALL}")

        return submit_daily
        
    def process_query(self, query, submit_daily: bool):

        user_id, username = self.load_data(query)

        account = self.auth(query, user_id, username)
        token = account['accessToken']

        if not token:
            self.log(
                f"{Fore.RED + Style.BRIGHT}[ Token Not Found:{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} Account {username} {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return None
        
        if account:
            user = account['user']
            if user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {username} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['coins']} Points {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Ticket{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['tickets']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            time.sleep(1)

            daily_reward = account['dailyRewards']
            if daily_reward['isNewDay'] and daily_reward:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Login{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {daily_reward['coins']} Points {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {daily_reward['tickets']} Tickets {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Streak{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {daily_reward['loginStreak']} Day {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Login{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Streak{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {daily_reward['loginStreak']} Day {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            time.sleep(1)

            refferal = user['referralRewards']
            if refferal != 0:
                claim = self.claim_refferal(token)
                if claim:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {user['referralRewards']} Points {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} No Available Points to Claim {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
            time.sleep(1)

            farm = self.farmings(token)

            if not farm:
                create = self.create_farming(token)
                end_farm = create['farming']['endTime']
                end_farm_utc = datetime.strptime(end_farm, '%Y-%m-%dT%H:%M:%S.%fZ')
                end_farm_wib = pytz.utc.localize(end_farm_utc).astimezone(wib).strftime('%x %X %Z')
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT} Is Started {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {end_farm_wib} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )

                farm = self.farmings(token)
            time.sleep(1)

            if farm:
                end_farm = farm['endTime']
                end_farm_utc = datetime.strptime(end_farm, '%Y-%m-%dT%H:%M:%S.%fZ')
                end_farm_wib = pytz.utc.localize(end_farm_utc).astimezone(wib).strftime('%x %X %Z')

                claim = self.claim_farming(token)
                if claim:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} 900 Points {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Not Time to Claim {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {end_farm_wib} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

            tasks = self.tasks(token)
            if tasks:
                for task in tasks:
                    if task and task.get('completedAt') is None:
                        task_id = task['id']
                        title = task['template']['title']
                        reward_coin = task['template']['rewardCoins']
                        reward_ticket = task['template']['rewardTickets']

                        slug = task['template']['slug']

                        if slug in ["share-x", "share-tiktok"]:
                            continue

                        start = self.start_tasks(token, task_id)

                        if start and start.get('status') == 'VERIFY_REQUESTED':
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ General Task{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}[ General Task{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                            )

                        verified = self.verify_tasks(token)

                        for verify in verified:
                            if verify and verify.get('status') == 'COMPLETED_CLAIMED':
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ General Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Verified{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {reward_coin} Points {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {reward_ticket} Tickets {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ General Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Verified{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ General Task{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )

            if submit_daily:
                for _ in range(2):
                    slug = self.get_next_slug()
                    post_link = self.generate_post_link(slug)
                    create_daily = self.daily_tasks(token, slug, post_link)

                    if create_daily:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Task{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {slug.upper()} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Submitted{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}Balance -750 Points {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Task{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {slug.upper()} {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}Isn't Submitted{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Task{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Skipped {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )
                
    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            submit_daily = self.question()

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query, submit_daily)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Pitch Talk - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    run = PitchTalk()
    run.main()