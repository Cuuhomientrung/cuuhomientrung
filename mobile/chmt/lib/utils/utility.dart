import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
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

  static void showErrorDialog(BuildContext context,
      {String title = 'Đã xảy ra lỗi', String message, Function pressOK}) {
    showCupertinoDialog(
      context: context,
      builder: (BuildContext context) {
        return CupertinoAlertDialog(
          title: Text(
            title,
            style: GoogleFonts.roboto(
              fontWeight: FontWeight.w500,
              fontSize: 18,
            ),
          ),
          content: Padding(
            padding: const EdgeInsets.only(top: 5),
            child: Text(
              message,
              style: GoogleFonts.openSans(
                fontSize: 15,
                height: 1.3,
              ),
            ),
          ),
          actions: <Widget>[
            FlatButton(
              child: Text(
                r"Đồng ý",
                style: TextStyle(color: Colors.deepOrange),
              ),
              onPressed: () {
                Navigator.of(context).pop();
                if (pressOK != null) pressOK();
              },
            ),
          ],
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
      if (needShowDialog) showErrorDialog(context, message: errorMessage);
    }
  }
}
