import 'package:chmt/model/model.dart';

abstract class API {
  Future<HouseHoldResponse> getHouseHoldList();
}

class APIPath {
  static String houseHold = r'hodan';
}