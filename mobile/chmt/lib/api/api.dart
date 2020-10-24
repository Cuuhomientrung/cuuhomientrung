import 'package:chmt/model/model.dart';

abstract class API {
  Future<BaseResponse> getHouseHoldList({Map<String, dynamic> params});
  Future<BaseResponse> getProvinceList();
  Future<BaseResponse> getDistrictList();
  Future<BaseResponse> getCommuneList();
  Future<BaseResponse> getRescuerList({Map<String, dynamic> params});
  Future<HouseHold> updateHouseHold({HouseHold item});
  Future<dynamic> deleteHouseHold({HouseHold item});
}