import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
from sys import exit
from configparser import ConfigParser
from progress.bar import Bar
from time import sleep
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from string import digits, ascii_letters
from datetime import datetime

config = ConfigParser()
config.read('config.ini')
profile_numbers = int(config['Settings']['account_numbers'])
threads_number = int(config['Settings']['threads'])

API_URl = 'http://localhost:50325/'


def worker(index):
    try:
        args = {
            'user_id': profile_ids[index],
            'ip_tab': 0
        }
        try:
            r = requests.get(API_URl + 'api/v1/browser/start', params=args).json()
        except Exception as e:
            print(f'\nНе удалось запустить профиль {index}: ' + str(e))
            return
        else:
            if r['code'] != 0:
                print(f'\nНе удалось запустить профиль {index}: ' + r['msg'])
                return
            else:
                ws = r["data"]["ws"]["selenium"]
                driver_path = r["data"]["webdriver"]

        options = Options()
        options.add_experimental_option("debuggerAddress", ws)
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()

        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="critical-error"]')))
        except:
            pass
        else:
            driver.refresh()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-import-wallet"]'))).click()
        WebDriverWait(driver, 1)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="metametrics-i-agree"]'))).click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'import-srp__srp-word-0')))

        seed = credentials[index].split()
        for j in range(12):
            driver.find_element(By.ID, f'import-srp__srp-word-{j}').send_keys(seed[j])

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="import-srp-confirm"]'))).click()

        meta_password = config['Settings']['meta_password']

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-new"]'))).send_keys(
            meta_password)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(((By.XPATH, '//input[@data-testid="create-password-confirm"]')))).send_keys(
            meta_password)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-password-import"]'))).click()

        driver.implicitly_wait(5)

        while 1:
            try:
                driver.find_element(By.XPATH, '//div[@class="loading-overlay"]')
            except:
                break
            else:
                sleep(1)
                continue

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-complete-done"]'))).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-next"]'))).click()
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-done"]'))).click()

        # ====

        driver.get('https://www.mobox.io/dragonmo/')

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[3]/span'))).click()
        sleep(random.randint(8, 19) / 10)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/button'))).click()
        sleep(random.randint(8, 19) / 10)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/ul/li[4]'))).click()

        sleep(1)
        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
        main_window = driver.current_window_handle
        handles = driver.window_handles
        handles.remove(main_window)
        driver.switch_to.window(handles[0])

        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]'))).click()
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]'))).click()

        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))
        driver.switch_to.window(main_window)

        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/button'))).click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[3]/div[2]/input'))).send_keys(email[index])
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/button'))).click()

        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
        main_window = driver.current_window_handle
        handles = driver.window_handles
        handles.remove(main_window)
        driver.switch_to.window(handles[0])

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[4]/footer/button[2]'))).click()

        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))
        driver.switch_to.window(main_window)

        sleep(4)
    except Exception as e:
        print(f'Произошла ошибка в профиле {index}: {str(e)}')
    else:
        print(f'Профиль {index} закончил работу')
        with open('done.txt', 'a', encoding='utf-8') as file:
            file.write(f'{credentials[index]}\n'
                       f'{email[index]}\n'
                       f'{proxy[index] if proxy else "NO PROXY"}\n\n')
            file.close()
    finally:
        driver.close()
        global active_profiles
        active_profiles -= 1
        return


def init_exit():
    input("\nНажмите Enter, чтобы выйти")
    exit()


def bypass():
    try:
        open('C:\.ADSPOWER_GLOBAL\extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js')
    except:
        try:
            open('D:\.ADSPOWER_GLOBAL\extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js')
        except:
            return False
        else:
            path = 'D:\.ADSPOWER_GLOBAL\\'
    else:
        path = 'C:\.ADSPOWER_GLOBAL\\'

    with open(path + 'extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js', 'r',
              encoding='utf-8') as file:
        text = file.read()
        file.close()

    text = text.replace(
        '} = {"scuttleGlobalThis":true,"scuttleGlobalThisExceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","location","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}',
        '} = {"scuttleGlobalThis":false,"scuttleGlobalThisExceptions":[]}')

    try:
        with open(path + 'ext\\19657\\runtime-lavamoat.js', 'w', encoding='utf-8') as file:
            file.write(text)
            file.close()
        with open(path + 'extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js', 'w',
                  encoding='utf-8') as file:
            file.write(text)
            file.close()
    except FileNotFoundError:
        try:
            with open(path + 'extension\\19657\\3f78540a9170bc1d87c525f061d1dd0f\\10.26.2_0\\runtime-lavamoat.js', 'w',
                      encoding='utf-8') as file:
                file.write(text)
                file.close()
        except FileNotFoundError:
            return False

    return True


