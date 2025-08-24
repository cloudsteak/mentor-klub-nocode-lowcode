# Azure Functions

Az Azure Functions egy felhőalapú eseményvezérelt számítási szolgáltatás, amely lehetővé teszi a fejlesztők számára, hogy könnyedén létrehozzanak és futtassanak kódot válaszul eseményekre anélkül, hogy a háttérinfrastruktúrával kellene foglalkozniuk.

## Fájlok

- [README.md](README.md): A bemutató leírása.

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
    - Hitelesítés: anonymous
5. Kattints a "Létrehozás" gombra.
6. Várj, amíg a funkció létrejön. Ekkor meg is nyílik a szerkesztő felület.
7. Kattints a "Függvény URL-címének beolvasása" gombra. Itt látod a függvény URL-címét, amelyet a hírlevél-feliratkozó űrlap adataainak mentéséhez használhatsz. Ezt ha beilleszted a böngésződbe, akkor. a függvényben most látható üzenetet fogod látni.
Pl: https://hirlevel-feliratkozas-funkcio.azurewebsites.net/api/Feliratkozas-mentese?name=MentorKlub
8. A szerkesztőben cseréld ki a meglévő kódot az alábbi kódra, hogy magyar nyelven legyen:

```javascript
module.exports = async function (context, req) {
    context.log('A JavaScript HTTP trigger függvény feldolgozott egy kérést.');

    const name = (req.query.name || (req.body && req.body.name));
    const responseMessage = name
        ? "Szia, " + name + ". Gratulálok az első Azure függvényedhez."
        : "Ez a HTTP-vezérelt függvény sikeresen végrehajtódott. Adj meg egy nevet a lekérdezési karakterláncban vagy a kérés törzsében a személyre szabott válaszhoz.";

    context.res = {
        // status: 200, /* Defaults to 200 */
        body: responseMessage
    };
}
```

9. Kattints a "Mentés" gombra.
10. Hívd meg újra a függvény URL-címét a böngészőben, és teszteld a funkciót. Eredmény:
```text
Szia, MentorKlub. Gratulálok az első Azure függvényedhez.
```
11. Ezzel van egy alap funkciónk, most adjuk hozzá a példának megfelelő üzleti logikát.
