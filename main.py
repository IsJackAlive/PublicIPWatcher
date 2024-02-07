import re
import sys
import subprocess
import public_ip as ip
import hashlib
import gnupg
import datetime

seed='anything' # Wygeneruje trudniejszy hash

# Funkcja do sprawdzania ostatniego commita w repozytorium Git
def get_latest_commit():
    try:
        latest_commit = subprocess.check_output(['git', 'log', '-n', '1', '--format=%s']).strip().decode('utf-8')
        return latest_commit
    except Exception as e:
        log_error(e)
        return None

# Sprawdź czy Ip uległo zmianie
def new_adress(hash_ip):
    commit_message = get_latest_commit()
      
    if commit_message:
        if hash_ip == commit_message:
            return False
    return True

# Funkcja do obliczania hashu hasła
def calculate_hash(ip_address):
    mix = ip_address + seed
    hash_object = hashlib.sha256(mix.encode()).hexdigest()
    match = re.search(r'.{10}(.{10})', hash_object) # Wykorzystaj tylko fragment hash
    cut_hash = match.group(1)
    return cut_hash
        
# Funkcja do obsługi zmian w repozytorium Git
def update_git_repository(commit_message):
    try:
        subprocess.run(['git', 'add', 'hello.txt'])
        subprocess.run(['git', 'commit', '-m', commit_message])
        subprocess.run(['git', 'push'])
    except Exception as e:
        log_error(e)

# Szyfrowanie wiadomosci
def save_file(message):
    gpg = gnupg.GPG(gnupghome='/home/user/.gnupg/') # Zmień na swoja scieżke do gpg home
    recipent_keyid = 'keykeykeykey' # Klucz klienta, do odszyfrowania wiadomości (np. '3E8A3E8A3E8A3E8A3E8A3')
    encrypted_message = gpg.encrypt(message, recipients=recipent_keyid)
    if encrypted_message.ok:
        try:
            with open('hello.txt', 'wb') as file:
                file.write(encrypted_message.data)
        except Exception as e:
            log_error(e)
    else:
        log_error(encrypted_message.stderr)

# Zapisywanie wyjatkow
def log_error(exception):
    with open("log.txt", "a") as log_file:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write("[{}] Error occurred:\n".format(current_time))
        log_file.write(str(exception))
        log_file.write(" Stopped.\n")
        sys.exit(1)

def main():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("date:(%Y-%m-%d %H:%M:%S) \t adress:(")

    try:
        current_ip = ip.get()   # Pobierz publiczne ip
    except Exception as e:
            log_error(e)

    hash_ip = calculate_hash(current_ip)    # Oblicz hash dla aktualnego ip
    message = formatted_time + current_ip + ")\n"

    if new_adress(hash_ip):
        save_file(message)
        update_git_repository(hash_ip)        

if __name__ == "__main__":
    main()