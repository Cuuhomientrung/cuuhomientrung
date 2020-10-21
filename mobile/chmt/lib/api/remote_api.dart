import 'package:chmt/api/api_method.dart';
import 'package:chmt/model/model.dart';

import 'api.dart';

class RemoteAPI implements API {
  RemoteAPI._();

  static final shared = RemoteAPI._();

  @override
  Future<HouseHoldResponse> getHouseHoldList() async {
    try {
      var res = await APIMethod.getData(APIPath.houseHold, {});
      return HouseHoldResponse(data: res as List);
    } catch (e) {
      throw e;
    }
  }
}
