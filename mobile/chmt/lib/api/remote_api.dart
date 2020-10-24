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

  @override
  Future<BaseResponse> getRescuerList({Map<String, dynamic> params}) async {
    try {
      var res = await APIMethod.getData(APIPath.rescuer, params);
      return BaseResponse(data: res as List);
    } catch (e) {
      throw e;
    }
  }

  @override
  Future<HouseHold> updateHouseHold({HouseHold item}) async {
    try {
      var res = await APIMethod.putData(
              APIPath.houseHold + '${item.id}/', item.toJson())
          .then((v) => Map<String, dynamic>.from(v));
      return HouseHold.fromJson(res);
    } catch (e) {
      throw e;
    }
  }

  @override
  Future<String> deleteHouseHold({HouseHold item}) async {
    try {
      return await APIMethod.delete(
          APIPath.houseHold + '${item.id}/', item.toJson())
          .then((v) => v.toString());
    } catch (e) {
      throw e;
    }
  }
}