if __name__ == '__main__':
    print('Проверка перед запуском...\n')

    try:
        status = requests.get(API_URl + 'status').json()
    except Exception:
        print('API недоступен. Проверьте, запущен ли AdsPower.')
        init_exit()

    if not bypass():
        print('Ошибка MetaMask. Проверьте, установлено ли расширение в AdsPower.')
        init_exit()

    credentials = []
    try:
        file = open(config["Settings"]["credentials_file"], encoding='utf-8')
    except FileNotFoundError:
        print(f'Файл {config["Settings"]["credentials_file"]} не найден')
        init_exit()
    else:
        credentials = file.read().split('\n')

    email = []
    try:
        file = open(config["Settings"]["email_file"], encoding='utf-8')
    except FileNotFoundError:
        print(f'Файл {config["Settings"]["email_file"]} не найден')
        init_exit()
    else:
        email = file.read().split('\n')

    proxy = []
    try:
        proxy = open(config['Settings']['proxy_file'], encoding='utf-8')
        proxy = proxy.read().split('\n')
    except FileNotFoundError:
        print(f'Файл {config["Settings"]["proxy_file"]} не найден. Прокси не будут использованы.\n')

    if profile_numbers > len(credentials) or profile_numbers > len(email) or proxy and profile_numbers > len(proxy):
        print('В одном из файлов строк меньше, чем указано в настройках.')
        init_exit()

    print('Проверка завершена. Создание профилей AdsPower...\n')

    group_name = f'EggsChingon'
    group_id = 0

    try:
        r = requests.get(API_URl + 'api/v1/group/list').json()
    except Exception as e:
        pass
    else:
        if r['code'] == 0:
            for i in r['data']['list']:
                if i['group_name'] == group_name:
                    group_id = i['group_id']
                    break

    if not group_id:
        try:
            r = requests.post(API_URl + 'api/v1/group/create', json={'group_name': group_name}).json()
        except Exception as e:
            print('Не удалось создать группу профилей AdsPower: ' + str(e))
            init_exit()
        else:
            if r['code'] != 0:
                print('Не удалось создать группу профилей AdsPower: ' + r['msg'])
                init_exit()
            else:
                group_id = r['data']['group_id']

    profile_ids = []
    bar = Bar('Создание профилей', max=profile_numbers)
    for i in range(profile_numbers):
        if proxy:
            host, port, user, password = proxy[i].split(':')
            account_data = {
                'group_id': group_id,
                'user_proxy_config': {
                    'proxy_soft': 'other',
                    'proxy_type': config['Settings']['proxy_type'],
                    'proxy_host': host,
                    'proxy_port': port,
                    'proxy_user': user,
                    'proxy_password': password
                }
            }
        else:
            account_data = {
                'group_id': group_id,
                'user_proxy_config': {
                    'proxy_soft': 'no_proxy'
                }
            }

            try:
                r = requests.post(API_URl + 'api/v1/user/create', json=account_data).json()
            except Exception as e:
                bar.finish()
                print('\nНе удалось создать профиль: ' + str(e))
                init_exit()
            else:
                if r['code'] != 0:
                    bar.finish()
                    print('\nНе удалось создать профиль: ' + r['msg'])
                    init_exit()
                else:
                    profile_ids.append(r['data']['id'])
                    bar.next()

            sleep(1)

    bar.finish()

    print('\nПрофили успешно созданы. Начинаем работу...\n')

    active_profiles = 0
    for i in range(len(profile_ids)):
        while active_profiles + 1 > threads_number:
            continue
        t = Thread(target=worker, args=(i,))
        active_profiles += 1
        t.start()
        sleep(1.5)
