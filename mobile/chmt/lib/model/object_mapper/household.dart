
import 'package:chmt/utils/utility.dart';
import 'package:diacritic/diacritic.dart';

class HouseHoldResponse {
  List data;

  HouseHoldResponse({this.data});

  List<HouseHold> get houseHolds =>
      data.map((e) => HouseHold.fromJson(e))
          .toList();
}

class HouseHold {
  int id, status;
  int tinh, huyen, xa, thon, volunteer, cuuho;
  String name, location, phone, note;
  DateTime updateTime;

  String get searchText {
    String searchQuery = name + phone + getObject(location) + getObject(note);
    return removeDiacritics(searchQuery).toLowerCase();
  }

  HouseHold.fromJson(Map json) {
    id = json['id'];
    status = json['status'];
    name = json['name'];
    updateTime = DateTime.parse(json["update_time"]).toLocal();
    location = json['location'];
    phone = json['phone'];
    note = json['note'];
    tinh = json[r'tinh'];
    huyen = json[r'huyen'];
    xa = json[r'xa'];
    thon = json[r'thon'];
    volunteer = json[r'volunteer'];
    cuuho = json[r'cuuho'];
  }

  Map<String, dynamic> toJson() => {
    "id": id,
    "name": name,
    "update_time": updateTime.toIso8601String(),
    "location": location,
    "status": status,
    "phone": phone,
    "note": note,
    "tinh": tinh,
    "huyen": huyen,
    "xa": xa,
    "thon": thon,
    "volunteer": volunteer,
    "cuuho": cuuho,
  };
}

/*
{
    "id": 93,
    "name": "",
    "update_time": "2020-10-19T17:36:29.638323+07:00",
    "location": "",
    "status": 0,
    "phone": "",
    "note": "",
    "tinh": null,
    "huyen": null,
    "xa": null,
    "thon": null,
    "volunteer": null,
    "cuuho": null
}*/
