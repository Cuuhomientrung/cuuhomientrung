import 'package:chmt/pages/household/household_page.dart';
import 'package:chmt/pages/household/household_vm.dart';
import 'package:chmt/utils/utility.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

enum HomeScreen { houseHold, importantNews, rescueTeam }

GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();

class HomePage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _HomePage();
  }
}

class _HomePage extends State<HomePage> {
  var screen = HomeScreen.houseHold;

  HouseHoldPage houseHoldPage;

  var count = '';

  Widget getBody() {
    switch (screen) {
      case HomeScreen.houseHold:
        if (houseHoldPage == null) {
          final viewModel = Provider.of<HouseHoldViewModel>(context);
          viewModel.houseHoldStream.listen((list) {
            setState(() => count = list.length.toString());
          });
          houseHoldPage = HouseHoldPage(viewModel);
        }
        return houseHoldPage;
      default:
        return Container();
    }
  }

  void changeHomeScreenTo(HomeScreen screen) {
    setState(() => this.screen = screen);
    if (_scaffoldKey.currentState.isDrawerOpen) {
      _scaffoldKey.currentState.openEndDrawer();
    }
  }

  @override
  Widget build(BuildContext context) {
    var menuStyle = GoogleFonts.openSans(
      fontSize: 15,
      fontWeight: FontWeight.w400,
    );

    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        title: Text(
          count.isNotEmpty ? '$count ' + r'trường hợp' : r'Cứu hộ miền Trung',
          style: GoogleFonts.openSans(
            fontSize: 17,
            fontWeight: FontWeight.w600,
          ),
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.replay),
            onPressed: () {
              Utility.hideKeyboardOf(context);
              houseHoldPage.viewModel.refreshChanged(true);
            },
          )
        ],
      ),
      drawer: Drawer(
        child: ListView(
          children: [
            DrawerHeader(
              child: Center(
                child: Container(
                  child: Text(
                    "CHMT 🌻",
                    style: GoogleFonts.merriweather(
                      fontSize: 24,
                      fontWeight: FontWeight.w400,
                    ),
                  ),
                ),
              ),
            ),
            Column(children: [
              InkWell(
                onTap: () => changeHomeScreenTo(HomeScreen.houseHold),
                child:
                    Row(mainAxisAlignment: MainAxisAlignment.start, children: [
                  IconButton(icon: Icon(Icons.home_outlined), onPressed: null),
                  Text(r'Các hộ cần ứng cứu', style: menuStyle)
                ]),
              ),
              Divider(),
              InkWell(
                onTap: () => changeHomeScreenTo(HomeScreen.importantNews),
                child:
                    Row(mainAxisAlignment: MainAxisAlignment.start, children: [
                  IconButton(icon: Icon(Icons.search), onPressed: null),
                  Text(r'Tin tức quan trọng', style: menuStyle)
                ]),
              ),
              Divider(),
              InkWell(
                onTap: () => changeHomeScreenTo(HomeScreen.rescueTeam),
                child:
                    Row(mainAxisAlignment: MainAxisAlignment.start, children: [
                  IconButton(
                      icon: Icon(Icons.bookmark_border), onPressed: null),
                  Text(r'Các đội cứu hộ', style: menuStyle)
                ]),
              ),
            ]),
          ],
        ),
      ),
      body: getBody(),
    );
  }
}
