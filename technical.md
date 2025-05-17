# Dokumentacja techniczna

- [Dokumentacja techniczna](#dokumentacja-techniczna)
  - [moduł `game`](#moduł-game)
    - [`Card.py`](#cardpy)
      - [`Value`](#value)
      - [`Suit`](#suit)
    - [`GameManager.py`](#gamemanagerpy)
      - [`GameManager`](#gamemanager)
        - [`init_cards`](#init_cards)
        - [`get_next_card`](#get_next_card)
        - [`init_game_piles`](#init_game_piles)
        - [`init_final_piles`](#init_final_piles)
        - [`init_reserve_pile`](#init_reserve_pile)
        - [`init_piles`](#init_piles)
        - [`get_structure`](#get_structure)
        - [`execute`](#execute)
        - [`move_card`](#move_card)
        - [`move_selected`](#move_selected)
        - [`handle_esc`](#handle_esc)
        - [`add_to_history`](#add_to_history)
        - [`back`](#back)
        - [`end`](#end)
        - [`solve`](#solve)
    - [`Pile.py`](#pilepy)
      - [`Pile`](#pile)
        - [`can_stack`](#can_stack)
        - [`can_add_to_empty`](#can_add_to_empty)
        - [`add`](#add)
        - [`find`](#find)
        - [`pop`](#pop)
        - [`on_move`](#on_move)
        - [`_str`](#_str)
        - [`get_last`](#get_last)
      - [`GamePile`](#gamepile)
      - [`FinalPile`](#finalpile)
      - [`ReservePile`](#reservepile)
    - [`scenes.py`](#scenespy)
        - [`start`](#start)
        - [`use_scene`](#use_scene)
        - [`exit_game`](#exit_game)
        - [`scene_main`](#scene_main)
        - [`scene_game_mode`](#scene_game_mode)
        - [`scene_info`](#scene_info)
        - [`scene_end`](#scene_end)
        - [`format_table`](#format_table)
        - [`scene_leaderboard`](#scene_leaderboard)
  - [moduł `ui`](#moduł-ui)
    - [`Colors.py`](#colorspy)
      - [`Colors`](#colors)
        - [`regex`](#regex)
        - [`get_color`](#get_color)
        - [`set_color`](#set_color)
        - [`get_prev_color`](#get_prev_color)
        - [`prev_color`](#prev_color)
        - [`clear`](#clear)
    - [`InputHandler.py`](#inputhandlerpy)
      - [`InputHandler`](#inputhandler)
        - [`call`](#call)
        - [`callback`](#callback)
        - [`add`](#add-1)
        - [`add_list`](#add_list)
        - [`start`](#start-1)
        - [`stop`](#stop)
    - [`Menu.py`](#menupy)
      - [`BaseMenu`](#basemenu)
        - [`change_selection`](#change_selection)
        - [`call`](#call-1)
        - [`submit`](#submit)
        - [`start`](#start-2)
        - [`stop`](#stop-1)
      - [`Menu`](#menu)
      - [`HorizontalMenu`](#horizontalmenu)
        - [`change_secondary_selection`](#change_secondary_selection)
        - [`get_highlight`](#get_highlight)
    - [`Renderer.py`](#rendererpy)
      - [`Renderer`](#renderer)
        - [`init_ascii_font`](#init_ascii_font)
        - [`get_ascii_text`](#get_ascii_text)
        - [`get_clear`](#get_clear)
        - [`clear`](#clear-1)
        - [`format_seconds`](#format_seconds)
      - [`AsciiText`](#asciitext)
      - [`Button`](#button)
        - [`get_buttons`](#get_buttons)
    - [`Scene.py`](#scenepy)
      - [`Scene`](#scene)
        - [`start`](#start-3)
        - [`stop`](#stop-2)
        - [`start_menus`](#start_menus)
        - [`stop_menus`](#stop_menus)

## moduł `game`

### `Card.py`

#### `Value`

Klasa (enum) określająca wartość karty

#### `Suit`

Klasa (enum) określająca kolor karty

### `GameManager.py`

#### `GameManager`

Najbardziej rozbudowana klasa projektu - zarządza całą rozgrywką.

##### `init_cards`

Inicjalizuje talię kart

##### `get_next_card`

Zwraca następną w talii kartę

##### `init_game_piles`

Inicjalizuje stosy do gry, nakładając na nie odpowiednią ilość kart

##### `init_final_piles`

Inicjalizuje stosy końcowe

##### `init_reserve_pile`

Inicjalizuje stosy rezerwowe

##### `init_piles`

Inicjalizuje wszystkie stosy, poprzez wywołanie `init_game_pile`, `init_final_piles` i `init_reserve_piles`

##### `get_structure`

Zwraca strukturę (wymiary) planszy w obecnym momencie, jako `list[int]`. Każdy element listy to wysokość kolejnego stosu

##### `execute`

Najbardziej rozbudowana metoda. Wywołuje odpowiednią akcję (przesunięcie karty, zaznaczenie, dopisanie do historii, itp.), w zależności od zaznaczonego miejsca oraz innych informacji o stanie gry (np. czy jakieś miejsce było już zaznaczone)

##### `move_card`

Przenosi wskazaną kartę pomiędzy wskazanymi stosami

##### `move_selected`

Przenosi zaznaczoną kartę na wskazany stos

##### `handle_esc`

Obsługa klawisza Escape

##### `add_to_history`

Dopisuje obecną sytuację do historii

##### `back`

Cofa do poprzedniej sytuacji

##### `end` 

Zakańcza rozgrywkę

##### `solve`

Auto-uzupełnia, jeśli jest to możliwe

### `Pile.py`

#### `Pile`

Abstrakcyjna klasa stosu

##### `can_stack`

Abstrakcyjna statyczna metoda, określająca, czy można nałożyć kartę `a` na kartę `b`

##### `can_add_to_empty`

Określa, czy można dodać wskazaną kartę do pustego stosu

##### `add`

Dodaje wskazaną kartę do stosu

##### `find`

Zwraca indeks szukanej karty na stosie jeśli istnieje, lub `-1` w przeciwnym razie

##### `pop`

Usuwa i zwraca element o indeksie `i`

##### `on_move`

Metoda wywoływana podczas przesuwania kart między stosami

##### `_str`

Zwraca reprezentację stosu jako `list[str]`

##### `get_last`

Zwraca reprezentację ostatniej karty jako `list[str]`

#### `GamePile`

Klasa stosu gry, dziedzicząca z klasy stosu

Nadpisuje metody `can_stack` i `can_add_to_empty`

#### `FinalPile`

Klasa stosu końcowego, dziedzicząca z klasy stosu

Nadpisuje metody `can_stack`, `can_add_to_empty` i `_str`

#### `ReservePile`

Klasa stosu rezerwowego, dziedzicząca z klasy stosu

Nadpisuje metody `can_stack`, `can_add_to_empty`, `on_move` i `_str`

### `scenes.py`

Plik obsługujący sceny

##### `start`

Funkcja wywoływana na początku rozgrywki. Tworzy instację klasy `GameManager`, obsługuje jej logikę i wywołuje scenę końcową, po zakończeniu rozgrywki

##### `use_scene`

Zmienia obecną scenę na podaną

##### `exit_game`

Zamyka wszytskie sceny

##### `scene_main`

Zwraca obiekt głównej sceny

##### `scene_game_mode`

Zwraca obiekt sceny menu wyboru trudności

##### `scene_info`

Zwraca obiekt sceny z informacjami

##### `scene_end`

Zwraca obiekt sceny końcowej i modyfikuje lokalną tablicę wyników

##### `format_table`

Formatuje podane dane jako tabelkę i zwraca je w postaci `list[str]`

##### `scene_leaderboard`

Zwraca obiekt sceny z tablicą wyników, odczytując je z lokanego pliku

## moduł `ui`

### `Colors.py`

#### `Colors`

Klasa zarządzająca kolorami

##### `regex`

Statyczna metoda, zwracająca regex, matchujący kody ANSI

##### `get_color`

Statyczna metoda, zwracająca ANSI danego koloru (może również dodać go na stos)

##### `set_color`

Statyczna metoda, ustawiająca kolor na podany

##### `get_prev_color`

Statyczna metoda, zwracająca ANSI poprzedniego koloru

##### `prev_color`

Statyczna metoda, ustawiająca kolor na poprzedni

##### `clear`

Statyczna metoda, czyszcząca stos kolorów i wszystkie efekty (zarówno koloru, jak i czcionki)

### `InputHandler.py`

#### `InputHandler`

Klasa służąca do obsługi klawiatury

##### `call`

Statyczna metoda, służąca do wywołania listy callbacków

##### `callback`

Wywołuje callbacki dla danego klawisza

##### `add`

Dodaje callback do klawisza

##### `add_list`

Dodaje listę callbacków do odpowiadających im kluczów

##### `start`

Uruchamia listener

##### `stop`

Zarzymuje listener

### `Menu.py`

#### `BaseMenu`

Klasa bazowa dla menu

##### `change_selection`

Przesówa zaznaczenie

##### `call`

Wywołuje callback i zatrzymuje listener

##### `submit`

Wywołuje `call` dla obecne wybranego elementu

##### `start`

Uruchamia listener

##### `stop`

Zatrzymuje listener

#### `Menu`

Klasa dziedzicząca z klasy menu bazowego

#### `HorizontalMenu`

Klasa dziedzicząca z klasy menu bazowego, używana przy obsłudze sceny z grą

Nadpisuje metodę `change_selection` i `submit`

##### `change_secondary_selection`

Przez swoją strukturę 2D, menu horyzontalne zawiera również możliwość poruszania się góra-dół, która obsługiwana jest przez tą metodę

##### `get_highlight`

Zwraca współrzędne obecnego zaznaczenia

### `Renderer.py`

#### `Renderer`

Klasa obsługująca niektóre aspekty wyświetlania

##### `init_ascii_font`

Inicjalizuje czcionkę do tekstów ASCII, korzystając z pliku `font.txt`

##### `get_ascii_text`

Zwraca tekst, pisany w czcionce ASCII, jako `str`

##### `get_clear`

Zwraca ANSI czyszczący ekran

##### `clear`

Czyści ekran

##### `format_seconds`

Formatuje sekundy do formatu `hh:mm:ss`

#### `AsciiText`

Klasa reprezentująca tekst ASCII

#### `Button`

Klasa, oprawiająca tekst w obramówkę

##### `get_buttons`

Statyczna metoda, zwracająca listę przycisków jednakowej długości, z listy tekstów

### `Scene.py`

#### `Scene`

Klasa sceny

##### `start`

Uruchamia wszystkie menu (wywołuje ich metodę `start`, co z kolei wywołuje metodę `start` listinerów) na scenie

##### `stop`

Zatrzymuje wszystkie menu na scenie

##### `start_menus`

Metoda wywoływana przez `start`

##### `stop_menus`

Metoda wywoływana przez `stop`