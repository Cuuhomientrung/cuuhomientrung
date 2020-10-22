import 'package:chmt/utils/global.dart';
import 'package:chmt/utils/utility.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

enum DrawerIndex {
  News,
  RescuerTeam,
  HouseHold,
}

class DrawerList {
  String labelName;
  Icon icon;
  bool isAssetsImage;
  String imageName;
  DrawerIndex index;

  DrawerList({
    this.isAssetsImage = false,
    this.labelName = '',
    this.icon,
    this.index,
    this.imageName = '',
  });
}

class HomeDrawer extends StatefulWidget {
  final AnimationController iconAnimationController;
  final DrawerIndex screenIndex;
  final Function(DrawerIndex) callBackIndex;

  HomeDrawer({
    Key key,
    this.screenIndex,
    this.iconAnimationController,
    this.callBackIndex,
  }) : super(key: key);

  @override
  _HomeDrawerState createState() => _HomeDrawerState();
}

class _HomeDrawerState extends State<HomeDrawer> {
  List<DrawerList> drawerList;
  int notice = 0;

  @override
  void initState() {
    initDrawerList();
    super.initState();
  }

  void initDrawerList() {
    drawerList = [
      DrawerList(
        index: DrawerIndex.HouseHold,
        labelName: r'Các hộ cần ứng cứu',
        icon: Icon(Icons.home),
      ),
      DrawerList(
        index: DrawerIndex.RescuerTeam,
        labelName: r'Các đội cứu hộ',
        icon: Icon(Icons.security),
      ),
      DrawerList(
        index: DrawerIndex.News,
        labelName: r'Tin tức',
        icon: Icon(Icons.extension),
      ),
    ];
  }

  void navigateToScreen(DrawerIndex screenIndex) async {
    widget.callBackIndex(screenIndex);
  }

