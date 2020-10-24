import 'package:chmt/pages/drawer/drawer_controller.dart';
import 'package:chmt/pages/drawer/home_drawer.dart';
import 'package:chmt/pages/household/household_page.dart';
import 'package:chmt/pages/rescuer/rescuer_page.dart';
import 'package:flutter/services.dart';
import 'package:flutter/material.dart';

class NavigationHomeScreen extends StatefulWidget {
  @override
  _NavigationHomeScreenState createState() => _NavigationHomeScreenState();
}

class _NavigationHomeScreenState extends State<NavigationHomeScreen> {
  Widget screenView;
  DrawerIndex drawerIndex;
  AnimationController sliderAnimationController;

  @override
  void initState() {
    _defaultHome();
    super.initState();
  }

  GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey();

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: onWillPop,
      child: Container(
        child: SafeArea(
          top: false,
          bottom: false,
          child: Scaffold(
            key: _scaffoldKey,
            body: DrawerUserController(
              screenIndex: drawerIndex,
              drawerWidth: MediaQuery.of(context).size.width - 100,
              animationController: (AnimationController animationController) {
                sliderAnimationController = animationController;
              },
              onDrawerCall: (DrawerIndex drawerIndexData) {
                changeIndex(drawerIndexData);
              },
              screenView: screenView,
            ),
          ),
        ),
      ),
    );
  }

  DateTime currentBackPressTime;

  Future<bool> onWillPop() {
    DateTime now = DateTime.now();
    if (currentBackPressTime == null ||
        now.difference(currentBackPressTime) > Duration(milliseconds: 700)) {
      currentBackPressTime = now;
      SystemNavigator.pop();
    }
    return Future.value(false);
  }

  void _defaultHome() {
    drawerIndex = DrawerIndex.HouseHold;
    screenView = HouseHoldPage();
  }
  void changeIndex(DrawerIndex drawerIndexData) {
    if (drawerIndex != drawerIndexData) {
      drawerIndex = drawerIndexData;
      if (drawerIndex == DrawerIndex.HouseHold) {
        setState(() => screenView = HouseHoldPage());
      } else if (drawerIndex == DrawerIndex.RescuerTeam) {
        setState(() => screenView = RescuerPage());
      } else if (drawerIndex == DrawerIndex.News) {

      }
    }
  }
}
