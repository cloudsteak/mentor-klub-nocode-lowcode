# AWS App Studio

Az AWS App Studio egy vizuális fejlesztői eszköz, amely lehetővé teszi alkalmazások gyors létrehozását kódolás nélkül vagy minimális kódolással. Segítségével üzleti felhasználók és fejlesztők egyaránt könnyedén tervezhetnek, építhetnek és telepíthetnek felhőalapú alkalmazásokat az AWS infrastruktúráján. Az eszköz támogatja az integrációt más AWS szolgáltatásokkal, így rugalmas és skálázható megoldásokat kínál.

## Fájlok

- [README.md](README.md): A bemutató leírása.

## Példa

A mi példánban most egy hírlevél feliratkozó alkalmazást fogunk létrehozni, amely lehetővé teszi a felhasználók számára, hogy feliratkozzanak egy hírlevélre, és az admin csapat számára, hogy kezelje a feliratkozókat ugyanabban az alkalmazásban.

## Előkészület


### AWS App Studio Instance létrehozása

1. Lépj be az AWS App Studio-ba az AWS Management Console-on keresztül.
2. Hozz létre egy új App Studio példányt: "Create an AWS App Studio instance (Standard create)".
3. SSO beállításoknál válaszd ki a megfelelő "IAM Identity Center" csoportokat.
4. Acknowledgment részben fogadd el a feltételeket.
5. Kattints a "Set up" gombra.
6. Nagyjából 20 perc múlva az AWS App Studio példányod készen áll.
7. Kattints a "Go to AWS App Studio" gombra.

## Lépések

1. Nyisd meg az AWS App Studio-t a linken, vagy a "Go to AWS App Studio" gombra kattintva.
2. Jelentkezz be a "Sign in" gombra kattintva, majd válaszd ki a megfelelő hitelesítési módszert.
3. Az "All applications" szakaszban kattints a "Create app" gombra.
4. Adj nevet az alkalmazásnak, döntsd el, hogy melyik megközelítést választod:
   - Generate an app with AI: Mesterséges intelligencia segítségével történő alkalmazásgenerálás
   - Start from scratch: Üres alkalmazásból való indulás
5. Válaszd a "Generate an app with AI" lehetőséget.
6. Kattints a "Next" gombra.
7. A "Connect to existing data - optional" szakaszban válaszd ki a megfelelő adatforrást, ha szükséges. Mi most a "Skip" lehetőséget választjuk.
8. Tudunk előre elkészített megoldásokat is használni és tudunk Prompt Engineeringet is alkalmazni.

   - Promt legyen a következő, amelyet angolul kell megadnunk:

   ```
   App name: Newsletter Signups

   Build an app that lets people subscribe to a newsletter and lets the team manage subscribers in the same app.

   Requirements:
   - Public signup form (no sign-in required) with fields:
       • full_name (string, required)
       • email (string, required, must be unique, validate email format)
       • Prevent duplicate emails (case-insensitive). Show a friendly “Thanks for subscribing” confirmation and clear the form.
       • status and created_at fields are hidden on signup form
       • On submit: create a record with default status = "Subscribed", store created_at (DateTime).

   - Management area (requires sign-in):
       • List view of subscribers with columns: full_name, email, status, created_at.
       • Search by name or email; quick filter by status (Subscribed, Unsubscribed).
       • Sort by created_at (newest first).
       • Details page + edit form to change full_name and status; email is read-only.
       • status must be a single select field (values: Subscribed, Unsubscribed)
       • status options must be Subscribed, Unsubscribed
       • On edit form the created_at field is hidden
       • Row actions: Unsubscribe, Delete.
       • Bulk action: Export current list to CSV.

   - Permissions:
       • Role "Admin": full create/read/update/delete.
       • Role "Editor": read, create, update name/status, cannot delete.
       • Public users can only access the signup form.

   UX:
       - Keep the app simple and mobile-friendly.
       - Validate inputs and show inline error messages.
   ```

9. Pár perc múlva kapunk egy leírást az alkalmazásról. Ha az tetszik, akkor a "Generate app" gombra kattintva létrehozhatjuk az alkalmazást.
10. Az alkalmazás létrehozása után megteinthetjük vagy szerkeszthetjük az alkalmazást az AWS App Studio felületén.
11. Ha véglegesnek tekintjük, akkor a "Publish center"-ben publikálhatjuk az alkalmazást a megfelelő környezetre.

## Fontos

- A szolgáltatás jelenleg csak az alábbi AWS régiókban érhető el: US West (Oregon), Europe (Ireland).

## Kiegészítő információk

Ha egy gyors információs alkalmazást szeretnél lkétrehozni, akkor az AWS App Studio egy nagyszerű eszköz erre. Íme néhány adat, hogy építs valami hasznosat:

- Cég: Tenara
- Bemutatkozás: A Tenara egy technológiai csapat, amely cloud-natív és AI-alapú rendszereket tervez, épít és üzemeltet. Ügyfeleinknek végigkísért utat adunk: stratégiai workshop → architektúra → megvalósítás → üzemeltetés és folyamatos fejlesztés. Erősségünk a mérnöki fegyelem és az automatizáció: infrastruktúrát kódból (IaC) kezelünk, CI/CD-t építünk, Kubernetesen és felhőkben (pl. Azure, AWS) skálázunk, miközben a biztonság és a megfigyelhetőség (observability) alapértelmezett. Hiszünk az egyszerű, karbantartható megoldásokban, amelyek mérhető üzleti eredményt hoznak — gyorsabb piacra lépést, alacsonyabb üzemeltetési kockázatot és átlátható költségeket.
- Logó: https://d1ihfnbuu2yrpj.cloudfront.net/wp-content/uploads/2025/08/tenara-logo-tr.webp
- Banner: https://d1ihfnbuu2yrpj.cloudfront.net/wp-content/uploads/2025/08/tenara-banner-website-1920x600-no-logo.webp
- Video: https://www.youtube.com/embed/U6fC4Ij608A?si=5WaJQKVytehQRTOO
