# AWS Infrastructure Composer

Az AWS Infrastructure Composer egy vizuális fejlesztői környezet, amely lehetővé teszi a felhasználók számára, hogy könnyedén létrehozzanak és kezeljenek alkalmazásokat az AWS felhőben. Az Infrastructure Composer segítségével gyorsan és egyszerűen tervezhetők meg az alkalmazások architektúrái, és integrálhatók az AWS szolgáltatások.

## Fájlok

- [architectura-template.json](architectura-template.json): Az architektúra sablonja JSON formátumban.
- [architectura-template.yaml](architectura-template.yaml): Az architektúra sablonja YAML formátumban.
- [README.md](README.md): A bemutató leírása.

## Példa

Megmutatom az Infrastructure Composer alapfunkcióit egy VPC és egy EC2 létrehozásával.

## AWS Infrastructure Composer projekt

1. Nyisd meg az AWS Management Console-t.
2. Keresd meg a "CloudFormation" szolgáltatást.
3. Ezen belül kattints az "Infrastructure Composer" szolgáltatásra.
4. A bal oldali elemek közül drag-and-drop módszerrel húzd be a szükséges AWS szolgáltatásokat a vászonra.
5. VPC: `VirtualisHalozat`

```json
{
  "CidrBlock": "10.0.0.0/16",
  "EnableDnsSupport": true,
  "EnableDnsHostnames": true,
  "Tags": [
    {
      "Key": "Name",
      "Value": "mentor-klub-vpc"
    }
  ]
}
```

6. Subnet: `FrontendSubnet`

```json
{
  "VpcId": {
    "Ref": "VirtualisHalozat"
  },
  "CidrBlock": "10.0.1.0/24",
  "MapPublicIpOnLaunch": true,
  "AvailabilityZone": "eu-central-1a",
  "Tags": [
    {
      "Key": "Name",
      "Value": "frontend-1a"
    }
  ]
}
```

7. InternetGateway: `InternetKapcsolat`

```json
{
  "Tags": [
    {
      "Key": "Name",
      "Value": "mentor-klub"
    }
  ]
}
```

8. VPCGatewayAttachment: `InternetKapcsolatCsatolas`

```json
{
  "VpcId": {
    "Ref": "VirtualisHalozat"
  },
  "InternetGatewayId": {
    "Ref": "InternetKapcsolat"
  }
}
```

9. RouteTable: `UtvonalValaszto`

```json
{
  "VpcId": {
    "Ref": "VirtualisHalozat"
  },
  "Tags": [
    {
      "Key": "Name",
      "Value": "mentor-klub"
    }
  ]
}
```

10. Route szabály az internet gateway-hez: `UtvonalInternet`

```json
{
  "RouteTableId": {
    "Ref": "UtvonalValaszto"
  },
  "DestinationCidrBlock": "0.0.0.0/0",
  "GatewayId": {
    "Ref": "InternetKapcsolat"
  }
}
```

11. SubnetRouteTableAssociation: `SubnetUtvonalValasztoCsatolas`

```json
{
  "SubnetId": {
    "Ref": "FrontendSubnet"
  },
  "RouteTableId": {
    "Ref": "UtvonalValaszto"
  }
}
```

12. Security Group (SSH-22): `BiztonsagiCsoport`

```json
{
  "GroupDescription": "Allow SSH",
  "VpcId": {
    "Ref": "VirtualisHalozat"
  },
  "SecurityGroupIngress": [
    {
      "IpProtocol": "tcp",
      "FromPort": 22,
      "ToPort": 22,
      "CidrIp": "0.0.0.0/0"
    }
  ],
  "Tags": [
    {
      "Key": "Name",
      "Value": "mentor-klub"
    }
  ]
}
```

13. SSH KeyPair: `SSHKulcs`

```json
{
  "KeyName": {
    "Fn::Sub": "${AWS::StackName}-keypair-${AWS::Region}"
  }
}
```

14. Virtual Machine (EC2 instance): `VirtualisLinux`

```json
{
  "InstanceType": "t3.micro",
  "ImageId": "ami-015cbce10f839bd0c",
  "SubnetId": {
    "Ref": "FrontendSubnet"
  },
  "SecurityGroupIds": [
    {
      "Ref": "BiztonsagiCsoport"
    }
  ],
  "Tags": [
    {
      "Key": "Name",
      "Value": "mentor-klub"
    }
  ],
  "KeyName": {
    "Ref": "SSHKulcs"
  }
}
```

15. Erőforrások létrehozása ebből:

    - Kattints a "Create template" gombra.
    - Ekkor felugrik egy ablak, hogy tájékoztasson a sablon mentéséről.
    - Kattints a "Confirm and continue to CloudFormation" gombra. (ez elindítja a CloudFormation-t)
    - Válaszd a "Build from Infrastructure Composer" lehetőséget.
    - Kattints a "Next" gombra.
    - Add meg a Stack (deployment) nevét, majd kattints a "Next" gombra.
    - Következő lapon görgess a lap aljára, és kattints a "Next" gombra.
    - Az összegzés oldalon ellenőrizd a beállításokat, majd kattints a "Submit" gombra.
    - Kövesd figyelemmel az erőforrások létrehozását a CloudFormation konzolon.

16. Minden erőforrás sikeres létrehozása után ellenőrizd a CloudFormation stack állapotát.

## Virtuális gép ssh kulcs lekérdezése

1. Menjd az EC2 konzolra.
2. A bal oldalon keresd meg a "Key Pairs" menüpontot.
3. Keresd meg a létrehozott SSH kulcs nevét a listában, a Stack (deployment) nevének megfelelően.
4. Jegyezd fel a kulcs ID-t.(key-xxxxxxxx)
5. Nyiss egy cloud shell-t.
6. Exportáld a kulcsot:

```bash
KEY_NAME=mentor-klub-key
KEY_ID=key-01e1112d1afbeac2e
aws ssm get-parameter --name "/ec2/keypair/${KEY_ID}" --with-decryption --query 'Parameter.Value' --output text > ${KEY_NAME}.pem
chmod 400 ${KEY_NAME}.pem
```

7. Tölts le a saját gépedre.
   - CloudShell: Actions
   - Download file
   - Írd be a mezőbe: `/home/cloudshell-user/mentor-klub-key.pem`
8. Saját géppeden állítsd be a megfelelő jogosultságokat:

```bash
chmod 400 mentor-klub-key.pem
```

9. Jelentkezz be a virtuális gépre SSH-n keresztül:

```bash
ssh -i mentor-klub-key.pem ec2-user@<instance-public-ip>
```
