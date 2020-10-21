import 'package:chmt/model/model.dart';

class BaseResponse {
  List data;

  BaseResponse({this.data});

  List<HouseHold> get houseHolds =>
      data.map((e) => HouseHold.fromJson(e)).toList();

  List<Province> get provinceList =>
      data.map((e) => Province.fromJson(e)).toList();

  List<District> get districtList =>
      data.map((e) => District.fromJson(e)).toList();

  List<Commune> get communeList =>
      data.map((e) => Commune.fromJson(e)).toList();

  List<Rescuer> get rescuerList =>
      data.map((e) => Rescuer.fromJson(e)).toList();
}
