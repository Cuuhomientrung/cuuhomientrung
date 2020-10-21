import 'package:flutter/material.dart';
import 'package:simple_logger/simple_logger.dart';

getObject(dynamic object, {String orNull = ''}) => object ?? orNull;

final SimpleLogger logger = SimpleLogger()
  ..mode = LoggerMode.print
  ..setLevel(Level.FINEST, includeCallerInfo: true);

class Utility {
  static hideKeyboardOf(BuildContext context) {
    // FocusScope.of(context).requestFocus(FocusNode());
    FocusScopeNode currentFocus = FocusScope.of(context);

    if (!currentFocus.hasPrimaryFocus) {
      currentFocus.unfocus();
    }
  }
}