import 'package:chmt/model/model.dart';
import 'package:chmt/model/object_mapper/province.dart';
import 'package:chmt/utils/utility.dart';
import 'package:chmt/view_model/base_vm.dart';
import 'package:flutter/material.dart';
import 'package:rxdart/rxdart.dart';

class LoadAppViewModel extends BaseViewModel with ChangeNotifier {
  final _province = BehaviorSubject<List<Province>>();
  final _district = BehaviorSubject<List<District>>();
  final _commune = BehaviorSubject<List<Commune>>();

  Stream<List<Province>> get provinceStream => _province.stream;
  Function(List<Province>) get provinceChanged => _province.sink.add;
  List<Province> get provinceList => _province.value;

  Stream<List<District>> get districtStream => _district.stream;
  Function(List<District>) get districtChanged => _district.sink.add;
  List<District> get allDistrict => _district.value;

  Stream<List<Commune>> get communeStream => _commune.stream;
  Function(List<Commune>) get communeChanged => _commune.sink.add;
  List<Commune> get allCommune => _commune.value;

  Stream<bool> get loadingSuccess =>
      Rx.combineLatest3(provinceStream, districtStream, communeStream, (p, d, c) {
        return true;
      });

  LoadAppViewModel() {
    init();
  }

  void init() {
    getProvinceList();
    getDistrictList();
    getCommuneList();
  }

  void getProvinceList() {
    repo.getProvinceList().then((value) {
      var list = value.provinceList;
      list.sort((a, b) => a.id.compareTo(b.id));
      provinceChanged(list);
    }).catchError((e) {
      logger.info(e);
      provinceChanged([]);
    });
  }

  void getDistrictList() {
    repo.getDistrictList().then((value) {
      districtChanged(value.districtList);
    }).catchError((e) {
      logger.info(e);
      districtChanged([]);
    });
  }

  void getCommuneList() {
    repo.getCommuneList().then((value) {
      communeChanged(value.communeList);
    }).catchError((e) {
      logger.info(e);
      communeChanged([]);
    });
  }

  String getLandmark(RescueObject object) {
    var result = '';

    try {
      var province = provinceList.firstWhere((element) => element.id == object.province);
      var district = allDistrict.firstWhere((element) => element.id == object.district);
      var commune = allCommune.firstWhere((element) => element.id == object.commune);

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

  @override
  void dispose() {
    super.dispose();
    _province.close();
    _district.close();
    _commune.close();
  }
}
