import 'package:chmt/utils/utility.dart';
import 'package:connectivity/connectivity.dart';
import 'package:dio/dio.dart';

class APIPath {
  static String houseHold = r'hodan/';
}

class APIMethod {
  static Dio _dio = APIMethod.dioClient();

  static String baseUrl = 'https://cuuhomientrung.info/api/app/';

  static Dio dioClient() {
    Dio dio = Dio();
    dio.options.baseUrl = baseUrl;
    dio.options.receiveTimeout = 20000;
    dio.options.connectTimeout = 20000;
    return dio;
  }

  /// GET
  static Future<dynamic> getData(
      String subPath, Map<String, dynamic> params) async {
    logger.info('>>>$subPath<<< PARAMS: $params');

    try {
      var connectivityResult = await (Connectivity().checkConnectivity());
      if (connectivityResult == ConnectivityResult.none) {
        throw r'Không có kết nối mạng';
      }

      Response res = await _dio.get(subPath, queryParameters: params);
      logger.info(res.data);
      return (res.data);
    } catch (e) {
      throw e;
    }
  }

  /// POST
  static Future<dynamic> postData(String subPath, Map params) async {
    logger.info('>>>$subPath<<< PARAMS: $params');

    try {
      var connectivityResult = await (Connectivity().checkConnectivity());
      if (connectivityResult == ConnectivityResult.none) {
        throw r'Không có kết nối mạng';
      }

      Response res = await _dio.post(subPath, data: params);

      logger.info('>>>$subPath<<< RESPONSE: ${res.data}');

      return (res.data);
    } catch (e) {
      throw e;
    }
  }
}
