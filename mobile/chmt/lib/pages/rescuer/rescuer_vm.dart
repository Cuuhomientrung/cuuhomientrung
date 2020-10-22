import 'package:chmt/model/model.dart';
import 'package:chmt/pages/household/household_vm.dart';
import 'package:chmt/utils/utility.dart';
import 'package:rxdart/rxdart.dart';

class RescuerViewModel extends HouseHoldViewModel {
  final _rescuer = BehaviorSubject<List<Rescuer>>();

  Stream<List<Rescuer>> get rescuerStream => _rescuer.stream;
  Function(List<Rescuer>) get rescuerChanged => _rescuer.sink.add;
  List<Rescuer> get rescuerList => _rescuer.value;

  RescuerViewModel() {
    init();
  }

  void getRescuerList() {
    Map<String, dynamic> params = {
      r'tinh': selectedProvince != null ? selectedProvince.id : null,
      r'huyen': selectedDistrict != null ? selectedDistrict.id : null,
      r'xa': selectedCommune != null ? selectedCommune.id : null,
      r'status': status != null ? status : null,
    };

    params.removeWhere((key, value) => value == null);

    repo.getRescuerList(params: params).then((value) {
      var list = value.rescuerList;
      list.sort((a, b) => b.updateTime.compareTo(a.updateTime));
      rescuerChanged(list);
    }).catchError((e) {
      logger.info(e);
      rescuerChanged([]);
    });
  }

  @override
  void dispose() {
    super.dispose();
    _rescuer.close();
  }
}