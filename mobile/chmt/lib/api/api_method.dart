import 'dart:convert';

import 'package:chmt/utils/utility.dart';
import 'package:connectivity/connectivity.dart';
import 'package:dio/dio.dart';

class APIMethod {
  static Dio _dio = APIMethod.dioClient();

  static Dio dioClient() {
    Dio dio = Dio();
    dio.options.baseUrl = 'https://cuuhomientrung.info/api/app/';
    dio.options.receiveTimeout = 20000;
    dio.options.connectTimeout = 20000;
    dio.options.contentType = "application/json";
    return dio;
  }

  static String getRawJson(dynamic rawJSON) {
    return json.decode(rawJSON.toString()).toString()
        .replaceAll("\n", "\\n")
        .replaceAll("\t", "\\t")
        .replaceAll("\r", "\\r");
  }

  //GET
  static Future<dynamic> getData(
      String path, Map<String, dynamic> params) async {
    logger.info('>>>$path<<< PARAMS: $params');

    try {
      var connectivityResult = await (Connectivity().checkConnectivity());
      if (connectivityResult == ConnectivityResult.none) {
        throw r'Không có kết nối mạng';
      }

      var res = await _dio.get(path, queryParameters: params);
      logger.info(res.data);
      return (res.data);
    } catch (e) {
      throw e;
    }
  }

  /// POST
  static Future<dynamic> postData(String path, Map params) async {
    logger.info('>>>$path<<< PARAMS: $params');

    try {
      var connectivityResult = await (Connectivity().checkConnectivity());
      if (connectivityResult == ConnectivityResult.none) {
        throw r'Không có kết nối mạng';
      }

      var res = await _dio.post(path, data: params);

      logger.info('>>>$path<<< RESPONSE: ${res.data}');

      return (res.data);
    } catch (e) {
      throw e;
    }
  }
}
