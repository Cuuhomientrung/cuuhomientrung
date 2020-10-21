import 'package:chmt/api/api_method.dart';
import 'package:chmt/model/model.dart';

import 'api.dart';

class RemoteAPI implements API {
  RemoteAPI._();

  static final shared = RemoteAPI._();

  @override
  Future<BaseResponse> getHouseHoldList({Map<String, dynamic> params}) async {
    try {
      var res = await APIMethod.getData(APIPath.houseHold, params);
      return BaseResponse(data: res as List);
    } catch (e) {
      throw e;
    }
  }

  @override
  Future<BaseResponse> getCommuneList() async {
    try {
      var res = await APIMethod.getData(APIPath.commune, {});
      return BaseResponse(data: res as List);
    } catch (e) {
      throw e;
    }
  }

  @override
  Future<BaseResponse> getDistrictList() async {
    try {
      var res = await APIMethod.getData(APIPath.district, {});
      return BaseResponse(data: res as List);
    } catch (e) {
      throw e;
    }
  }

  @override
  Future<BaseResponse> getProvinceList() async {
    try {
      var res = await APIMethod.getData(APIPath.province, {});
      return BaseResponse(data: res as List);
    } catch (e) {
      throw e;
    }
  }
}
