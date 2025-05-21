# System rozpoznawania twarzy na bazie wzorca z wprowadzaniem zdefiniowanych zaburzeń

System rozpoznawania twarzy (ang. _face recognition_) na bazie wczytanego wzorca, z wprowadzaniem zdefiniowanych zaburzeń. 
Aplikacja desktopowa napisana została w języku Python, z wykorzystaniem bibliotek OpenCV oraz FaceX-Zoo. Docelową platformą
dla aplikacji jest system Windows 10/11 lub Ubuntu Linux w wersji 20.04 lub nowszej.

## Wymagania systemowe

* **System operacyjny**: Windows 10/11 lub Ubuntu Linux (20.04 lub nowszy)

* **Python**: wersja 3.7.1 lub nowsza

* **`pip`**: zainstalowany menedżer pakietów

* **Zalecane**:
    * Środowisko wirtualne (`venv`) do zarządzania zależnościami
    * Dostęp do terminala lub konsoli (cmd / PowerShell / bash)

## Instrukcja uruchomienia programu

1. **Pobierz projekt**

    ```bash
    git clone https://github.com/lipa13/FaceRecognitionApp.git
    cd FaceRecognitionApp
    ```

2. **(Zalecane) Utwórz i aktywuj środowisko wirtualne**

    * Dla **Windows**:

      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

    * Dla **Linux/macOS**:

      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```


3. **Zainstaluj zależności**

    ```bash
    pip install -r requirements.txt
    ```

4. **Uruchom aplikację**

    ```bash
    python GUI/main_view.py
    ```  
