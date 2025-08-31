# Azure Data Factory

Az Azure Data Factory (ADF) egy felhőalapú adat-integrációs szolgáltatás, amely lehetővé teszi az adatok mozgatását és átalakítását különböző forrásokból és célokba. Az ADF segítségével könnyedén létrehozhatók adatfolyamok, amelyek automatizálják az adatok betöltését és feldolgozását.

## Példa

CSV adatok automatizált betöltése tárhelyre, alap tisztítás (oszlopok kiválasztása, dátumformátum, kerekítés), optimalizált Parquet kimenethez.

## Fájlok

- [Hibas_adatok.xlsx](Hibas_adatok.xlsx): A hibás adatokat tartalmazó bemeneti fájl.
- [README.md](README.md): A projekt leírását tartalmazó fájl.

## Azure Data Factory létrehozása

1. Jelentkezz be az Azure Portalba.
2. Kattints az "Új erőforrás" gombra.
3. Majd keresd meg az "Data Factory" szolgáltatást.
4. Add meg a Data Factory nevét, válaszd ki a régiót és a verziót (v2).
5. Git configuration: most válaszd a Configure later-t, ne állítsd be rögtön.
6. Kattints a "Létrehozás" gombra.
7. Várd meg, amíg a Data Factory létrejön, majd navigálj a Data Factory-hoz.
8. A Data Factory-ben navigálj az Identitások → "Managed Identity" menüpontra, és engedélyezd a Managed Identity-t.

## Tárfiók létrehozása

1. Jelentkezz be az Azure Portalba.
2. Kattints az "Új erőforrás" gombra.
3. Majd keresd meg az "Tárfiók" szolgáltatást.
4. Add meg a tárfiók nevét, válaszd ki a régiót és a teljesítmény szintet (Standard vagy Premium).
5. Fontos: Hierarchical namespace: Enabled ajánlott
6. Kattints a "Létrehozás" gombra.
7. Várd meg, amíg a tárfiók létrejön, majd navigálj a tárfiókhoz.
8. Storage‑ra adj "Storage-blobadatok közreműködője" jogot a Data Factory Managed Identity‑nek (Storage → Access control (IAM) → Add role assignment). (Ehhez szükséges jogok: tulajdonos vagy Felhasználói hozzáférés adminisztrátora)
9. Hozzunk létre két tárolót: `bemenet` és `kimenet`.
10. A `bemenet` tárolóba töltsük fel a [Hibas_adatok.xlsx](Hibas_adatok.xlsx) fájlt.

## Data Factory stúdió használata

1. A Data Factory-ben kattints a "Launch Studio" gombra.
2. Egy új böngésző tab-on megnyílik a Data Factory stúdió.

### Adatkészletek létrehozása

### Bemeneti adatkészlet

A hibás adatokat tartalmazó XLSX fájl betöltése.

1. A Data Factory stúdióban navigálj az "Szerző" → "Adatkészlet" menüpontra.
2. Kattints az "Új" gombra, majd válaszd az "Azure Data Lake Storage Gen2" lehetőséget.
3. Majd válaszd az "Excel" lehetőséget.
4. Add meg az adatkészlet nevét (Pl.: HibasAdatok).
5. Linked service: Hozz létre egy újat:
   - Neve legyen mondjuk `AdatTarhely`
   - Authentication type: System-assigned managed identity
   - Storage account: Válaszd ki a korábban létrehozott tárfiókot.
   - Kattints a "Create" gombra.
6. A "Fájl elérési útja" mezőben válaszd ki a hibás adatokat tartalmazó fájlt (Pl.: `Hibás_adatok.xlsx`).
7. A "Lap neve" mezőben válaszd ki a megfelelő munkalapot (Pl.: `Sheet1`).
8. A "Első sor mint fejléc" opciót jelöld be.
9. Kattints a "Ok" gombra.

### Kimeneti adatkészlet

A tisztított adatokat tartalmazó Parquet fájl létrehozása.

1. A Data Factory stúdióban navigálj az "Szerző" → "Adatkészlet" menüpontra.
2. Kattints az "Új" gombra, majd válaszd az "Azure Data Lake Storage Gen2" lehetőséget.
3. Majd válaszd a "Parquet" lehetőséget.
4. Add meg az adatkészlet nevét (Pl.: TisztaAdatok).
5. Linked service: Válaszd ki a korábban létrehozott linked service-t. (Ha ugyanabban a tárfiókban vannak az adatok, akkor ugyanazt használhatod.)
6. A "File path" mezőben add meg a kimeneti fájl elérési útját. Jelenleg csak a mappát tudod megadni, a fájlnevet később az adatfolyamban fogjuk beállítani.
7. Kattints a "Ok" gombra.
8. Ezután megjelenik a `TisztaAdatok` adatkészlet, amelyet később használni fogunk az adatfolyamban. Állítsuk be a compression type-ot: `Snappy`
9. Fájlnév legyen: `Tiszta_adatok.parquet`

_Megjegyzés: Mentsük el a jelenlegi munkát a Data Factory stúdióban, hogy ne veszítsük el a beállításokat. Ezt a "Publish" gombra kattintva tehetjük meg._

