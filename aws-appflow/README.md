# Amazon AppFlow

Az Amazon AppFlow egy felhőalapú szolgáltatás, amely lehetővé teszi az adatok egyszerű és biztonságos átvitelét különböző SaaS alkalmazások és AWS szolgáltatások között. Az AppFlow segítségével könnyedén integrálhatók az adatok, és automatizálhatók az adatfolyamok.

## Példa

Van egy Wordpress alapú Woocommerce webshop, amelyben a vásárlások adatai tárolódnak. Ezeket az adatokat szeretnénk automatikusan átkonvertálni és feltölteni egy Amazon S3 bucket-be, ahol további feldolgozásra kerülhetnek. (Pl. Amazon QuickSight-ban történő vizualizáció)

## Wordpress beállítások

1. Előfeltétel, hogy a Wordpress oldaladban telepítve legyen a [WooCommerce](https://woocommerce.com/) bővítmény.
2. Hasznos ha élő webshop, tehát már vannak megrendelők és vásárlások.
3. Jelentkezz be a Wordpress admin felületére.
4. Navigálj az "WooCommerce" → "Beállítások" → "Haladó" → "REST API" menüpontra.
5. Kattints az "Új kulcs létrehozása" gombra.
6. Add meg a kulcs nevét, válaszd ki a felhasználót és a jogosultságot. ("Olvasás" jogosultság elegendő a vásárlási adatok lekéréséhez.)
7. Kattints az "API-kulcs generálása" gombra.
8. Másold ki a generált "Felhasználói kulcs" és "Felhasználói titkos kulcs" értéket, mert később szükséged lesz rájuk.

## Amazon AppFlow beállítások

1. Jelentkezz be az AWS Management Console-ba.
2. Navigálj az "Amazon AppFlow" szolgáltatáshoz.
3. Kattints a "Connections" menüpontra, majd keresd meg a Connectors alatt a "WooCommerce" lehetőséget.
4. Kattints a "Create connection" gombra.
5. Add meg a kapcsolat nevét (Pl.: Webshop adatok), illeszd be a "Felhasználói kulcs" és "Felhasználói titkos kulcs" értéket
6. Add meg a weboldal URL-jét (Pl.: https://webshop.hu), majd kattints a "Connect" gombra.
7. A kapcsolat létrejön, és megjelenik a "Connections" listában.


## Fontos

- AppFlow-ban állítható a kimeneti formátum. (File format settings)
- Woocommerce kapcsolat esetén jó példa ha az  "Order" objektumot használjuk forrásként.
- Ha Amazon QuickSight-ban szeretnéd használni az AppFlow által létrehozott adatokat, akkor szükséges, hogy a QuickSight hozzáférést kapjon az S3 bucket-hez, ahová az AppFlow az adatokat feltölti.
  - Ehhez navigálj a QuickSight szolgáltatáshoz, majd a "Manage QuickSight" → "Security & permissions" menüpontra, és add hozzá az S3 bucket-hez való hozzáférést.
  - Amikor a Dataset-et létrehozod, szükséged lesz egy manifest fájlra, amely leírja az adatokat. Ezt a manifest fájlt az AppFlow automatikusan létrehozza, amikor az adatokat feltölti az S3 bucket-be. Találsz egy példa manifest fájlt a mappában, amelyet az AppFlow létrehozott: `manifest.json`. Ezt a manifest fájt módosítsd a saját S3 bucket-ed elérési útjára, majd töltsd fel a QuickSight-ba.
