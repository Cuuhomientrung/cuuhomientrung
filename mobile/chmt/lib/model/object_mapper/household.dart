class HouseHoldResponse {
  List data;

  HouseHoldResponse({this.data});

  List<HouseHold> get houseHolds =>
      data.map((e) => HouseHold.fromJson(e)).toList();
}

class HouseHold {
  int id, status;
  int tinh, huyen, xa, thon, volunteer, cuuho;
  String name, updateTime, location, phone, note;

  HouseHold.fromJson(Map e, {Map json}) {
    id = json['id'];
    status = json['status'];
    name = json['name'];
    updateTime = json['update_time'];
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
