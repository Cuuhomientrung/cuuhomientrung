import 'package:chmt/utils/utility.dart';
import 'package:diacritic/diacritic.dart';

class HouseHold {
  int id, status;
  int province, district, commune, village, volunteer, rescue;
  String name, location, phone, note;
  DateTime updateTime;

  String get searchText {
    String searchQuery = name + phone + getObject(location) + getObject(note);
    return removeDiacritics(searchQuery).toLowerCase();
  }

  String get phoneCall => 'tel:$phone';

  HouseHold.fromJson(Map json) {
    id = json['id'];
    status = json['status'];
    name = json['name'];
    updateTime = DateTime.parse(json["update_time"]).toLocal();
    location = json['location'];
    phone = json['phone'];
    note = json['note'];
    province = json[r'tinh'];
    district = json[r'huyen'];
    commune = json[r'xa'];
    village = json[r'thon'];
    volunteer = json[r'volunteer'];
    rescue = json[r'cuuho'];
  }

  Map<String, dynamic> toJson() => {
    "id": id,
    "name": name,
    "update_time": updateTime.toIso8601String(),
    "location": location,
    "status": status,
    "phone": phone,
    "note": note,
    "tinh": province,
    "huyen": district,
    "xa": commune,
    "thon": village,
    "volunteer": volunteer,
    "cuuho": rescue,
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
