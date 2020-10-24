import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:loading_indicator/loading_indicator.dart';
import 'package:simple_logger/simple_logger.dart';
import 'package:url_launcher/url_launcher.dart';

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

  static Widget centerLoadingIndicator({double size = 64}) => Center(
        child: Container(
          width: size,
          height: size,
          child: LoadingIndicator(
            indicatorType: Indicator.ballClipRotateMultiple,
            color: Colors.blue,
          ),
        ),
      );

  static Future<bool> showConfirmDialog(
    BuildContext context, {
    String title = r'Xác nhận',
    String message = '',
    Widget child,
    String okTitle = r'Đồng ý',
    String cancelTitle = 'Bỏ qua',
    bool showCancelButton = true,
    Function onPressedOK,
    Function onPressCancel,
  }) {
    var okAction = FlatButton(
      child: Text(
        okTitle,
        style: TextStyle(color: Colors.deepOrange),
      ),
      onPressed: () {
        Navigator.of(context).pop();
        if (onPressedOK != null) {
          onPressedOK();
        }
      },
    );
    var cancelAction = FlatButton(
      child: Text(
        cancelTitle,
        style: TextStyle(color: Colors.blueGrey),
      ),
      onPressed: () {
        Navigator.of(context).pop();
        if (onPressCancel != null) {
          onPressCancel();
        }
      },
    );

    var actions = showCancelButton ? [cancelAction, okAction] : [okAction];

    return showCupertinoDialog<bool>(
      context: context,
      builder: (BuildContext context) {
        return CupertinoAlertDialog(
          title: Text(
            title,
            style: GoogleFonts.merriweather(
              fontWeight: FontWeight.w500,
              fontSize: 18,
            ),
          ),
          content: Padding(
            padding: EdgeInsets.only(top: 5),
            child: Column(
              children: [
                Text(
                  message,
                  style: GoogleFonts.lato(
                    fontSize: 15,
                  ),
                ),
                child ?? SizedBox()
              ],
            ),
          ),
          actions: actions,
        );
      },
    );
  }

  static launchURL(BuildContext context,
      {String url = '',
      String errorMessage = 'Can not open url',
      bool needShowDialog = true}) async {
    logger.info('Open url: $url');

    if (await canLaunch(url)) {
      await launch(url);
    } else {
      if (needShowDialog)
        showConfirmDialog(
          context,
          message: errorMessage,
          title: r'Đã xảy ra lỗi',
          showCancelButton: false,
        );
    }
  }

  static showLoading(BuildContext context, String msg,
          {Indicator type = Indicator.ballClipRotateMultiple,
          Color color = Colors.white}) =>
      showDialog(
        barrierDismissible: false,
        context: context,
        builder: (context) => _createLoading(context, msg, type, color),
      );

  static _createLoading(
      BuildContext context, String msg, Indicator type, Color color) {
    Size size = MediaQuery.of(context).size;
    return Center(
      child: Container(
        width: size.width * 0.7,
        height: size.height * 0.7,
        child: Stack(
          children: <Widget>[
            Align(
              alignment: Alignment.center,
              child: LoadingIndicator(indicatorType: type, color: color),
            ),
            Align(
              alignment: Alignment.center,
              child: Text(
                msg ?? '',
                style: GoogleFonts.roboto(
                  color: Colors.white,
                  fontSize: 17,
                  decoration: TextDecoration.none,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
