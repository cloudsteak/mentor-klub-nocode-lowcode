# Azure Functions

Az Azure Functions egy felhőalapú eseményvezérelt számítási szolgáltatás, amely lehetővé teszi a fejlesztők számára, hogy könnyedén létrehozzanak és futtassanak kódot válaszul eseményekre anélkül, hogy a háttérinfrastruktúrával kellene foglalkozniuk.

## Fájlok

- [README.md](README.md): A bemutató leírása.
- [feliratkozó mappa](feliratkozo): Python alkalmazás a feliratkozás teszteléséhez.

## Példa

Azure Function segítségével készítünk egy egyszerű megoldást, amely egy weboldalon lévő hírlevél‑feliratkozó űrlap adatait (név, email) menti el tárfiókba, hogy azokat később fel lehessen dolgozni (Pl. Logic Apps vagy Data Factory segítségével).

## Előkészületek

1. Azure fiók létrehozása vagy bejelentkezés.
2. Erőforráscsoport létrehozása.
3. Azure Functions létrehozása.
4. Tárfiók létrehozása.

### Tárfiók létrehozása

1. Nyisd meg a [Azure Portal](https://portal.azure.com/) weboldalt.
2. Kattints az "Create a resource" gombra.
3. Keress rá és válaszd ki a "Storage account" (tárfiók) lehetőséget.
4. Töltsd ki a szükséges mezőket (előfizetés, erőforráscsoport, név, stb.).
   - Neve legyen: hirlevelfeliratkozas
   - Elsődleges szolgáltatás: Blob Storage és Data Lake Storage
   - Rendelkezésreállás: LRS (Locally Redundant Storage)
5. Kattints a "Review + create" gombra, majd a "Create" gombra.

### Azure Functions létrehozása

1. Nyisd meg a [Azure Portal](https://portal.azure.com/) weboldalt.
2. Kattints az "Create a resource" gombra.
3. Keress rá és válaszd ki a "Function App" lehetőséget.
4. Töltsd ki a szükséges mezőket (előfizetés, erőforráscsoport, név, stb.).
   - Díjcsomag: Consumption (Ez azt jelenti, hogy csak a ténylegesen használt erőforrásokért kell fizetni.)
   - Neve legyen: hirlevel-feliratkozas-funkcio
   - OS: Windows
   - Programnyelv: NodeJs 22 LTS
   - Tárfiók: hirlevelfeliratkozas
5. Kattints a "Review + create" gombra, majd a "Create" gombra.

## Funkciók létrehozása és beállítása

1. Nyisd meg Portálon az új Function App-ot: hirlevel-feliratkozas-funkcio.
2. Áttekintési oldalon kattints a "Funkció létrehozása" gombra.
3. Sablonok közül válaszd: "HTTP trigger", majd kattints a "Következő" gombra.
4. Töltsd ki a szükséges mezőket (név, stb.).
   - Név: Feliratkozas-mentese
   - Hitelesítés: anonymous (**Fontos: ez lehetővé teszi, hogy a funkciót hitelesítés nélkül hívják meg. Ilyet nem állítunk be élő rendszeren.**)
5. Kattints a "Létrehozás" gombra.
6. Várj, amíg a funkció létrejön. Ekkor meg is nyílik a szerkesztő felület.
7. Kattints a "Függvény URL-címének beolvasása" gombra. Itt látod a függvény URL-címét, amelyet a hírlevél-feliratkozó űrlap adataainak mentéséhez használhatsz. Ezt ha beilleszted a böngésződbe, akkor. a függvényben most látható üzenetet fogod látni.
   Pl: https://hirlevel-feliratkozas-funkcio.azurewebsites.net/api/Feliratkozas-mentese?name=MentorKlub
8. A szerkesztőben cseréld ki a meglévő kódot az alábbi kódra, hogy magyar nyelven legyen:

```javascript
module.exports = async function (context, req) {
  context.log("A JavaScript HTTP trigger függvény feldolgozott egy kérést.");

  const name = req.query.name || (req.body && req.body.name);
  const responseMessage = name
    ? "Szia, " + name + ". Gratulálok az első Azure függvényedhez."
    : "Ez a HTTP-vezérelt függvény sikeresen végrehajtódott. Adj meg egy nevet a lekérdezési karakterláncban vagy a kérés törzsében a személyre szabott válaszhoz.";

  context.res = {
    // status: 200, /* Defaults to 200 */
    body: responseMessage,
  };
};
```

9. Kattints a "Mentés" gombra.
10. Hívd meg újra a függvény URL-címét a böngészőben, és teszteld a funkciót. Eredmény:

```text
Szia, MentorKlub. Gratulálok az első Azure függvényedhez.
```

11. Ezzel van egy alap funkciónk, most adjuk hozzá a példának megfelelő üzleti logikát.

## Blob kimenet beállítása

1. A Függvény szerkesztőben
2. A szerkesztő fölött keresd meg: Integráció
3. Ez egy vizuális felület, ahol beállíthatod a függvény bemeneti és kimeneti kapcsolatait.
4. Kattints a "Kimenet hozzáadása" gombra.
5. Töltsd ki a mezőket a következőképpen:
   - Kimeneti típus: Azure Blob Storage
   - Storage account connection → Új és utána válaszd ki: hirlevelfeliratkozas
   - Blob parameter name: outputBlob
   - Blob tároló neve: feliratkozasok
   - Path: feliratkozasok/{rand-guid}.json
6. Hozzáadás gombra kattintás után csatolódik a kimenet a függvényhez.

## Kód frissítése a kérések fogadásához

1. Lépj vissza a "Kódolás és tesztelése" fülre.
2. Bizonyosodj meg róla, hogy az "index.js" fájlt szerkeszted.
3. Cseréld ki a meglévő kódot az alábbi kódra:

```javascript
// Node.js 22 – HTTP indítás, majd Blob kimenet ("outputBlob")
module.exports = async function (context, req) {
  try {
    if (req.method !== "POST") {
      context.res = { status: 405, body: "Engedélyezett metódus: POST" };
      return;
    }

    const data = req.body || {};
    // Minimális adatellenőrzés
    if (!data.name || !data.email) {
      context.res = { status: 400, body: "Név vagy email hiányzik" };
      return;
    }

    // Mentendő tartalom
    const payload = {
      name: data.name,
      email: data.email,
      timestampUtc: new Date().toISOString(),
    };

    // A Blob kimenet hozzárendelés neve az integráció részben: "outputBlob"
    // A path értéke ugyanott: feliratkozasok/{rand-guid}.json
    context.bindings.outputBlob = JSON.stringify(payload);

    context.res = {
      status: 201,
      headers: { "Content-Type": "application/json" },
      body: { ok: true, message: "Mentve", data: payload },
    };
  } catch (e) {
    context.log("Hiba:", e);
    context.res = { status: 500, body: "Szerverhiba" };
  }
};
```

4. Kattints a "Mentés" gombra.

## Funkció tesztelése - Portálon

1. Válts a "Teszt/Futtatás" fülre.
2. Válaszd ki a "POST" metódust.
3. "Fejlécek" szakaszban add meg a következőket:
   - Kulcs: Content-Type
   - Érték: application/json
4. A "Kérés törzse" mezőbe írd be a tesztelni kívánt JSON adatokat, például:

```json
{
  "name": "MentorKlub",
  "email": "mentor@klub.hu"
}
```

5. Kattints a "Futtatás" gombra.
6. Eredmény:
   - HTTP-válaszkód: 201
   - HTTP-válasz tartalma:
   ```json
   {
     "ok": true,
     "message": "Mentve",
     "data": {
       "name": "MentorKlub",
       "email": "mentor@klub.hu",
       "timestampUtc": "2025-xx-yyT11:55:38.939Z"
     }
   }
   ```
7. Most menj át a Tárfiókra, keresd meg a feliratkozások tárolót, és ellenőrizd, hogy a JSON fájl létrejött-e a megfelelő adatokkal.

## Funkció tesztelése - webalkalmazás

Itt egy egyszerű webalkalmazás kódjából fogjuk meghíni a függvényt, hogy lásd, hogyan működik a HTTP kérés.

### CORS engedélyezése (ha helyi HTML-ből hívod)

A CORS (Cross-Origin Resource Sharing) lehetővé teszi, hogy a webalkalmazásod HTTP kéréseket küldjön az Azure Functions végpontjára. Ez azért fontos, mert a böngészők biztonsági okokból alapértelmezés szerint blokkolják a különböző eredetű (cross-origin) kéréseket.

1. Function App szintjén: API → CORS.
2. Add hozzá a webalkalmazásod URL-jét (pl. http://localhost:5000, ha helyileg futtatod).
3. Kattints a "Mentés" gombra.

### Webalkalmazás kód példa

Egy egyszerű kód példát találsz a [feliratozo](feliratozo) mappában.

1. Nevezd át a `_.env` fájlt `.env`-ra.
2. A `.env` fájlban állítsd be az `FUNCTION_URL` változót a saját Azure Function URL-edre.
3. Készíts egy Python virtuális környezetet a `feliratozo` mappában:
   - Linux/Mac/Windows
   ```bash
   cd feliratozo
   python -m venv venv
   ```
   - Linux/Mac
   ```bash
   source venv/bin/activate
   ```
   - Windows
   ```bash
   .\venv\Scripts\activate
   ```
4. Telepítsd a szükséges csomagokat:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Futtasd a Flask alkalmazást:
   ```bash
   flask run
   ```
6. Ellenőrizd, hogy a Flask alkalmazás megfelelően fut-e a `http://localhost:5000` címen.

7. Iratkozz fel a hírlevélre a webalkalmazás felületén.
8. Ha sikeres, ellenőrizd az eredményt a Tárfiókban.
