# AWS Proton

Az AWS Proton egy felhőalapú szolgáltatás, amely lehetővé teszi a fejlesztők számára, hogy könnyedén telepítsenek és kezeljenek konténerizált alkalmazásokat. Az AWS Proton segítségével a fejlesztők egyszerűen definiálhatják az alkalmazások architektúráját, és automatizálhatják a telepítési folyamatokat.

## Fájlok

- [README.md](README.md): A bemutató leírása.

## Példa

Sablonból futó Fargate webszolgáltatás.


## Előfeltételek

- Régió: javasolt eu‑central‑1 (Frankfurt).
- AWS jogosultság: admin vagy Proton‑admin + kapcsolódó szolgáltatások.
- GitHub fiók.

## GitHub kapcsolat létrehozása

1. Az AWS Console megnyitása.
2. Navigálás a "Proton" szolgáltatáshoz.
3. Nyisd meg a "Repository connections" menüpontot.
4. Kattints a "Create connection" gombra.
5. Válaszd ki a "GitHub" lehetőséget.
6. Kövesd az utasításokat a GitHub fiók összekapcsolásához.


## Minta repository-k forkolása

1. Nyisd meg a GitHub fiókodat.
2. Keresd meg a forkolni kívánt repository-t.
    - Environment + service sablonok: https://github.com/aws-samples/aws-proton-cloudformation-sample-templates
    - Alkalmazás kód: https://github.com/aws-samples/aws-proton-sample-services
3. Mindkettőt forkold a saját GitHub fiókodba.

## Környezet sablon létrehozása

1. Nyisd meg az AWS Proton konzolt.
2. Kattints a "Create environment template" gombra.
    - `Create a template for provisioning new environments`
    - Sync a template bundle from Git
    - Link another Git repository
    - GitHub  
3. Válaszd ki a forkolt environment sablont a "CodeStar connection" alatt.
    - Repository: `aws-proton-cloudformation-sample-templates`
    - Branch: `main`
    - Environment template bundle directory - optional: `/loadbalanced-fargate-svc/loadbalanced-fargate-env`
    - Environment template name: `loadbalanced-fargate-env`
4. Hozd létre a template-t.


## Service sablon létrehozása

1. Nyisd meg az AWS Proton konzolt.
2. Kattints a "Create service template" gombra.
    - Sync a template bundle from Git
    - Link another Git repository
    - GitHub
3. Válaszd ki a forkolt service sablont a "CodeStar connection" alatt.
    - Repository: `aws-proton-cloudformation-sample-templates`
    - Branch: `main`
    - Service template bundle directory - optional: `/loadbalanced-fargate-svc/loadbalanced-fargate-svc`
    - Service template name: `loadbalanced-fargate-svc`
    - Compatible environment templates: `loadbalanced-fargate-env`


## Sablonok publikálása

1. Nyisd meg az AWS Proton konzolt.
2. Nyisd meg szerkesztésre mindkét sablont.
3. A "Template version" draft-ban van. Kattints a "Publish" gombra a kívánt sablon mellett.

## Environment létrehozása

1. Nyisd meg az AWS Proton konzolt.
2. Kattints a "Create environment" gombra.
3. Válaszd ki a kívánt environment sablont.
4. Kövesd az utasításokat az environment létrehozásához.
    - Environment name: low-code-env
    - Environment description: low-code-env-role
    - Role: Create a new role in IAM
    - New role name: `low-code-env-role`
5. Kattints a "Next" gombra.
6. Végül kattints a "Create" gombra az environment létrehozásához.

## CI/CD pipeline role beállítása (Account settings)

1. Nyisd meg az AWS Proton konzolt.
2. Válaszd a "Account settings" menüpontot, majd Configure.
3. CI/CD AWS-managed provisioning pipeline role
    - Existing role name: `low-code-env-role`
    - Mentsd el a változásokat a "Save changes" gombra kattintva.

## Service létrehozása

1. Nyisd meg az AWS Proton konzolt.
2. Kattints a "Create service" gombra.
3. Válaszd ki a kívánt service sablont.
4. Kövesd az utasításokat a service létrehozásához.
    - Service name: `low-code-svc`
    - Service description: `low-code-svc-role`
    - Link another Git repository
    - GitHub
    - Repository: `aws-proton-sample-services`
    - Branch: `main`
5. Next
6. Service instance
    - Define your service directly in Proton
    - Instance name: `low-code-svc-instance`
    - Environment: `low-code-env`
7. Next
8. Review oldal alján kattints a "Create" gombra.
9. Várd meg, míg a service létrejön (15-20 perc).

## Tesztelés

1. Keresd meg a loadbalancer címét és nyisd meg a böngészőben.
2. Ellenőrizd, hogy a szolgáltatás elérhető-e a loadbalancer címén.

## Lényeg

Vissza Protonba: sablonból kaptunk teljes környezetet (VPC+ECS+ALB), "a fejlesztő csak pár mezőt töltött ki".


## Környezet törlése

- Proton → Services → low-code-svc → Delete service.
– Várd meg, míg eltűnik az ECS service, target group, stb.
- Proton → Environments → low-code-env → Delete environment.
- (Opcionális) Templates → Service templates / Environment templates
– Töröld a v1 verziót, majd magát a template‑et is, ha nem kell.
- (Opcionális) Settings → Repository connections: törölheted a GitHub connection‑t, ha csak a demóhoz kellett.
- (Opcionális) IAM → Roles: törölhető a low-code-pipeline-role, ha nincs rá többé szükség.
- (Opcionális) Nézz rá az S3 artifact bucketre és a CloudWatch Logs log groupokra (ECS/ALB) — ha akarsz, töröld.