  @override
  Widget build(BuildContext context) {
    double avatarSize = 54;

    var userWidget = Container(
      width: double.infinity,
      padding: EdgeInsets.only(top: MediaQuery.of(context).padding.top),
      child: Container(
        padding: EdgeInsets.only(left: 10, top: 10, bottom: 16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            AnimatedBuilder(
              animation: widget.iconAnimationController,
              builder: (BuildContext context, Widget child) {
                return ScaleTransition(
                  scale: AlwaysStoppedAnimation(
                      1.0 - (widget.iconAnimationController.value) * 0.2),
                  child: RotationTransition(
                    turns: AlwaysStoppedAnimation(Tween(begin: 0.0, end: 24.0)
                        .animate(CurvedAnimation(
                        parent: widget.iconAnimationController,
                        curve: Curves.fastOutSlowIn))
                        .value /
                        360),
                    child: GestureDetector(
                      onTap: () {},
                      child: Container(
                        height: avatarSize,
                        width: avatarSize,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          boxShadow: <BoxShadow>[
                            BoxShadow(
                                color: Color(0xFFa8edea).withOpacity(0.33),
                                offset: Offset(3.0, 3.0),
                                blurRadius: 10),
                          ],
                          border: Border.all(
                            color: Colors.white,
                            width: 1.3,
                          ),
                        ),
                        child: ClipRRect(
                          borderRadius: BorderRadius.all(Radius.circular(60)),
                          child: Image.asset("assets/logo.png"),
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
            SizedBox(height: 10),
            Expanded(
              child: GestureDetector(
                onTap: () => Utility.launchURL(context, url: AppGlobal.baseUrl),
                child: Container(
                  padding: EdgeInsets.only(left: 10, top: 5, right: 8),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Container(
//                        width: calculateUserWidgetWidth,
                        child: Text(
                          r'Cứu hộ miền Trung'.toUpperCase(),
                          maxLines: 2,
                          overflow: TextOverflow.fade,
                          textAlign: TextAlign.left,
                          softWrap: false,
                          style: GoogleFonts.merriweather(
                            fontSize: 16.0,
                            fontWeight: FontWeight.w600,
                            letterSpacing: 0.05,
                            color: Colors.blue,
                          ),
                        ),
                      ),
                      Container(
//                        width: calculateUserWidgetWidth,
                        child: Text(
                          r'cuuhomientrung.info',
                          overflow: TextOverflow.fade,
                          style: GoogleFonts.lato(
                            fontSize: 13.0,
                            fontWeight: FontWeight.w500,
                            color: Color(0xFF01477f),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );

    return Scaffold(
      backgroundColor: Color(0xFFF2F3F8),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        mainAxisAlignment: MainAxisAlignment.start,
        children: <Widget>[
          userWidget,
          Divider(
            height: 1,
          ),
          Expanded(
            child: ListView.builder(
              physics: BouncingScrollPhysics(),
              padding: EdgeInsets.all(0.0),
              itemCount: drawerList.length,
              itemBuilder: (context, index) {
                return inkwell(drawerList[index]);
              },
            ),
          ),
          Divider(
            height: 1,
          ),
          Column(
            children: <Widget>[
              Material(
                color: Colors.transparent,
                child: InkWell(
                  splashColor: Colors.grey.withOpacity(0.1),
                  highlightColor: Colors.transparent,
                  onTap: () => Utility.launchURL(context, url: AppGlobal.baseUrl),
                  child: Stack(
                    children: <Widget>[
                      Container(
                        padding: EdgeInsets.all(16),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            Icon(
                              Icons.link,
                              color: Colors.blue,
                            ),
                            SizedBox(width: 10),
                            Text(
                              'CHMT',
                              style: GoogleFonts.lato(
                                fontSize: 17.0,
                                fontWeight: FontWeight.w400,
                                color: Colors.blue,
                              ),
                              textAlign: TextAlign.left,
                            )
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              SizedBox(
                height: MediaQuery.of(context).padding.bottom,
              )
            ],
          )
        ],
      ),
    );
  }

  Widget inkwell(DrawerList listData) {
    var width = MediaQuery.of(context).size.width - 150;
    var animatedBuilder = AnimatedBuilder(
      animation: widget.iconAnimationController,
      builder: (BuildContext context, Widget child) {
        return Transform(
          transform: Matrix4.translationValues(
              width * (1.0 - widget.iconAnimationController.value - 1.0),
              0.0,
              0.0),
          child: Padding(
            padding: EdgeInsets.only(top: 8, bottom: 8),
            child: Container(
              width: width,
              height: 46,
              decoration: BoxDecoration(
                color: Colors.orange[400],
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(0),
                  topRight: Radius.circular(23),
                  bottomLeft: Radius.circular(0),
                  bottomRight: Radius.circular(23),
                ),
              ),
            ),
          ),
        );
      },
    );

    var isSelected = widget.screenIndex == listData.index;

    return Material(
      color: Colors.transparent,
      child: InkWell(
        splashColor: Colors.grey.withOpacity(0.1),
        highlightColor: Colors.transparent,
        onTap: () {
          navigateToScreen(listData.index);
        },
        child: Stack(
          children: <Widget>[
            isSelected ? animatedBuilder : SizedBox(),
            Container(
              padding: EdgeInsets.only(top: 8.0, bottom: 8.0),
              child: Row(
                children: <Widget>[
                  Container(
                    width: 6.0,
                    height: 46.0,
                  ),
                  Padding(
                    padding: EdgeInsets.all(4.0),
                  ),
                  listData.isAssetsImage
                      ? Container(
                    width: 24,
                    height: 24,
                    child: Image.asset(listData.imageName,
                        color:
                        isSelected ? Colors.white : Color(0xFF01477f)),
                  )
                      : Icon(listData.icon.icon,
                      color: isSelected ? Colors.white : Color(0xFF01477f)),
                  Padding(
                    padding: EdgeInsets.all(4.0),
                  ),
                  Text(
                    listData.labelName,
                    style: GoogleFonts.roboto(
                      fontWeight:
                      isSelected ? FontWeight.w500 : FontWeight.w400,
                      fontSize: 16,
                      color: isSelected ? Colors.white : Color(0xFF01477f),
                    ),
                    textAlign: TextAlign.left,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
