import 'package:simple_logger/simple_logger.dart';

getObject(dynamic object, {String orNull = ''}) => object ?? orNull;

final SimpleLogger logger = SimpleLogger()
  ..mode = LoggerMode.print
  ..setLevel(Level.FINEST, includeCallerInfo: true);