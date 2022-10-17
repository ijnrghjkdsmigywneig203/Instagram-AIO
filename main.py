import httpx, random, itertools, ctypes, re, json, os, ssl, datetime, sys, threading, time

__config__     = json.load(open('./config.json'))
__proxies__    = open('data/Proxies.txt', 'r').readlines()
__cookies__    = itertools.cycle(open('data/cookies.txt', 'r').readlines())
__base_headers__ = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-encoding': 'gzip, deflate, br','Accept-language': 'en-US,en;q=0.9','Pragma': 'no-cache','Origin': 'https://www.instagram.com','Referer': 'https://www.instagram.com/','Sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','Sec-ch-ua-mobile': '?0','Sec-ch-ua-platform': '"Windows"','Sec-fetch-dest': 'empty','Sec-fetch-mode': 'cors','Sec-fetch-site': 'same-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
__ciphers__ = 'ECDH+AESGCM:ECDH+CHACHA20:DH+AESGCM:DH+CHACHA20:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:RSA+AESGCM:RSA+AES:RSA+HIGH:!aNULL:!eNULL:!MD5:!3DES'

__SSLcontext__ = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
__SSLcontext__.set_alpn_protocols(["h2"])
__SSLcontext__.set_ciphers(__ciphers__)

class bcolors:
    BLACK  = '\033[30m'
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN   = '\033[36m'
    WHITE  = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET  = '\033[0m'


