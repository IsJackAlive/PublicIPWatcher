# PublicIPWatcher
PublicIPWatcher to aplikacja stworzona w języku Python, która umożliwia monitorowanie i śledzenie zmian publicznego adresu IP. Aktualny adres zapisuje w pliku, korzystając z szyfrowania GnuPG oraz repozytorium Git.

>Do poprawnego działania aplikacji wymagany jest **klucz publiczny klienta**. Upewnij się, że klucz `recipent_keyid` został poprawnie skonfigurowany w odpowiednim miejscu w kodzie.

## Funkcje
- [x] Sprawdzenie adresu IP
- [x] Haszowanie z wykorzystaniem seeda
- [x] Szyfrowanie GPG
- [x] Interakcja z systemem Git
- [x] Zapisywanie błędów

### ToDo:
- [ ] Wersja klienta

### Działanie
1. Aplikacja pobiera publiczny adres IP.
1. Oblicza hash dla pobranego adresu IP z wykorzystaniem seeda.
1. Sprawdza, czy adres IP uległ zmianie porównując fragment hash z ostatniego commita.
1. Jeśli adres IP uległ zmianie:
    - Szyfruje nowy adres IP za pomocą klucza publicznego klienta.
    - Zapisuje zaszyfrowany adres IP w pliku hello.txt.
    - Wysyła zmiany do repozytorium Git.
1. W przypadku wystąpienia błędu zapisuje wyjątki do pliku log.txt i zamyka program.

### Pliki
- hello.txt: Plik przechowujący zaszyfrowany adres IP.
- log.txt: Plik z zapisanymi wyjątkami.
- main.py: Główny plik programu.

#### Biblioteki
[python-gnupg](https://gnupg.readthedocs.io/en/latest/)

[hashlib](https://docs.python.org/3/library/hashlib.html)

[public-ip](https://github.com/vterron/public-ip)
