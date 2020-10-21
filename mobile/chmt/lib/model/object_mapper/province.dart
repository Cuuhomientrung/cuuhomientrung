
abstract class AddressItem {
  int id, parentID;
  String name;
}

/// Tỉnh
class Province implements AddressItem {
  int id, parentID;
  String name;

  Province.fromJson(Map json)
      : id = json["id"],
        name = json['name'];
}

/// Huyện
class District implements AddressItem {
  int id, parentID;
  String name;

  District.fromJson(Map json)
      : id = json["id"],
        name = json['name'],
        parentID = json[r'tinh'];
}

/*
{
    "id": 33,
    "name": "Huyện Can Lộc",
    "tinh": 4
}*/

/// Xã
class Commune implements Province {
  int id, parentID;
  String name;

  Commune.fromJson(Map json)
      : id = json["id"],
        name = json['name'],
        parentID = json[r'huyen'];
}

/*
{
  "id": 443,
  "name": "Phường Ba Đồn",
  "huyen": 108
}*/