import 'package:chmt/model/model.dart';

abstract class API {
  Future<HouseHoldResponse> getHouseHoldList();
}