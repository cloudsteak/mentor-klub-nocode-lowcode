# Azure IoT Central

Az Azure IoT Central egy felhőalapú IoT (Internet of Things) alkalmazás, amely lehetővé teszi az IoT eszközök egyszerű és biztonságos kezelését. Az IoT Central segítségével könnyedén létrehozhatók IoT megoldások, amelyek lehetővé teszik az adatok gyűjtését, elemzését és vizualizálását.

## Példa

Ebben a példában szemléltetjük az okos otthoni szenzoradatok megjelenítését Azure IoT Central-ban. Az IoT eszközön futó alkalmazás adatokat gyűjt a szenzoroktól, és ezeket az adatokat az IoT Central segítségével valós időben megjeleníti.

Egy egyszerű Python „eszköz” folyamatosan, valószerűen változó hőmérsékletadatot küld (drift + zaj), amit IoT Centralban valós időben megjelenítünk grafikonon.

## Tárfiók létrehozása

1. Jelentkezz be az Azure Portalba.
2. Kattints az "Új erőforrás" gombra.
3. Majd keresd meg az "Tárfiók" szolgáltatást.
4. Add meg a tárfiók nevét, válaszd ki a régiót és a teljesítmény szintet (Standard vagy Premium).
5. Fontos: Hierarchical namespace: Enabled ajánlott
6. Kattints a "Létrehozás" gombra.
7. Várd meg, amíg a tárfiók létrejön, majd navigálj a tárfiókhoz.
8. Hozz létre egy új tárolót a tárfiókban, ahol majd az IoT eszközök által küldött adatokat tárolod.

## IoT Central

### IoT Central alkalmazás létrehozása

