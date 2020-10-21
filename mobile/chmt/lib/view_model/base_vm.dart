import 'package:chmt/api/api.dart';
import 'package:chmt/api/remote_api.dart';
import 'package:rxdart/rxdart.dart';

abstract class BaseViewModel {
  final BehaviorSubject<dynamic> _error = BehaviorSubject();

  Sink<dynamic> get error => _error.sink;

  Stream<dynamic> get errorStream => _error.stream;

  Function(dynamic) get errorEvent => _error.sink.add;

//  final API repo = MockAPI.shared;
  final API repo = RemoteAPI.shared;

  void dispose() {
    _error.close();
  }
}