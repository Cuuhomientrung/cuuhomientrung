import 'package:chmt/utils/utility.dart';
import 'package:diacritic/diacritic.dart';

abstract class RescueObject {
  int id, status;
  int _province, _district, _commune, village, volunteer, rescue;
  String name, location, phone, note;
  String _updateTime, _createTime;

  int get province => _province ?? -1;
  int get district => _district ?? -1;
  int get commune => _commune ?? -1;
}

extension RescueDateTime on RescueObject {
  DateTime get updateTime => DateTime.parse(_updateTime).toLocal();
  DateTime get createTime => DateTime.parse(_createTime).toLocal();
}

class HouseHold implements RescueObject {
  int id, status;
  int _province, _district, _commune, village, volunteer, rescue;
  String name, location, phone, note;
  String _updateTime, _createTime;

  int get province => _province ?? -1;
  int get district => _district ?? -1;
  int get commune => _commune ?? -1;

  String get searchText {
    String searchQuery = name + phone + getObject(location) + getObject(note);
    return removeDiacritics(searchQuery).toLowerCase();
  }

  void setUpdateTime(DateTime dateTime) {
    _updateTime = dateTime.toIso8601String();
  }

  String get phoneCall => 'tel:$phone';

  HouseHold.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    status = json['status'];
    name = json['name'];
    _updateTime = json["update_time"];
    _createTime = json["created_time"];
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
    "created_time": createTime.toIso8601String(),
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

/*
{
    "id": 93,
    "name": "",
    "update_time": "2020-10-19T17:36:29.638323+07:00",
    "created_time": "2020-10-23T14:41:05.495936+07:00",
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