1. Lépj be az [Azure Portal](https://portal.azure.com/) felületére.
2. Kattints az "Create a resource" gombra.
3. Keresd meg az "IoT Central application" lehetőséget, és válaszd ki.
4. Kattints a "Create" gombra.
5. Töltsd ki az alkalmazás létrehozásához szükséges adatokat
   - A szokásos adatokra már nem térek ki (Előfizetés, erőforráscsoport)
   - Név: Legyen valami, ami leírja a szolgáltatásunkat. pl. okos-otthon
   - Application url, az a névből lesz generélva, de megváltoztathatod.
   - Template: Válaszd ki a "Custom application" lehetőséget.
   - Region: Válaszd ki a legközelebbi régiót.
   - Pricing plan: Válaszd ki a megfelelőt.
6. Kattints a "Review + create" gombra, majd a "Create" gombra az alkalmazás létrehozásához.

### IoT Central alkalmazás konfigurálása

Létrehozás után nyissuk meg az IoT Central alkalmazást, majd az Overview fülre kattintsunk és ott megnyitjuk az IoT Central Application URL-t. Ekkor új tab-on megnyílik a böngészőnkben, ahol el is kezdhetjük a konfigurálást.

### Eszközsablon létrehozása

1. Az IoT Central alkalmazásban navigálj az "Eszközök" menüpontra.
2. Kattints az "Eszközsablonok" menüpontra.
3. Kattints az "IoT-eszköz" gombra, majd a lap alján kattints a "Következő: Testreszabás" gombra.
4. Eszközsablon neve legyen valami beszédes, pl.: "Hőmérséklet-érzékelő". Majd kattints a "Következő: ellenőrzés" gombra.
5. Végül a "Létrehozás" gombra kattintva hozd létre az eszközsablont.
6. Adj hozzá egy képességet:
   - Hőmérséklet
   - temperature
   - Telemetria
   - Temperature
7. Mentsd el a módosításokat.
8. Kattints a "Közzététel" gombra az eszközsablon közzétételéhez.

### Eszköz létrehozása

1. Az IoT Central kezdőlapján máris látunk egy "Eszköz hozzáadása" gombot. Itt kezdünk.
2. Az Új eszköz létrehozása ablakban láthatjuk, hogy van egy generált eszköznév (ezt módosítjuk, hogy beszédesebb legyen a neve. Pl.: homerseklet-001) és egy eszközazonosítóv (ez maradjon így, mert egyedinek kell lennie). Ezeket az értékeket felhasználhatjuk az alkalmazásunkban.
3. Eszköz sablon legyen a fent létrehozott. Pl.: Hőmérséklet-érzékelő
4. Fontos, hogy a Szimulált eszköz? jelölőnégyzet ki legyen kapcsolva. (ellenkező esetben nem fogunk tudni hozzá csatlakozni.)
5. Kattintsunk a "Létrehozás" gombra az eszköz létrehozásához.

### Tárolt adatok beállítása

1. Az IoT Central alkalmazásban navigálj az "Alkalmazás" menüpontra.
2. Kattints az "Eszköz fájltárolója" fülre.
3. Válaszd ki a "Tárfiókot", majd a tárolót.
4. A "Hozzáférés a tárolt fájlokhoz az IoT Centralban" lehetőség bekapcsolása is hasznos.
5. Végül mentsük el a beállításokat a "Mentés" gombra kattintva.

## Python alkalmazás

### Alkalmazás előkészítése

Előfeltétel, hogy a gépeden legyen telepítve Python 3.9 vagy újabb verzió.

1. Nevezd át a `_.env` fájlt `.env`-ra.
2. Töltsd ki a `.env` fájlt a megfelelő értékekkel.
   - Az IoT Central alkalmazásban létrehozott eszközt keresd meg és nyisd meg. Találszegy "Csatlakozás" vagy "Connect" gombot. Kattints rá, és másold ki a szükséges értékeket.
   - IOTC_ID_SCOPE={ID scope}
   - IOTC_DEVICE_ID={Device ID}
   - IOTC_DEVICE_KEY={Primary vagy Secondary key}
   - SEND_INTERVAL_SEC=5
3. Hozd létre a Python virtuális környezetet:
   ```bash
   python -m venv venv
   ```
4. Aktiváld a virtuális környezetet:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
     vagy
     ```PowerShell
     . .venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. Telepítsd a szükséges csomagokat:
   ```bash
   pip install -r requirements.txt
   ```
6. Futtasd az alkalmazást:
   ```bash
   python iot.py
   ```
7. Kimenet az alábbi lesz:
   ```
   DPS provisioning…
   Assigned IoT Hub: <assigned_hub>
   Connecting IoT Hub…
   Connected.
   Küldési intervallum: 5s. Leállítás: Ctrl+C
   [1] → {'deviceId': 'homerseklet-001', 'temperature': 22.0, 'timestamp': '2023-03-15T12:00:00Z'}
   [2] → {'deviceId': 'homerseklet-001', 'temperature': 22.1, 'timestamp': '2023-03-15T12:00:05Z'}
   [3] → {'deviceId': 'homerseklet-001', 'temperature': 22.0, 'timestamp': '2023-03-15T12:00:10Z'}
   ```
8. Ha leállítod az alkalmazást (Ctrl+C), a következő üzenet jelenik meg:
   ```
   Disconnecting…
   Bye.
   ```

## Adatok kezelése

### Bejövő adatok

Az IoT Central alkalmazásban a bejövő adatokat az "Eszközök" menüpont alatt találod. Itt láthatod az összes csatlakoztatott eszközt és azok aktuális állapotát. Az eszközök által küldött adatok megjelennek a megfelelő eszköz részleteinél.

Ha kiválasztod az egyik eszközt, majd rákattintasz a "nyers adatok" fülre, akkor láthatod az eszköz által küldött nyers adatokat.

### Irányítópult

1. Az IoT Central alkalmazásban navigálj az "Irányítópult" menüpontra.
2. Az ott lévőnél kattintsunk a "Szerkesztés" gombra.
3. Távolítsuk el a csempéket
4. Adjunk hozzá egy "Vonaldiagram" csempét.
5. Állítsuk be a "Vonaldiagram" csempe nevét. Pl.: Hőmérséklet - élő. Emellett állítsuk be az alábbiakat:
   - Tartomány megjelenítése
   - Eszközcsoport: Hőmérséklet-érzékelők
   - Eszközök: válasszuk mindet
   - Telemetria: adjunk hozzá egy képeséget.
6. Frissítés gomb megnyomása, hogy elmentsük a módosításokat.
7. Láthatjuk a hőmérséklet adatokat a csempén.
8. A "Mentés" gombra kattintva elmenthetjük a módosításokat.

### Riasztási szabály

1. Keressük meg a "Szabályok" menüpontot az IoT Central alkalmazásban.
2. Hozzunk létre egy újat:
   - Név: Magas hőmérséklet
   - Eszközsablon: Hőmérséklet-érzékelő
   - A szabály aktiválása ha: az alábbi feltételek bármelyike igaz
   - Telemetria: Hőmérséklet
   - Operátor: Nagyobb vagy egyenlő
   - Adjon meg egy értéket: 25
   - Műveletek: Válasszunk egyet az előre definiált műveletek közül és állítsuk be a kívánt értesítést.
3. Végül a "Mentés" gombra kattintva elmenthetjük a szabályt.

Ezzel, ha a hőmérséklet eléri vagy meghaladja a 25 °C-ot, a rendszer értesítést küld.
