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
        data = json.dumps({
            'hash': query,
            'photoUrl': '',
            'referralCode': '3dbacc',
            'telegramId': user_id,
            'username': username
        })
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None

    def claim_refferal(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/users/claim-referral'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return None

    def farmings(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/farmings'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.get(url, headers=self.headers)

        if response.status_code != 200 or not response.text.strip():
            return None

        try:
            return response.json()
        except json.JSONDecodeError as e:
            self.log(f"[ JSON Error ]: {e}")
            return None
        
    def create_farming(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/users/create-farming'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def claim_farming(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/users/claim-farming'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def tasks(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/tasks'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def start_tasks(self, token: str, query: str, task_id: str):
        url = f'https://api.pitchtalk.app/v1/api/tasks/{task_id}/start'
        data = {}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            return {}

    def verify_tasks(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/tasks/verify'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return []
        
    def upgrade_level(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/users/upgrade'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return response.json()
        
    def upgrade_speed(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/users/upgrade-speed'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return response.json()
        
    def upgrade_capacity(self, token: str, query: str):
        url = 'https://api.pitchtalk.app/v1/api/users/upgrade-capacity'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'X-Telegram-Hash': query
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            return response.json()
        else:
            return response.json()
        
    def question(self):
        while True:
            upgrade_level = input("Upgrade User Level? [y/n] -> ").strip().lower()
            if upgrade_level in ["y", "n"]:
                upgrade_level = upgrade_level == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to upgrade or 'n' to skip.{Style.RESET_ALL}")

        while True:
            upgrade_speed = input("Upgrade Speed Booster Level? [y/n] -> ").strip().lower()
            if upgrade_speed in ["y", "n"]:
                upgrade_speed = upgrade_speed == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to upgrade or 'n' to skip.{Style.RESET_ALL}")

        speed_count = 0
        if upgrade_speed:
            while True:
                try:
                    speed_count = int(input("How many times? -> "))
                    if speed_count > 0:
                        break
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")
        
        while True:
            upgrade_capacity = input("Upgrade Time Booster Level? [y/n] -> ").strip().lower()
            if upgrade_capacity in ["y", "n"]:
                upgrade_capacity = upgrade_capacity == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to upgrade or 'n' to skip.{Style.RESET_ALL}")

        capacity_count = 0
        if upgrade_capacity:
            while True:
                try:
                    capacity_count = int(input("How many times? -> "))
                    if capacity_count > 0:
                        break
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        return upgrade_level, upgrade_speed, speed_count, upgrade_capacity, capacity_count
        
    def process_query(self, query, upgrade_level: bool, upgrade_speed: bool, speed_count: int, upgrade_capacity: bool, capacity_count: int):

        user_id, username = self.load_data(query)

        account = self.auth(query, user_id, username)
        token = account['accessToken']

        if not token:
            self.log(
                f"{Fore.RED + Style.BRIGHT}[ Token Not Found:{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} Account {username} {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
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
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Level{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['level']} {Style.RESET_ALL}"
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
                claim = self.claim_refferal(token, query)
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

            farm = self.farmings(token, query)

            if not farm:
                create = self.create_farming(token, query)
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

                farm = self.farmings(token, query)
            time.sleep(1)

            if farm:
                end_farm = farm['endTime']
                end_farm_utc = datetime.strptime(end_farm, '%Y-%m-%dT%H:%M:%S.%fZ')
                end_farm_wib = pytz.utc.localize(end_farm_utc).astimezone(wib).strftime('%x %X %Z')

                claim = self.claim_farming(token, query)
                if claim:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance Now{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {claim['coins']} Points {Style.RESET_ALL}"
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

            tasks = self.tasks(token, query)
            if tasks:
                for task in tasks:
                    task_id = task['id']
                    title = task['template']['title']
                    reward_coin = task['template']['rewardCoins']
                    reward_ticket = task['template']['rewardTickets']

                    if task and task.get('completedAt') is None:
                        start = self.start_tasks(token, query, task_id)
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

                        verified = self.verify_tasks(token, query)

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
            time.sleep(1)

            if upgrade_level:
                upgrade = self.upgrade_level(token, query)
                if isinstance(upgrade, dict) and 'message' in upgrade:
                    error_message = upgrade['message']
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade User{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Level {user['level']+1} {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}Isn't Success{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reason{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {error_message} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade User{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Level {user['level']+1} {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}Is Success{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade User{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Level {user['level']+1} {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Skipped{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
            time.sleep(1)


            speed_level = user['speedBoostLevel']
            if upgrade_speed:
                for i in range(speed_count):
                    upgrade = self.upgrade_speed(token, query)
                    if isinstance(upgrade, dict) and 'message' in upgrade:
                        error_message = upgrade['message']
                        if "BadRequestException:" in error_message:
                            error_message = error_message.split("BadRequestException:")[1].strip()

                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade Speed{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} Level {speed_level+1} {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}Isn't Success{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [ Reason{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {error_message} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )   
                        break

                    else:
                        speed_level = upgrade.get('speedBoostLevel', speed_level)
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade Speed{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} Level {speed_level} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Success{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                    time.sleep(1)
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade Speed{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Level {speed_level+1} {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Skipped{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
            time.sleep(1)


            capacity_level = user['timeBoostLevel']
            if upgrade_capacity:
                for i in range(capacity_count):
                    upgrade = self.upgrade_capacity(token, query)
                    if isinstance(upgrade, dict) and 'message' in upgrade:
                        error_message = upgrade['message']
                        if "BadRequestException:" in error_message:
                            error_message = error_message.split("BadRequestException:")[1].strip()

                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade Time{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} Level {capacity_level+1} {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}Isn't Success{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [ Reason{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {error_message} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )   
                        break

                    else:
                        capacity_level = upgrade.get('timeBoostLevel', capacity_level)
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade Time{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} Level {capacity_level} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Success{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                    time.sleep(1)
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Upgrade Time{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} Level {capacity_level+1} {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Skipped{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                )
            time.sleep(1)
       
    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            upgrade_level, upgrade_speed, speed_count, upgrade_capacity, capacity_count = self.question()

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
                        self.process_query(query, upgrade_level, upgrade_speed, speed_count, upgrade_capacity, capacity_count)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        time.sleep(3)

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