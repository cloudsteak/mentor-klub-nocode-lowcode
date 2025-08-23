# AWS App Runner

Az Amazon App Runner egy felhőalapú szolgáltatás, amely lehetővé teszi a fejlesztők számára, hogy könnyedén telepítsenek és futtassanak konténerizált webalkalmazásokat anélkül, hogy a háttérinfrastruktúrával kellene foglalkozniuk.

## Fájlok

- [README.md](README.md): A projekt leírása és dokumentációja.

## Példa

1. "Hello, App Runner” – publikus konténer indítása pár kattintással.
2. "Apache" – publikus konténer indítása pár kattintással.

## Előkészületek

- A példához a nyilvános Amazon ECR galériájából fogunk használni egy Docker képet: https://gallery.ecr.aws/
- Győződj meg róla, hogy rendelkezel AWS fiókkal és jogosultságokkal az App Runner használatához.

## Lépések

1. Egy böngésző ablakban nyisd meg a [nyilvános Amazon ECR galériát](https://gallery.ecr.aws/).
2. Keress rá az "Apache" kifejezésre.
3. Az első találat a "docker/library/httpd" lesz. Ezt válaszd.
4. A legördülő menüből válaszd ki a "latest" verziót, és másol ki vágólapra. (public.ecr.aws/docker/library/httpd:latest)
5. Lépj be az [AWS Management Console](https://aws.amazon.com/console/) felületére.
6. Keresd meg az "App Runner" szolgáltatást, és válaszd ki.
7. Kattints az "Create service" gombra.
8. Válaszd ki a "Container registry" lehetőséget a Repository típusánál.
9. Provider legyen "Amazon ECR Public"
10. Illeszd be a korábban másolt Docker kép URL-jét a "Container image URI" mezőbe.
11. Kattints a "Next" gombra, és kövesd a további utasításokat a szolgáltatás létrehozásához. (Név, Port, skálázás, biztonság, stb.)
12. Miután a szolgáltatás létrejött, teszteld a működését a megadott URL-en.

_Megjegyzések_

- Az App Runner automatikusan kezeli a skálázást és a terheléselosztást.
- A szolgáltatás létrehozása után a megadott URL-en elérheted az alkalmazást.
- További információkért és részletes útmutatókért látogass el az [AWS dokumentációjára](https://docs.aws.amazon.com/apprunner/latest/dg/what-is.html).
- Domain nevet opcionálisan megadhatsz a szolgáltatás beállításainál.
