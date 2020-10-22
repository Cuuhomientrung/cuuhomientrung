import 'package:chmt/pages/drawer/home_drawer.dart';
import 'package:flutter/material.dart';

class DrawerUserController extends StatefulWidget {
  final double drawerWidth;
  final Function(DrawerIndex) onDrawerCall;
  final Widget screenView;
  final Function(AnimationController) animationController;
  final Function(bool) drawerIsOpen;
  final AnimatedIconData animatedIconData;
  final Widget menuView;
  final DrawerIndex screenIndex;

  const DrawerUserController({
    Key key,
    this.drawerWidth: 250,
    this.onDrawerCall,
    this.screenView,
    this.animationController,
    this.animatedIconData: AnimatedIcons.arrow_menu,
    this.menuView,
    this.drawerIsOpen,
    this.screenIndex,
  }) : super(key: key);

  @override
  _DrawerUserControllerState createState() => _DrawerUserControllerState();
}

class _DrawerUserControllerState extends State<DrawerUserController>
    with TickerProviderStateMixin {
  ScrollController scrollController;
  AnimationController iconAnimationController;
  AnimationController animationController;

  double scrollOffset = 0.0;
  bool isSetDrawer = false;

  void onDrawerClick() {
    if (scrollController.offset != 0.0) {
      scrollController.animateTo(
        0.0,
        duration: Duration(milliseconds: 400),
        curve: Curves.fastOutSlowIn,
      );
    } else {
      scrollController.animateTo(
        widget.drawerWidth,
        duration: Duration(milliseconds: 400),
        curve: Curves.fastOutSlowIn,
      );
    }
  }

  @override
  void initState() {
    animationController = AnimationController(
        duration: Duration(milliseconds: 2000), vsync: this);
    iconAnimationController =
        AnimationController(vsync: this, duration: Duration(milliseconds: 0));
    iconAnimationController.animateTo(1.0,
        duration: Duration(milliseconds: 0), curve: Curves.fastOutSlowIn);
    scrollController =
        ScrollController(initialScrollOffset: widget.drawerWidth);
    scrollController
      ..addListener(() {
        if (scrollController.offset <= 0) {
          if (scrollOffset != 1.0) {
            setState(() {
              scrollOffset = 1.0;
              try {
                widget.drawerIsOpen(true);
              } catch (e) {}
            });
          }
          iconAnimationController.animateTo(0.0,
              duration: Duration(milliseconds: 0), curve: Curves.linear);
        } else if (scrollController.offset > 0 &&
            scrollController.offset < widget.drawerWidth) {
          iconAnimationController.animateTo(
              (scrollController.offset * 100 / (widget.drawerWidth)) / 100,
              duration: Duration(milliseconds: 0),
              curve: Curves.linear);
        } else if (scrollController.offset <= widget.drawerWidth) {
          if (scrollOffset != 0.0) {
            setState(() {
              scrollOffset = 0.0;
              try {
                widget.drawerIsOpen(false);
              } catch (e) {}
            });
          }
          iconAnimationController.animateTo(1.0,
              duration: Duration(milliseconds: 0), curve: Curves.linear);
        }
      });
    getInitState();
    super.initState();
  }

  Future<bool> getInitState() async {
    await Future.delayed(Duration(milliseconds: 300));
    try {
      widget.animationController(iconAnimationController);
    } catch (e) {}
    await Future.delayed(Duration(milliseconds: 100));
    scrollController.jumpTo(
      widget.drawerWidth,
    );
    setState(() {
      isSetDrawer = true;
    });
    return true;
  }

  @override
  Widget build(BuildContext context) {
    var appBarHeight = AppBar().preferredSize.height;

    return Scaffold(
      backgroundColor: Color(0xFFF2F3F8),
      body: SingleChildScrollView(
        controller: scrollController,
        scrollDirection: Axis.horizontal,
        physics: PageScrollPhysics(parent: ClampingScrollPhysics()),
        child: Opacity(
          opacity: isSetDrawer ? 1 : 0,
          child: SizedBox(
            height: MediaQuery.of(context).size.height,
            width: MediaQuery.of(context).size.width + widget.drawerWidth,
            child: Row(
              children: <Widget>[
                SizedBox(
                  width: widget.drawerWidth,
                  height: MediaQuery.of(context).size.height,
                  child: AnimatedBuilder(
                    animation: iconAnimationController,
                    builder: (BuildContext context, Widget child) {
                      return Transform(
                        transform: Matrix4.translationValues(
                            scrollController.offset, 0.0, 0.0),
                        child: SizedBox(
                          height: MediaQuery.of(context).size.height,
                          width: widget.drawerWidth,
                          child: HomeDrawer(
                            screenIndex: widget.screenIndex == null
                                ? DrawerIndex.News
                                : widget.screenIndex,
                            iconAnimationController: iconAnimationController,
                            callBackIndex: (DrawerIndex index) {
                              onDrawerClick();
                              try {
                                widget.onDrawerCall(index);
                              } catch (e) {}
                            },
                          ),
                        ),
                      );
                    },
                  ),
                ),
                SizedBox(
                  width: MediaQuery.of(context).size.width,
                  height: MediaQuery.of(context).size.height,
                  child: Container(
                    decoration: BoxDecoration(
                      color: Color(0xFFF2F3F8),
                      boxShadow: <BoxShadow>[
                        BoxShadow(
                            color: Color(0xFF3A5160).withOpacity(0.6),
                            blurRadius: 24),
                      ],
                    ),
                    child: Stack(
                      children: <Widget>[
                        IgnorePointer(
                          ignoring: scrollOffset == 1 ? true : false,
                          child: widget.screenView == null
                              ? Container(
                            color: Colors.white,
                          )
                              : widget.screenView,
                        ),
                        scrollOffset == 1.0
                            ? InkWell(
                          onTap: () {
                            onDrawerClick();
                          },
                        )
                            : SizedBox(),
                        Padding(
                          padding: EdgeInsets.only(
                              top: MediaQuery.of(context).padding.top+4, left: 8),
                          child: SizedBox(
                            width: appBarHeight - 8,
                            height: appBarHeight - 8,
                            child: Material(
                              color: Colors.transparent,
                              child: InkWell(
                                borderRadius:
                                BorderRadius.circular(appBarHeight),
                                child: Center(
                                  child: widget.menuView != null
                                      ? widget.menuView
                                      : AnimatedIcon(
                                      color: Color(0xFFF2F3F8),
                                      icon: widget.animatedIconData != null
                                          ? widget.animatedIconData
                                          : AnimatedIcons.arrow_menu,
                                      progress: iconAnimationController),
                                ),
                                onTap: () {
                                  FocusScope.of(context)
                                      .requestFocus(FocusNode());
                                  onDrawerClick();
                                },
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