### Tisztítási DataFlow létrehozása

1. A Data Factory stúdióban navigálj az "Szerző" → "Data flows" menüpontra.
2. Kattints az "Új" gombra, majd válaszd a "Data flow" lehetőséget.
3. Add meg a DataFlow nevét (Pl.: AdatTisztitas).
4. A DataFlow szerkesztőben kattints az "Add source" gombra.
5. Válaszd ki a korábban létrehozott `HibasAdatok` adatkészletet.
6. Options részben kapcsold be az Allow schema drift opciót, hogy a DataFlow automatikusan kezelje az oszlopok változásait.
7. Sampling: Válaszd ki a "First 100 rows" lehetőséget, hogy csak az első 100 sort használja a DataFlow a teszteléshez.
8. A "Projection" fül alatt ellenőrizd, hogy az oszlopok helyesen vannak-e beállítva. Ha szükséges, módosítsd az oszlopok típusát.
9. Kattints a "+" gombra, itt láthatod a különböző adattranszformációs lehetőségeket.

### Adattisztítási lépések

1. **Irányítószám tisztítása**

   - Válaszd ki a "+" → "Származtatott oszlop" lehetőséget.
   - Adj hozzá egy új oszlopot, amelyben a következő kifejezést használod:
     ```sql
     regexReplace(regexReplace(regexReplace(iranyitoszam, '^(?i)H-', ''),'[^0-9]', ''),'^0+', '')
     ```
   - Ez eltávolítja a 'H-' előtagot, a nem szám karaktereket, és az esetleges vezető nullákat az irányítószámokból.

2. **Telefonszám tisztítása**

   - Válaszd ki a "+" → "Származtatott oszlop" lehetőséget.
   - Adj hozzá egy új oszlopot (`telefonszam_norm`), amelyben a következő kifejezést használod:

     ```sql
      iif( regexMatch(telefonszam, '^06'),
        regexReplace(telefonszam, '^06', '+36'),
        telefonszam
      )
     ```

   - Ez a kifejezés ellenőrzi, hogy a telefonszám 06-tal kezdődik-e, és ha igen, akkor +36-ra cseréli.

3. **Testsúly tisztítása**
   - Válaszd ki a "+" → "Származtatott oszlop" lehetőséget.
   - Adj hozzá egy új oszlopot (`testsuly_kg_norm`), amelyben a következő kifejezést használod:
     ```sql
      toInteger(regexReplace(toString(testsuly_kg), `[^0-9]`, ''))
     ```
   - Ez eltávolítja a testsúlyból a nem szám karaktereket, és egész számra konvertálja.

### Sink hozzáadása

1. Ha készen vagy az adattisztítási lépésekkel, akkor adj hozzá egy "Sink" komponenst a DataFlow-hoz.
2. A DataFlow szerkesztőben az utolsó adattisztítási lépés után kattints a "+" gombra, majd válaszd a "Sink" lehetőséget. (az utolsó elem a listában)
3. Válaszd ki a korábban létrehozott `TisztaAdatok` adatkészletet.
4. A "Sink" beállításoknál adj egy nevet `TisztaKimenet`.
5. ADataset type: Válaszd a "TisztaAdatok" lehetőséget (amit korábban létrehoztál).
6. Settings fülön a "File name options" részben válaszd az "Output to single file" lehetőséget, és add meg a fájl nevét (Pl.: `Tiszta_adatok.parquet`).

_Megjegyzés: Mentsük el a jelenlegi munkát a Data Factory stúdióban, hogy ne veszítsük el a beállításokat. Ezt a "Publish" gombra kattintva tehetjük meg._

### Pipeline létrehozása

1. A Data Factory stúdióban navigálj az "Szerző" → "Pipelines" menüpontra.
2. Kattints az "Új" gombra, majd válaszd a "Pipeline" lehetőséget.
3. Add meg a Pipeline nevét (Pl.: AdatTisztitasiFolyamat).
4. a. Ha ütemezetten szeretnéd futtatni az adattisztítást, akkor van lehetőséged ütemezés létrehozására:
   - A Pipeline szerkesztőben kattints az "Add trigger" gombra, majd válaszd a "New/Edit" lehetőséget.
   - Állítsd be a trigger típusát (Pl.: "Schedule") és a futtatási időpontot.
   - Kattints az "Ok" gombra a trigger mentéséhez.
5. b. Ha manuálisan szeretnéd futtatni, akkor csak néhány egyszerű lépést kell végrehajtanod
6. Bal oldalon az `Activities` panelen keresd meg a `Move and Transform` tevékenységet és azon belül keresd meg a `Data flow`-t, és húzd be a Pipeline területére.
7. A `Data flow` tevékenység beállításaiban, adj neki egy nevet, majd a Settings fülön válaszd ki a korábban létrehozott `AdatTisztitas` DataFlow-t.
8. Kattints a "Debug" gombra a Pipeline teszteléséhez.
9. Ellenőrizd a Pipeline futási eredményeit a "Monitor" fül alatt.

### Véglegesítés

- Ha végeztél az ellenőrzéssel, akkor a Data flow-ban tiltsd le a Sampling-ot.
- Finomítsd az ütemezést.
