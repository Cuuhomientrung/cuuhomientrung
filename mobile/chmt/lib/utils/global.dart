import 'package:chmt/model/model.dart';
import 'package:chmt/utils/utility.dart';

class AppGlobal {
  AppGlobal._();

  static final shared = AppGlobal._();

  static const baseUrl = r'https://cuuhomientrung.info/';

  List<Province> provinceList = [];
  List<District> districtList = [];
  List<Commune> communeList = [];

  String getAddress(HouseHold houseHold) {
    var result = '';

    try {
      var province = provinceList.firstWhere((element) => element.id == houseHold.province);
      var district = districtList.firstWhere((element) => element.id == houseHold.district);
      var commune = communeList.firstWhere((element) => element.id == houseHold.commune);

      if (province != null) {
        result += province.name + ', ';
      }

      if (district != null) {
        result += district.name + ', ';
      }

      if (commune != null) {
        result += commune.name;
      }
    } catch (e) {
      logger.info(e);
    }

    return result;
  }
}