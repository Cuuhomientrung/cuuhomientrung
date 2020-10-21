import 'package:chmt/model/model.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:chmt/model/status.dart';

class RescuerItemView extends StatelessWidget {
  const RescuerItemView({
    Key key,
    this.item,
    this.animationController,
    this.animation,
    this.phoneCallback,
    this.callback,
    this.statusCallback,
    this.deleteCallback,
    this.address = '',
  }) : super(key: key);

  final VoidCallback callback;
  final VoidCallback statusCallback;
  final VoidCallback phoneCallback;
  final VoidCallback deleteCallback;
  final Rescuer item;
  final AnimationController animationController;
  final Animation<dynamic> animation;
  final String address;

  @override
  Widget build(BuildContext context) {
    Color color = Color(0xFF01477f);

    var textStyle = GoogleFonts.roboto(
        color: color, fontWeight: FontWeight.w400, fontSize: 14.5);
    var subStyle = GoogleFonts.roboto(
      fontSize: 15,
      fontWeight: FontWeight.w400,
      color: Color(0xff797878),
    );

    List<Widget> columnContent = [
      Container(
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Expanded(
              child: TitleText(
                text: '${item.name}',
                fontSize: 20,
                color: color,
              ),
            ),
            SizedBox(width: 5),
            Padding(
              padding: EdgeInsets.only(top: 2.5),
              child: GestureDetector(
                onTap: () => statusCallback(),
                child: StatusView(
                  status: '${item.status.rescuerStatus}',
                  color: item.status.rescuerColor,
                ),
              ),
            )
          ],
        ),
      ),
      SizedBox(height: 5),
      Divider(height: 1),
      SizedBox(height: 10),
      GestureDetector(
        onTap: () => phoneCallback(),
        child: RichText(
          text: TextSpan(
            text: r"Điện thoại: ",
            style: subStyle,
            children: <TextSpan>[
              TextSpan(
                text: '${item.phone}',
                style: GoogleFonts.roboto(
                  color: Colors.blue,
                  fontWeight: FontWeight.w500,
                  fontSize: 15,
                ),
              ),
            ],
          ),
        ),
      ),
      SizedBox(height: 5),
      RichText(
        text: TextSpan(
          text: r'Phạm vi cứu hộ: ',
          style: subStyle,
          children: <TextSpan>[
            TextSpan(
              text: '${item.location}',
              style: textStyle,
            ),
          ],
        ),
      ),
      SizedBox(height: 5),
      RichText(
        text: TextSpan(
          text: r'Địa chỉ: ',
          style: subStyle,
          children: <TextSpan>[
            TextSpan(
              text: '$address',
              style: textStyle,
            ),
          ],
        ),
      ),
      SizedBox(height: 5),
      RichText(
        text: TextSpan(
          text: r"Ngày cập nhật: ",
          style: subStyle,
          children: <TextSpan>[
            TextSpan(
              text: '${DateFormat('dd/MM/yy HH:mm').format(item.updateTime)}',
              style: GoogleFonts.roboto(
                color: color,
                fontWeight: FontWeight.w500,
                fontSize: 15,
              ),
            ),
          ],
        ),
      )
    ];

    return AnimatedBuilder(
      animation: animationController,
      builder: (BuildContext context, Widget child) {
        return FadeTransition(
          opacity: animation,
          child: Transform(
            transform: Matrix4.translationValues(
                0.0, 50 * (1.0 - animation.value), 0.0),
            child: Padding(
              padding:
              const EdgeInsets.only(left: 16, right: 16, top: 8, bottom: 8),
              child: Container(
                decoration: BoxDecoration(
                  color: Color(0xFFFEFEFE),
                  borderRadius: const BorderRadius.all(Radius.circular(8.0)),
                  boxShadow: <BoxShadow>[
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.4),
                      offset: Offset.zero,
                      blurRadius: 8,
                    ),
                  ],
                ),
                child: Material(
                  color: Colors.transparent,
                  child: InkWell(
                    highlightColor: Colors.transparent,
                    splashColor:
                    Color.fromRGBO(129, 199, 245, 1).withAlpha(120),
                    borderRadius: BorderRadius.all(Radius.circular(8.0)),
                    onTap: () {
                      callback();
                    },
                    child: Padding(
                      padding: EdgeInsets.fromLTRB(16, 10, 16, 10),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.max,
                        children: columnContent,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}

class TitleText extends StatelessWidget {
  final String text;
  final double fontSize;
  final Color color;
  final FontWeight fontWeight;

  const TitleText(
      {Key key,
        this.text,
        this.fontSize = 18,
        this.color,
        this.fontWeight = FontWeight.w600})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: GoogleFonts.roboto(
        fontSize: fontSize,
        fontWeight: fontWeight,
        color: color ?? Color(0xff797878),
      ),
    );
  }
}

class StatusView extends StatelessWidget {
  final String status;
  final Color color;
  final EdgeInsets padding;

  const StatusView({@required this.status, this.color, this.padding});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
          color: color,
          borderRadius: const BorderRadius.all(Radius.circular(3.0)),
          border: Border.all(width: .7, color: color)),
      padding: padding ?? EdgeInsets.fromLTRB(3, 2, 3, 1.5),
      child: Text(
        status,
        style: GoogleFonts.roboto(
          color: Colors.white,
          fontWeight: FontWeight.normal,
          fontSize: 11,
        ),
      ),
    );
  }
}