class Instagram:
    def __init__(self):
        self.set_title()

    def clear(self) -> None:
        os.system('clear') if os.name == 'posix' else os.system('cls')

    def set_title(self) -> None:
        ctypes.windll.kernel32.SetConsoleTitleW(f"Gramify ^| Cookies: {len(open('data/cookies.txt', 'r+').readlines())} ^| Proxies: {len(open('data/proxies.txt', 'r+').readlines())}") if os.name == 'nt' else ctypes.windll.kernel32.SetConsoleTitleW(f"Gramify ^| Cookies: {len(open('data/cookies.txt', 'r+').readlines())} ^| Proxies: {len(open('data/proxies.txt', 'r+').readlines())}")

    def __getID__(self, username: str) -> str:
        client = httpx.Client(http2=True, headers=__base_headers__, proxies=f'http://{random.choice(__proxies__)}',timeout=30, verify=__SSLcontext__) if __config__["proxyless"] !=True else httpx.Client(http2=True, headers=__base_headers__, timeout=30, verify=__SSLcontext__)
        try:
            __lib_hash__ = re.findall(r"(?<=ConsumerLibCommons\.js\/)[a-z0-9]{12}", client.get("https://www.instagram.com/", headers=__base_headers__).text,)[0]
            Lib = client.get(f"https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/{__lib_hash__}.js", headers=__base_headers__,).text
            client.headers['x-ig-app-id'] = re.findall(r"AppId='(\d+)'", Lib)[0]
            client.headers['x-asbd-id'] = re.findall(r"ASBD_ID='(\d+)'", Lib)[0]
            _ex_data_ = client.get("https://www.instagram.com").text
            client.headers["x-csrftoken"] = re.findall(r'(?<="csrf_token":")[a-zA-Z0-9]{31,32}', _ex_data_)[0]
            client.headers["X-Instagram-Ajax"] = re.findall(r'(?<="rollout_hash":")[a-z0-9]{11,12}', _ex_data_)[0]
        except Exception as e:
               print(f'Error Setting up Session | Line:  | Function: __getID__ | err: {e}')
               client.headers["x-csrftoken"] = 'Jy0Bodoxg2o76T8otYFtcFZOACFedCfA'
               client.headers["X-Instagram-Ajax"] = '1006400684'
               client.headers['x-ig-app-id'] = '936619743392459'
               client.headers['x-asbd-id'] = '198387'
               pass
        try:
            client.headers["user-agent"] = "Instagram 219.0.0.12.117 Android"
            u=client.get(f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}')
            return u.json()["data"]["user"]["id"]
        except Exception as e:
            return False
    

    def __postID__(self, id: str) -> int:
        client = httpx.Client(http2=True, headers=__base_headers__, proxies=f'http://{random.choice(__proxies__)}',timeout=30, verify=__SSLcontext__) if __config__["proxyless"] !=True else httpx.Client(http2=True, headers=__base_headers__, timeout=30, verify=__SSLcontext__)
        try:
            p=client.get(f'https://www.instagram.com/p/{id}/', cookies=client.cookies).text
            return p.split('postPage_')[1].split('"')[0]
        except:
            return False


    def __likePost__(self, nonfmtid: str, id: str) -> None:
        client = httpx.Client(http2=True, headers=__base_headers__, proxies=f'http://{random.choice(__proxies__)}',timeout=30, verify=__SSLcontext__) if __config__["proxyless"] !=True else httpx.Client(http2=True, headers=__base_headers__, timeout=30, verify=__SSLcontext__)
        try:
            __lib_hash__ = re.findall(r"(?<=ConsumerLibCommons\.js\/)[a-z0-9]{12}", client.get("https://www.instagram.com/", headers=__base_headers__).text,)[0]
            Lib = client.get(f"https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/{__lib_hash__}.js", headers=__base_headers__,).text
            client.headers['x-ig-app-id'] = re.findall(r"AppId='(\d+)'", Lib)[0]
            client.headers['x-asbd-id'] = re.findall(r"ASBD_ID='(\d+)'", Lib)[0]
            _ex_data_ = client.get("https://www.instagram.com").text
            client.headers["x-csrftoken"] = re.findall(r'(?<="csrf_token":")[a-zA-Z0-9]{31,32}', _ex_data_)[0]
            client.headers["X-Instagram-Ajax"] = re.findall(r'(?<="rollout_hash":")[a-z0-9]{11,12}', _ex_data_)[0]
        except Exception as e:
               print(f'Error Setting up Session | Line:  | Function: __likePost__ | err: {e}')
               client.headers["x-csrftoken"] = 'Jy0Bodoxg2o76T8otYFtcFZOACFedCfA'
               client.headers["X-Instagram-Ajax"] = '1006400684'
               client.headers['x-ig-app-id'] = '936619743392459'
               client.headers['x-asbd-id'] = '198387'
        try:
            Cookie = next(__cookies__)
            client.headers["referer"] = f"https://www.instagram.com/p/{nonfmtid}/"
            client.headers["cookie"] = f"sessionid={Cookie}"
            l=client.post(f'https://i.instagram.com/api/v1/web/likes/{id}/like/',)
            if l.status_code in [204, 200] and l.json()["status"]=='ok':
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {bcolors.GREEN}Liked Post: www.instagram.com/p/{nonfmtid}{bcolors.RESET}")
            else:
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {bcolors.RED}Failed To Like Post: www.instagram.com/p/{nonfmtid}{bcolors.RESET}")
        except:
            pass
    

    def __unlikePost__(self, nonfmtid: str, id: str) -> None:
        client = httpx.Client(http2=True, headers=__base_headers__, proxies=f'http://{random.choice(__proxies__)}',timeout=30, verify=__SSLcontext__) if __config__["proxyless"] !=True else httpx.Client(http2=True, headers=__base_headers__, timeout=30, verify=__SSLcontext__)
        try:
            __lib_hash__ = re.findall(r"(?<=ConsumerLibCommons\.js\/)[a-z0-9]{12}", client.get("https://www.instagram.com/", headers=__base_headers__).text,)[0]
            Lib = client.get(f"https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/{__lib_hash__}.js", headers=__base_headers__,).text
            client.headers['x-ig-app-id'] = re.findall(r"AppId='(\d+)'", Lib)[0]
            client.headers['x-asbd-id'] = re.findall(r"ASBD_ID='(\d+)'", Lib)[0]
            _ex_data_ = client.get("https://www.instagram.com").text
            client.headers["x-csrftoken"] = re.findall(r'(?<="csrf_token":")[a-zA-Z0-9]{31,32}', _ex_data_)[0]
            client.headers["X-Instagram-Ajax"] = re.findall(r'(?<="rollout_hash":")[a-z0-9]{11,12}', _ex_data_)[0]
        except Exception as e:
               print(f'Error Setting up Session | Line:  | Function: __unlikePost__ | err: {e}')
               client.headers["x-csrftoken"] = 'Jy0Bodoxg2o76T8otYFtcFZOACFedCfA'
               client.headers["X-Instagram-Ajax"] = '1006400684'
               client.headers['x-ig-app-id'] = '936619743392459'
               client.headers['x-asbd-id'] = '198387'
        try:
            Cookie = next(__cookies__)
            client.headers["referer"] = f"https://www.instagram.com/p/{nonfmtid}/"
            client.headers["cookie"] = f"sessionid={Cookie}"
            u=client.post(f'https://i.instagram.com/api/v1/web/likes/{id}/unlike/',)
            if u.status_code in [204, 200] and u.json()["status"]=='ok':
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {bcolors.GREEN}Unliked Post: www.instagram.com/p/{nonfmtid}{bcolors.RESET}")
            else:
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {bcolors.RED}Failed To Unlike Post: www.instagram.com/p/{nonfmtid}{bcolors.RESET}")
        except:
            pass
    

    def __followAccount__(self, nonfmtusr: str, id: str) -> None:
        client = httpx.Client(http2=True, headers=__base_headers__, proxies=f'http://{random.choice(__proxies__)}',timeout=30, verify=__SSLcontext__) if __config__["proxyless"] !=True else httpx.Client(http2=True, headers=__base_headers__, timeout=30, verify=__SSLcontext__)
        try:
            __lib_hash__ = re.findall(r"(?<=ConsumerLibCommons\.js\/)[a-z0-9]{12}", client.get("https://www.instagram.com/", headers=__base_headers__).text,)[0]
            Lib = client.get(f"https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/{__lib_hash__}.js", headers=__base_headers__,).text
            client.headers['x-ig-app-id'] = re.findall(r"AppId='(\d+)'", Lib)[0]
            client.headers['x-asbd-id'] = re.findall(r"ASBD_ID='(\d+)'", Lib)[0]
            _ex_data_ = client.get("https://www.instagram.com").text
            client.headers["x-csrftoken"] = re.findall(r'(?<="csrf_token":")[a-zA-Z0-9]{31,32}', _ex_data_)[0]
            client.headers["X-Instagram-Ajax"] = re.findall(r'(?<="rollout_hash":")[a-z0-9]{11,12}', _ex_data_)[0]
        except Exception as e:
               print(f'Error Setting up Session | Line:  | Function: __followAccount__ | err: {e}')
               client.headers["x-csrftoken"] = 'Jy0Bodoxg2o76T8otYFtcFZOACFedCfA'
               client.headers["X-Instagram-Ajax"] = '1006400684'
               client.headers['x-ig-app-id'] = '936619743392459'
               client.headers['x-asbd-id'] = '198387'
        try:
            Cookie = next(__cookies__)
            client.headers["referer"] = f"https://www.instagram.com/violets.tv/"
            client.headers["cookie"] = f"sessionid={Cookie}"
            f=client.post(f'https://i.instagram.com/api/v1/web/friendships/{id}/follow/',)
            if f.status_code in [204, 200] and f.json()["result"]=='following':
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {bcolors.GREEN}Followed User: www.instagram.com/{nonfmtusr}{bcolors.RESET}")
            else:
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {bcolors.RED}Failed to Follow User: www.instagram.com/{nonfmtusr}{bcolors.RESET}")
        except:
            pass
    

    def __unfollowAccount__(self, nonfmtusr, id: str) -> None:
        client = httpx.Client(http2=True, headers=__base_headers__, proxies=f'http://{random.choice(__proxies__)}',timeout=30, verify=__SSLcontext__) if __config__["proxyless"] !=True else httpx.Client(http2=True, headers=__base_headers__, timeout=30, verify=__SSLcontext__)
        try:
            __lib_hash__ = re.findall(r"(?<=ConsumerLibCommons\.js\/)[a-z0-9]{12}", client.get("https://www.instagram.com/", headers=__base_headers__).text,)[0]
            Lib = client.get(f"https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/{__lib_hash__}.js", headers=__base_headers__,).text
            client.headers['x-ig-app-id'] = re.findall(r"AppId='(\d+)'", Lib)[0]
            client.headers['x-asbd-id'] = re.findall(r"ASBD_ID='(\d+)'", Lib)[0]
            _ex_data_ = client.get("https://www.instagram.com").text
            client.headers["x-csrftoken"] = re.findall(r'(?<="csrf_token":")[a-zA-Z0-9]{31,32}', _ex_data_)[0]
            client.headers["X-Instagram-Ajax"] = re.findall(r'(?<="rollout_hash":")[a-z0-9]{11,12}', _ex_data_)[0]
        except Exception as e:
               print(f'Error Setting up Session | Line:  | Function: __unfollowAccount__ | err: {e}')
               client.headers["x-csrftoken"] = 'Jy0Bodoxg2o76T8otYFtcFZOACFedCfA'
               client.headers["X-Instagram-Ajax"] = '1006400684'
               client.headers['x-ig-app-id'] = '936619743392459'
               client.headers['x-asbd-id'] = '198387'
        try:
            Cookie = next(__cookies__)
            client.headers["referer"] = f"https://www.instagram.com/violets.tv/"
            client.headers["cookie"] = f"sessionid={Cookie}"
            f=client.post(f'https://i.instagram.com/api/v1/web/friendships/{id}/unfollow/')
            if f.status_code in [204, 200] and f.json()["status"]=='ok':
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {bcolors.GREEN}Unfollowed User: www.instagram.com/{nonfmtusr}{bcolors.RESET}")
            else:
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {bcolors.RED}Failed to Unfollow User: www.instagram.com/{nonfmtusr}{bcolors.RESET}")
        except Exception as e:
            print(e)


    def __commentPost__(self, nonfmtpst: str, message: str, id: str) -> None:
        client = httpx.Client(http2=True, headers=__base_headers__, proxies=f'http://{random.choice(__proxies__)}',timeout=30, verify=__SSLcontext__) if __config__["proxyless"] !=True else httpx.Client(http2=True, headers=__base_headers__, timeout=30, verify=__SSLcontext__)
        try:
            __lib_hash__ = re.findall(r"(?<=ConsumerLibCommons\.js\/)[a-z0-9]{12}", client.get("https://www.instagram.com/", headers=__base_headers__).text,)[0]
            Lib = client.get(f"https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/{__lib_hash__}.js", headers=__base_headers__,).text
            client.headers['x-ig-app-id'] = re.findall(r"AppId='(\d+)'", Lib)[0]
            client.headers['x-asbd-id'] = re.findall(r"ASBD_ID='(\d+)'", Lib)[0]
            _ex_data_ = client.get("https://"+"www.instagram.com").text
            client.headers["x-csrftoken"] = re.findall(r'(?<="csrf_token":")[a-zA-Z0-9]{31,32}', _ex_data_)[0]
            client.headers["X-Instagram-Ajax"] = re.findall(r'(?<="rollout_hash":")[a-z0-9]{11,12}', _ex_data_)[0]
        except Exception as e:
               print(f'Error Setting up Session | Line:  | Function: __commentPost__ | err: {e}')
               client.headers["x-csrftoken"] = 'Jy0Bodoxg2o76T8otYFtcFZOACFedCfA'
               client.headers["X-Instagram-Ajax"] = '1006400684'
               client.headers['x-ig-app-id'] = '936619743392459'
               client.headers['x-asbd-id'] = '198387'
        try:
            Cookie = next(__cookies__)
            client.headers["cookie"] = f"sessionid={Cookie}"
            c=client.post(f'https://i.instagram.com/api/v1/web/comments/{id}/add/', data={'comment_text': message})
            if c.status_code in [204, 200] and c.json()["status"]=='ok':
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {message} | {bcolors.GREEN}Commented On Post: www.instagram.com/p/{nonfmtpst}{bcolors.RESET}")
            else:
                print(f"     {bcolors.CYAN}[{datetime.datetime.now().strftime('%H:%M:%S')}]{bcolors.RESET} {bcolors.BLUE}({Cookie[:25]}){bcolors.RESET} | {message} | {bcolors.RED}Failed to Comment on Post: www.instagram.com/{nonfmtpst}{bcolors.RESET}")
        except:
            pass
    

    def main(self) -> None:
        self.clear()
        self.set_title()
        print(f"""

                                            {bcolors.CYAN}╔═╗┬─┐┌─┐┌┬┐┬┌─┐┬ ┬{bcolors.RESET}
                                            {bcolors.CYAN}║ ╦├┬┘├─┤││││├┤ └┬┘{bcolors.RESET}
                                            {bcolors.CYAN}╚═╝┴└─┴ ┴┴ ┴┴└   ┴{bcolors.RESET}
                """)
        print(f"            {bcolors.RED}[{bcolors.RESET}{bcolors.CYAN}1{bcolors.RESET}{bcolors.RED}]{bcolors.RESET} {bcolors.CYAN}Follow User{bcolors.RESET}")
        print(f"            {bcolors.RED}[{bcolors.RESET}{bcolors.CYAN}2{bcolors.RESET}{bcolors.RED}]{bcolors.RESET} {bcolors.CYAN}Unfollow User{bcolors.RESET}")
        print(f"            {bcolors.RED}[{bcolors.RESET}{bcolors.CYAN}3{bcolors.RESET}{bcolors.RED}]{bcolors.RESET} {bcolors.CYAN}Like Post{bcolors.RESET}")
        print(f"            {bcolors.RED}[{bcolors.RESET}{bcolors.CYAN}4{bcolors.RESET}{bcolors.RED}]{bcolors.RESET} {bcolors.CYAN}Unlike Post{bcolors.RESET}")
        print(f"            {bcolors.RED}[{bcolors.RESET}{bcolors.CYAN}5{bcolors.RESET}{bcolors.RED}]{bcolors.RESET} {bcolors.CYAN}Comment on Post{bcolors.RESET}")
        print('')
        print('')
        choice=int(input(f"     {bcolors.GREEN}[{bcolors.RESET} {bcolors.CYAN}?{bcolors.RESET}{bcolors.GREEN} ]{bcolors.RESET} {bcolors.RED}>{bcolors.RESET} "))
        
        if choice == 1:
            username=str(input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Username {bcolors.RED}> {bcolors.RESET}"))
            usrid = self.__getID__(username)
            if usrid == False:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Invalid Username {bcolors.RED}>{bcolors.RESET} ")
                self.main()
            else:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Following {username} with {len(open('data/cookies.txt', 'r').readlines())} Cookies{bcolors.RED} ")
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Press Enter To Begin {bcolors.RED}>{bcolors.RESET} ")
                self.clear()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x = threading.Thread(target=self.__followAccount__, args=(username, usrid,))
                    x.start()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x.join()
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Completed! Press Enter To Return To Menu {bcolors.RED}>{bcolors.RESET} ")
                self.main()
                
        elif choice == 2:
            username=str(input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Username {bcolors.RED}> {bcolors.RESET}"))
            usrid = self.__getID__(username)
            if usrid == False:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Invalid Username {bcolors.RED}>{bcolors.RESET} ")
                time.sleep(5)
                self.main()
            else:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Unfollowing {username} with {len(open('data/cookies.txt', 'r').readlines())} Cookies{bcolors.RED} ")
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Press Enter To Begin {bcolors.RED}>{bcolors.RESET} ")
                self.clear()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x = threading.Thread(target=self.__unfollowAccount__, args=(username, usrid,))
                    x.start()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x.join()
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Completed! Press Enter To Return To Menu {bcolors.RED}>{bcolors.RESET} ")
                self.main()
        
        elif choice == 3:
            id=input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Link of Post {bcolors.RED}> {bcolors.RESET}").split("/p/")[1].split("/")[0]
            pstid = self.__postID__(id)
            if pstid == False:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Post Does not Exist {bcolors.RED}>{bcolors.RESET} ")
                time.sleep(5)
                self.main()
            else:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Liking Post www.instagram.com/p/{id} with {len(open('data/cookies.txt', 'r').readlines())} Cookies{bcolors.RED} ")
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Press Enter To Begin {bcolors.RED}>{bcolors.RESET} ")
                self.clear()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x = threading.Thread(target=self.__likePost__, args=(id, pstid,))
                    x.start()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x.join()
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Completed! Press Enter To Return To Menu {bcolors.RED}>{bcolors.RESET} ")
                self.main()
        
        elif choice == 4:
            id=input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Link of Post {bcolors.RED}> {bcolors.RESET}").split("/p/")[1].split("/")[0]
            pstid = self.__postID__(id)
            if pstid == False:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Post Does not Exist {bcolors.RED}>{bcolors.RESET} ")
                time.sleep(5)
                self.main()
            else:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Uniking Post www.instagram.com/p/{id} with {len(open('data/cookies.txt', 'r').readlines())} Cookies{bcolors.RED} ")
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Press Enter To Begin {bcolors.RED}>{bcolors.RESET} ")
                self.clear()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x = threading.Thread(target=self.__unlikePost__, args=(id, pstid,))
                    x.start()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x.join()
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Completed! Press Enter To Return To Menu {bcolors.RED}>{bcolors.RESET} ")
                self.main()
        
        elif choice == 5:
            id=input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Link of Post {bcolors.RED}> {bcolors.RESET}").split("/p/")[1].split("/")[0]
            msg=input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Message to Comment With {bcolors.RED}> {bcolors.RESET}")
            pstid = self.__postID__(id)
            if pstid == False:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Post Does not Exist {bcolors.RED}>{bcolors.RESET} ")
                time.sleep(5)
                self.main()
            else:
                print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Commenting on Post www.instagram.com/p/{id} with {len(open('data/cookies.txt', 'r').readlines())} Cookies{bcolors.RED} ")
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Press Enter To Begin {bcolors.RED}>{bcolors.RESET} ")
                self.clear()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x = threading.Thread(target=self.__commentPost__, args=(id, msg, pstid,))
                    x.start()
                for i in range(len(open('data/cookies.txt', 'r').readlines())):
                    x.join()
                input(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} Completed! Press Enter To Return To Menu {bcolors.RED}>{bcolors.RESET} ")
                self.main()
        
        else:
            print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} {bcolors.RED}Invalid Option {bcolors.RED}{bcolors.RESET} ")
            time.sleep(2)
            print(f"     {bcolors.GREEN}[{bcolors.RESET}{bcolors.CYAN}Gramify{bcolors.RESET}{bcolors.GREEN}]{bcolors.RESET} {bcolors.RED}Returning to Main Menu... {bcolors.RED}{bcolors.RESET} ")
            time.sleep(3)
            self.main()

            

if __name__ == "__main__":
    try:
        Instagram().main()
    except KeyboardInterrupt:
        sys.exit(0)

    

    

    







    
    

    

