import 'package:flutter/material.dart';

extension HODAN_STATUS on int {
  String get statusString {
    switch (this) {
      case 0: return r'Chưa xác minh';
      case 1: return r'Cần ứng cứu gấp';
      case 2: return r'Không gọi được';
      case 3: return r'Đã được cứu';
      case 4: return r'Gặp nạn';
      default: return r'Chưa xác minh';
    }
  }

  Color get statusColor {
    switch (this) {
      case 0: return Colors.blueGrey;
      case 1: return Colors.deepPurple;
      case 2: return Colors.orange;
      case 3: return Colors.green;
      case 4: return Colors.red;
      default: return Colors.white;
    }
  }

  String get rescuerStatus {
    switch (this) {
      case 0: return r'Chưa xác minh';
      case 1: return r'Sẵn sàng';
      case 2: return r'Không gọi được';
      case 3: return r'Đang cứu hộ';
      case 4: return r'Đang nghỉ';
      default: return r'Chưa xác minh';
    }
  }

  Color get rescuerColor {
    switch (this) {
      case 0: return Colors.blueGrey;
      case 1: return Colors.green;
      case 2: return Colors.red;
      case 3: return Colors.lime;
      case 4: return Colors.orange;
      default: return Colors.white;
    }
  }
}