import 'package:chmt/model/model.dart';
import 'package:chmt/model/object_mapper/province.dart';
import 'package:chmt/utils/utility.dart';
import 'package:chmt/view_model/base_vm.dart';
import 'package:flutter/material.dart';
import 'package:rxdart/rxdart.dart';

class HouseHoldViewModel extends BaseViewModel with ChangeNotifier {
  final _houseHold = BehaviorSubject<List<HouseHold>>();
  final _province = BehaviorSubject<List<Province>>();
  final _district = BehaviorSubject<List<District>>();
  final _commune = BehaviorSubject<List<Commune>>();
  final _refresh = BehaviorSubject<bool>();

  final _selectedProvince = BehaviorSubject<Province>();
  final _selectedDistrict = BehaviorSubject<District>();
  final _selectedCommune = BehaviorSubject<Commune>();

  Stream<List<HouseHold>> get houseHoldStream => _houseHold.stream;
  Stream<bool> get refreshStream => _refresh.stream;

  Function(bool) get refreshChanged => _refresh.sink.add;
  Function(List<HouseHold>) get houseHoldChanged => _houseHold.sink.add;

  List<HouseHold> get houseHoldList => _houseHold.value;

  Stream<List<Province>> get provinceStream => _province.stream;
  Function(List<Province>) get provinceChanged => _province.sink.add;
  List<Province> get provinceList => _province.value;

  Stream<List<District>> get districtStream => _district.stream;
  Function(List<District>) get districtChanged => _district.sink.add;
  List<District> get districtList {
   if (selectedProvince == null) {
     return [];
   } else {
     return _district.value.where((e) => e.parentID == selectedProvince.id).toList();
   }
  }

  Stream<List<Commune>> get communeStream => _commune.stream;
  Function(List<Commune>) get communeChanged => _commune.sink.add;
  List<Commune> get communeList {
    if (selectedDistrict == null) {
      return [];
    } else {
      return _commune.value.where((e) => e.parentID == selectedDistrict.id).toList();
    }
  }

  Stream<Commune> get selectedCommuneStream => _selectedCommune.stream;
  Function(Commune) get selectedCommuneChanged => _selectedCommune.sink.add;
  Commune get selectedCommune => _selectedCommune.value;

  Stream<District> get selectedDistrictStream => _selectedDistrict.stream;
  Function(District) get selectedDistrictChanged => _selectedDistrict.sink.add;
  District get selectedDistrict => _selectedDistrict.value;

  Stream<Province> get selectedProvinceStream => _selectedProvince.stream;
  Function(Province) get selectedProvinceChanged => _selectedProvince.sink.add;
  Province get selectedProvince => _selectedProvince.value;

  HouseHoldViewModel() {
    getProvinceList();
    getDistrictList();
    getCommuneList();
  }

  void reset() {
    selectedProvinceChanged(null);
    selectedDistrictChanged(null);
    selectedCommuneChanged(null);
  }

  void getHouseHoldList() {
    Map<String, dynamic> params = {
      r'tinh': selectedProvince != null ? selectedProvince.id : null,
      r'huyen': selectedDistrict != null ? selectedDistrict.id : null,
      r'xa': selectedCommune != null ? selectedCommune.id : null,
    };

    params.removeWhere((key, value) => value == null);

    repo.getHouseHoldList(params: params).then((value) {
      var list = value.houseHolds;
      list.sort((a, b) => b.updateTime.compareTo(a.updateTime));
      houseHoldChanged(list);
    }).catchError((e) {
      logger.info(e);
      houseHoldChanged([]);
    });
  }
  
  String getAddress(HouseHold houseHold) {
    var result = '';
    
    var province = provinceList.firstWhere((element) => element.id == houseHold.province);
    
    return result;
  }

  void getProvinceList() {
    repo.getProvinceList().then((value) {
      provinceChanged(value.provinceList);
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

  @override
  void dispose() {
    super.dispose();
    _houseHold.close();
    _refresh.close();
    _province.close();
    _district.close();
    _commune.close();
    _selectedProvince.close();
    _selectedDistrict.close();
    _selectedCommune.close();
  }
}
