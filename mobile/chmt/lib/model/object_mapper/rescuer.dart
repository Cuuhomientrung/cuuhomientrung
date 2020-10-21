
import 'package:chmt/utils/utility.dart';
import 'package:diacritic/diacritic.dart';

class Rescuer {
  Rescuer({
    this.id,
    this.updateTime,
    this.name,
    this.status,
    this.location,
    this.phone,
    this.note,
    this.tinh,
    this.huyen,
    this.xa,
    this.thon,
    this.volunteer,
  });

  int id;
  DateTime updateTime;
  String name;
  int status;
  String location;
  String phone;
  String note;
  int tinh;
  int huyen;
  int xa;
  int thon;
  int volunteer;

  String get searchText {
    String searchQuery = name + phone + getObject(location) + getObject(note);
    return removeDiacritics(searchQuery).toLowerCase();
  }

  String get phoneCall => 'tel:$phone';

  factory Rescuer.fromJson(Map<String, dynamic> json) => Rescuer(
    id: json["id"],
    updateTime: DateTime.parse(json["update_time"]),
    name: json["name"],
    status: json["status"],
    location: json["location"],
    phone: json["phone"],
    note: json["note"],
    tinh: json["tinh"] == null ? null : json["tinh"],
    huyen: json["huyen"] == null ? null : json["huyen"],
    xa: json["xa"] == null ? null : json["xa"],
    thon: json["thon"] == null ? null : json["thon"],
    volunteer: json["volunteer"] == null ? null : json["volunteer"],
  );

  Map<String, dynamic> toJson() => {
    "id": id,
    "update_time": updateTime.toIso8601String(),
    "name": name,
    "status": status,
    "location": location,
    "phone": phone,
    "note": note,
    "tinh": tinh == null ? null : tinh,
    "huyen": huyen == null ? null : huyen,
    "xa": xa == null ? null : xa,
    "thon": thon == null ? null : thon,
    "volunteer": volunteer == null ? null : volunteer,
  };
}
