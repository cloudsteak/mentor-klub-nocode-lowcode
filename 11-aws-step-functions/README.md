# AWS Step Functions

Az AWS Step Functions egy felhőalapú szolgáltatás, amely lehetővé teszi a felhasználók számára, hogy könnyedén létrehozzanak és kezeljenek összetett munkafolyamatokat. A Step Functions segítségével vizuálisan tervezhetők meg a munkafolyamatok, és integrálhatók az AWS szolgáltatások.

## Fájlok

- [Bolti_eladasok.csv](Bolti_eladasok.csv): Minta fájl feltöltéshez.
- [tesz_input.json](tesz_input.json): Bemeneti JSON példa a teszteléshez.
- [README.md](README.md): A bemutató leírása.

## Példa

Több fájl automatikus átmozgatása S3 könyvtárak között Step Functions-el. Gyakori igény: egy "beerkezo" könyvtárból a fájlokat át kell helyezni egy "feldolgozott" könyvtárba.

## S3 bucket létrehozása

1. Nyisd meg az AWS Management Console-t.
2. Kattints az "S3" szolgáltatásra.
3. Kattints a "Create bucket" gombra.
4. Add meg a bucket nevét (pl. "fajlfeldolgozo") és válaszd ki a régiót.
5. Kattints a "Create" gombra.

## Mappák létrehozása

1. Kattints a "fajlfeldolgozo" bucket nevére.
2. Kattints a "Create folder" gombra.
3. Add meg a "beerkezo" mappa nevét és kattints a "Create" gombra.
4. Ismételd meg a 2-3. lépéseket a "feldolgozott" mappa létrehozásához.

## IAM Role

