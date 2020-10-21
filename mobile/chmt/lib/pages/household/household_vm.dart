import 'package:chmt/model/model.dart';
import 'package:chmt/utils/utility.dart';
import 'package:chmt/view_model/base_vm.dart';
import 'package:flutter/material.dart';
import 'package:rxdart/rxdart.dart';

class HouseHoldViewModel extends BaseViewModel with ChangeNotifier {
  final _houseHold = BehaviorSubject<List<HouseHold>>();
  final _refresh = BehaviorSubject<bool>();

  Stream<List<HouseHold>> get houseHoldStream => _houseHold.stream;
  Stream<bool> get refreshStream => _refresh.stream;

  Function(bool) get refreshChanged => _refresh.sink.add;
  Function(List<HouseHold>) get houseHoldChanged => _houseHold.sink.add;

  List<HouseHold> get houseHoldList => _houseHold.value;

  void getHouseHoldList() {
    repo.getHouseHoldList().then((value) {
      var list = value.houseHolds;
      list.sort((a, b) => b.updateTime.compareTo(a.updateTime));
      houseHoldChanged(list);
    }).catchError((e) {
      logger.info(e);
      houseHoldChanged([]);
    });
  }

  @override
  void dispose() {
    super.dispose();
    _houseHold.close();
    _refresh.close();
  }
}
