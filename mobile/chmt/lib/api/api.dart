import 'package:chmt/model/model.dart';

abstract class API {
  Future<BaseResponse> getHouseHoldList({Map<String, dynamic> params});
  Future<BaseResponse> getProvinceList();
  Future<BaseResponse> getDistrictList();
  Future<BaseResponse> getCommuneList();
}