1. Nyisd meg az AWS Management Console-t.
2. Kattints az "IAM" szolgáltatásra.
3. Kattints a "Roles" menüpontra.
4. Kattints a "Create role" gombra.
5. Válaszd ki az "AWS service" lehetőséget, majd az "Step Functions" szolgáltatást.
6. Kattints a "Next" gombra.
7. Kattints a "Next" gombra.
8. Add meg a Role nevét: (pl. "StepFunctionsS3Role")
9. Írj valamit a "Description" mezőbe (pl. "Step Function hozzaferes az S3-hoz").
10. Kattints a "Create role" gombra.
11. Keresd meg a létrehozott szerepkört és kattints rá.
12. Add permissions → Create inline policy → JSON, majd illeszd be az alábbi JSON-t (Resource résznél módosítsd a bucket nevét a sajátodra):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BeerkezoOlvasTorol",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::fajlfeldolgozo/beerkezo/*"
    },
    {
      "Sid": "FeldolgozottFeltoltes",
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::fajlfeldolgozo/feldolgozott/*"
    },
    {
      "Sid": "BeerkezoListazasa",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::fajlfeldolgozo",
      "Condition": { "StringLike": { "s3:prefix": ["beerkezo/*"] } }
    }
  ]
}
```

13. Kattints a "Next" gombra.
14. Add meg a "Policy name" mezőt (pl. "StepFunctionsS3Policy-ReadWrite").
15. Kattints a "Create policy" gombra.

## Step Functions létrehozása és konfigurálása

1. Nyisd meg az AWS Management Console-t.
2. Kattints a "Step Functions" szolgáltatásra, azon belül pedig a "State machines" menüpontra.
3. Kattints a "Create state machine" gombra.
4. Válaszd ki a "Create from blank" lehetőséget és add meg a State machine nevét (pl. "FajlMozgato"). Type: "Standard".
5. Kattints a "Continue" gombra.
6. Ekkor megnyílik a Workflow definition szerkesztő.
7. A bal oldali panelon keresd meg az S3 (CopyObject) műveletet és húzd a Start állapot alá.
8. Most keresd meg az S3 (DeleteObject) műveletet és húzd a CopyObject állapot alá.
9. Config fülön a Permissions → Execute role mezőben válaszd ki a korábban létrehozott IAM szerepkört (pl. "StepFunctionsS3Role").
10. Menjünk vissza a Design fülre és kattintsunk a "CopyObject"lépésre.
11. Nevezzük át a Configuration fülön: "FajlokMasolasa"
12. Az "Argument & Output" fülön az Arguments mezőbe illeszd be az alábbiakat:

```json
{
  "Bucket.$": "$.bucket",
  "Key.$": "$.targetKey",
  "CopySource.$": "States.Format('{}/{}', $.bucket, $.sourceKey)"
}
```

13. Menjünk vissza a Design fülre és kattintsunk a "DeleteObject" lépésre.
14. Nevezzük át a Configuration fülön: "FajlokTorlese"
15. Az "Argument & Output" fülön az Arguments mezőbe illeszd be az alábbiakat:

```json
{
  "Bucket.$": "$.bucket",
  "Key.$": "$.sourceKey"
}
```

16. Amint látod, most hibát jelez mindkét lépés. Ez azért van, mert az új felület "JSONData" formátumban várja az adatokat, de nekünk a "JSONPath" formátumot kell használnunk. A hiba javításához módosítsuk az Arguments mezőt a következőképpen:

    - Kattints a Code fülre
    - Az ott lévő JSON-t módosítsd a következőképpen:
    - `"QueryLanguage": "JSONData"` → `"QueryLanguage": "JSONPath"`
    - `"Arguments"` → `"Parameters"`
    - A `"Next": "FajlokTorlese"` sor elé add hozzá ezt: `"ResultPath": null,`

17. Így néz ki:

```json
{
  "Comment": "A description of my state machine",
  "StartAt": "FajlokMasolasa",
  "States": {
    "FajlokMasolasa": {
      "Type": "Task",
      "Parameters": {
        "Bucket.$": "$.bucket",
        "Key.$": "$.targetKey",
        "CopySource.$": "States.Format('{}/{}', $.bucket, $.sourceKey)"
      },
      "Resource": "arn:aws:states:::aws-sdk:s3:copyObject",
      "ResultPath": null,
      "Next": "FajlokTorlese"
    },
    "FajlokTorlese": {
      "Type": "Task",
      "Parameters": {
        "Bucket.$": "$.bucket",
        "Key.$": "$.sourceKey"
      },
      "Resource": "arn:aws:states:::aws-sdk:s3:deleteObject",
      "End": true
    }
  },
  "QueryLanguage": "JSONPath"
}
```

18. Mentsük el a "Create" gombra kattintva a State machine-t.

## Teszteljük a State machine-t

1. Menjünk az S3 konzolra.
2. Töltsünk fel legalább 1 fájlt a "fajlfeldolgozo/beerkezo" mappába. (Pl.: Bolti_eladasok.csv)
3. Ellenőrizzük, hogy a fájl megjelent-e a "fajlfeldolgozo/beerkezo" mappában.
4. Most menjünk vissza a "Step Functions" konzolra.
5. Keressük meg és kattintsunk rá az "Execute" gombra.
6. A megnyíló böngésző tab "Input - optional" mezőjébe illeszd be az alábbi JSON-t:

```json
{
  "bucket": "fajlfeldolgozo",
  "sourceKey": "beerkezo/Bolti_eladasok.csv",
  "targetKey": "feldolgozott/Bolti_eladasok.csv"
}
```

7. Kattintsunk a "Start execution" gombra.
8. Láthatjuk az eredményt. Az állapotgép végrehajtja a fájlok másolását és törlését az S3-ban.

## Feltétel hozzáadása

Ha kicsit szeretnénk tovább finomítani a folyamatot, hozzáadhatunk egy feltételt a State machine-hez. Például, ha csak akkor szeretnénk végrehajtani a fájlok másolását és törlését, ha a bemeneti fájl létezik.

Ennek a megoldásnak itt a JSON formátuma:

```json
{
  "Comment": "A description of my state machine",
  "StartAt": "Ellenorzes",
  "States": {
    "Ellenorzes": {
      "Type": "Task",
      "Parameters": {
        "Bucket.$": "$.bucket",
        "Prefix.$": "$.sourceKey"
      },
      "Resource": "arn:aws:states:::aws-sdk:s3:listObjects",
      "ResultPath": "$.list",
      "Next": "VanFajl"
    },
    "VanFajl": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.list.Contents[0].Key",
          "IsPresent": true,
          "Next": "FajlokMasolasa"
        }
      ],
      "Default": "NincsFajl"
    },
    "FajlokMasolasa": {
      "Type": "Task",
      "Parameters": {
        "Bucket.$": "$.bucket",
        "Key.$": "$.targetKey",
        "CopySource.$": "States.Format('{}/{}', $.bucket, $.sourceKey)"
      },
      "Resource": "arn:aws:states:::aws-sdk:s3:copyObject",
      "ResultPath": null,
      "Next": "FajlokTorlese"
    },
    "FajlokTorlese": {
      "Type": "Task",
      "Parameters": {
        "Bucket.$": "$.bucket",
        "Key.$": "$.sourceKey"
      },
      "Resource": "arn:aws:states:::aws-sdk:s3:deleteObject",
      "End": true
    },
    "NincsFajl": {
      "Type": "Succeed"
    }
  },
  "QueryLanguage": "JSONPath"
}
```

Most a State machine csak akkor fogja végrehajtani a fájlok másolását és törlését, ha a bemeneti fájl létezik az S3-ban.

Ellenőrizni hasonlóan kell, mint a [Teszteljük a State machine-t](#teszteljük-a-state-machine-t) részben.
