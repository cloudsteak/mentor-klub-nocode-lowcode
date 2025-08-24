# AWS Amplify Studio

Az AWS Amplify Studio egy vizuális fejlesztői környezet, amely lehetővé teszi a felhasználók számára, hogy könnyedén létrehozzanak és kezeljenek web- és mobilalkalmazásokat. Az Amplify Studio segítségével gyorsan és egyszerűen tervezhetők meg a felhasználói felületek, és integrálhatók az AWS szolgáltatások.

## Fájlok

- [amplify.yaml](amplify.yaml): Az AWS Amplify konfigurációs fájlja.
- [README.md](README.md): A projekt leírása és dokumentációja.

## Példa

Mini-alkalmazás létrehozása az AWS Amplify Studio segítségével. Az alkalmazás forráskódja: https://github.com/cloudsteak/trn-angular

## Lépések

1. Lépj be az AWS Amplify Studio-ba.
2. Kattints a "Deploy an app" gombra.
3. "Deploy your app" ablakban válaszd ki a "GitHub" lehetőséget.
4. Kattints a "Next" gombra.
5. Felugró ablakban jelentkezz be a GitHub fiókoddal, majd kattints az "Authorize" gombra.
6. "Install AWS Amplify" ablakban válaszd ki azt a GitHub fiókot/szervezetet, amelyhez az alkalmazást telepíteni szeretnéd.
7. Lehetőséged van minden Repositoryhoz hozzáférést adni, vagy csak egy adott Repositoryhoz. (Ezt Rád bízom)
8. Kattints az "Install & Authorize" gombra.
9. Amint sikeres, visszatér az AWS felületére, ahol ki kell választanod a megfelelő repository-t.
10. Majd ki kell választanod azt a branch-t (ág), amelyet telepíteni szeretnél.
11. Kattints a "Next" gombra.
12. Add meg az alkalmazás nevét és ellenőrizd, hogy az Amplify jól olvasta-e fel a amplify.yaml fájl tartalmát.
13. Kattints a "Next" gombra.
14. Ellenőrizd a beállításokat, majd kattints a "Save and Deploy" gombra.
15. Várj, amíg az AWS Amplify befejezi az alkalmazás telepítését.
16. Amint a telepítés befejeződött, megjelenik az alkalmazás URL-je, amelyen elérheted az újonnan telepített alkalmazást.

## Fontos

- Az AWS Amplify Studio használata előtt győződj meg arról, hogy a projekted megfelel az AWS követelményeinek.
- Az Amplify alkalmazásokhoz szükséges egy `amplify.yaml` fájl, amely tartalmazza a projekt konfigurációját. Minden esetben ellenőrizd, hogy ez létezik-e a GitHub repository-ban.
