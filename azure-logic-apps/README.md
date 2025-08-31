# Azure Logic Apps

Az Azure Logic Apps egy felhőalapú szolgáltatás, amely lehetővé teszi a felhasználók számára, hogy könnyedén létrehozzanak és kezeljenek automatizált munkafolyamatokat. A Logic Apps segítségével a felhasználók vizuálisan tervezhetik meg a munkafolyamatokat, és integrálhatják az Azure szolgáltatásokat.

## Fájlok

- [README.md](README.md): A projekt leírása és útmutató a használathoz.

## Példa

A partnerek által a céges Gmail címre küldött PDF számlák automatikusan lementődnek a Google Drive-on egy megosztott mappába, így nincs szükség manuális letöltögetésre. Ez üzleti környezetben tipikus helyzet, hiszen a cégeknél rendszeresen előfordul, hogy a partnerektől e-mailben érkeznek számlák.

Ugyanez a példa megvalósítható más e-mail szolgáltatásokkal is, például a M365 és OneDrive használatával. (magán és céges előfizetésekkel is)

## Google Drive beállítása

1. Nyisd meg a [Google Drive](https://drive.google.com/) weboldalt.
2. Hozz létre egy új mappát, ahová a fájlokat menteni szeretnéd. Pl.: "Beérkező számlák"

## Logikai alkalmazás létrehozása

1. Nyisd meg a [Azure Portal](https://portal.azure.com/) weboldalt.
2. Kattints az "Új erőforrás létrehozása" gombra.
3. Keress rá és válaszd ki a "Logikai alkalmazás" lehetőséget.
4. Díjcsomag: Felhasználás vagy Megosztott (Ez azt jelenti, hogy csak a ténylegesen használt erőforrásokért kell fizetni.)
5. Töltsd ki a szükséges mezőket (előfizetés, erőforráscsoport, név, stb.).
6. Kattints a "Review + create" gombra, majd a "Create" gombra.

## Logikai alkalmazás tervezése

### Kiváltó esemény beállítása (email érkezik csatolmánnyal)

1. Nyisd meg a "Logikaialkalmazás-tervezőt".
2. Válaszd ki a "Üres alkalmazás" lehetőséget.
3. Keresd meg a "Új e-mail érkezésekor" (GMAIL) trigger-t, és válaszd ki.
4. Kapcsolódj a GMAIL fiókodhoz.
5. Speciális paramétereknél add hozzá a "tárgy" paramétert.
6. Állítsd be a trigger-t a következőképpen:
   - Tárgy: `[SZÁMLA]`
   - Melléklettel rendelkezik: "Igen"
   - Mellékletek is: "Igen"
   - Milyen gyakran szeretne elemeket keresni? (30 perc)
   - Time Zone: Budapest (UTC+1)

### Csatolmány ellenőrzése (csak PDF)

1. Kattints a "Új lépés beszúrása" gombra. (+ jel)
2. Művelet hozzáadása
3. Keresd meg a "Feltétel" vagy "Condition" műveletet, és válaszd ki.
4. Állítsd be a feltételt a következőképpen:
   - Kattints a "Villám" ikonra
   - Válaszd ki a "Mellékletek név" dinamikus tartalmat
   - Válaszd ki a "ends with" műveletet
   - Írd be a következőt: `.pdf`
5. Igaz ágon folytatjuk tovább

### Fájl létrehozása a Google Drive-on

1. Kattints a "Új lépés beszúrása" gombra. (+ jel)
2. Művelet hozzáadása
3. Keresd meg a "Google Drive - Fájl létrehozása" műveletet, és válaszd ki.
4. Kattints a "Bejelentkezés" gombra, és kövesd az utasításokat a Google Drive fiókodhoz való csatlakozáshoz.
5. Állítsd be a műveletet a következőképpen:
   - Mappa: Válaszd ki a korábban létrehozott "Beérkező számlák" mappát.
   - Fájl neve: Válaszd ki a "Mellékletek név" dinamikus tartalmat. (ha azt szeretnéd, hogy ne legyen hiba biztosan, akkor ezt add meg a dinamikus tartalomnál: `concat(split(item()?['Name'],'.')[0],'-',formatDateTime(utcNow(),'yyyyMMdd-HHmmss'),'.pdf')`)
   - Fájl tartalma: Válaszd ki a "Mellékletek tartalma" dinamikus tartalmat.

### Mentés és tesztelés

1. Kattints a "Mentés" gombra a szerkesztő jobb felső sarkában.
2. A mentés után kattints a "Futtatás" vagy "Run" gombra.
3. Küldj egy emailt a céges Gmail címre a megfelelő PDF csatolmányokkal és a megfelelő tárggyal. (pl.: [SZÁMLA] - Cég neve)
4. Nézd a futási előzményeket, hogy ellenőrizd a folyamat állapotát.
5. Ellenőrizd a Google Drive mappát, hogy a fájlok sikeresen létrejöttek-e.
