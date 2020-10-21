import 'package:chmt/utils/utility.dart';
import 'package:chmt/view_model/base_vm.dart';

class HouseHoldViewModel extends BaseViewModel {

  void getHouseHoldList() {
    repo.getHouseHoldList().then((value) {
      logger.info(value);
    }).catchError((e) => logger.info(e));
  }
}