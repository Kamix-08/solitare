# pasjans

_Projekt wykonany przez Kamila Pawłowskiego w ramach konkursu Gigathon 2025 w języku Python._

## uruchomienie

Aby uruchomić grę, należy wykonać następujące kroki (z katalogu projektu):

1. Pobierz zależności projektu:

```bash
pip install -r requirements.txt
```

2. Uruchom grę:

```bash
python main.py
```

> [!NOTE] 
> Wymaga zainstalowanego i skonfigurowanego Pythona.
> Zalecana wersja to 3.12.x

3. _(opcjonalne)_ Sprawdź poprawność typów:

```bash
mypy .
```

## instrukcje

System sterowania jest intuicyjny - używaj klawiszy strzałek do poruszania się oraz klawisza Enter do zatwierdzania wyboru.

W trakcie gry klawisz Esc pozwala anulować zaznaczenie lub wyjść z gry.

W menu wskaźnik zaznaczenia jest zielony, w scenie gry - niebieski. Zaznaczone elementy mają kolor fioletowy.

Aby przenieść kartę, zaznacz ją, a następnie wybierz miejsce docelowe.

Aby dobrać karty ze stosu zapasowego, zaznacz ten stos.

## dodatkowe informacje

Dokumentacja techniczna, w postaci opisu klas, metod i funkcji każdego pliku, znajduje się w osobnym dokumencie: [technical.md](./technical.md).