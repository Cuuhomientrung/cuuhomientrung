
import 'package:chmt/utils/utility.dart';
import 'package:diacritic/diacritic.dart';

import 'household.dart';

class Rescuer implements RescueObject {
  int id, status;
  int _province, _district, _commune, village, volunteer, rescue;
  String name, location, phone, note;
  DateTime updateTime;

  int get province => _province ?? -1;
  int get district => _district ?? -1;
  int get commune => _commune ?? -1;

  String get searchText {
    String searchQuery = name + phone + getObject(location) + getObject(note);
    return removeDiacritics(searchQuery).toLowerCase();
  }

  String get phoneCall => 'tel:$phone';

  Rescuer.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    status = json['status'];
    name = json['name'];
    updateTime = DateTime.parse(json["update_time"]).toLocal();
    location = json['location'];
    phone = json['phone'];
    note = json['note'];
    _province = json[r'tinh'];
    _district = json[r'huyen'];
    _commune = json[r'xa'];
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
    r"tinh": _province,
    r"huyen": _district,
    "xa": _commune,
    r"thon": village,
    "volunteer": volunteer,
    r"cuuho": rescue,
  };
}
