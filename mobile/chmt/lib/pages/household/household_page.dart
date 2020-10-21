import 'dart:async';

import 'package:chmt/helper/search_box.dart';
import 'package:chmt/model/model.dart';
import 'package:chmt/utils/utility.dart';
import 'package:diacritic/diacritic.dart';
import 'package:flutter/material.dart';

import 'house_hold_item.dart';
import 'household_vm.dart';

class HouseHoldPage extends StatefulWidget {
  final HouseHoldViewModel viewModel;

  const HouseHoldPage(this.viewModel);

  @override
  State<StatefulWidget> createState() => _HouseHoldPage();
}

class _HouseHoldPage extends State<HouseHoldPage>
    with TickerProviderStateMixin {
  AnimationController animationController;
  ScrollController _scrollController = ScrollController();
  var searchEditingCtl = TextEditingController(text: '');

  Timer timer;

  @override
  void initState() {
    _initAnimation();

    super.initState();
    widget.viewModel.getHouseHoldList();

    // timer = Timer.periodic(Duration(seconds: 15), (Timer t) => _refresh());

    widget.viewModel.refreshStream.listen((e) => _refresh());
  }

  void _refresh() {
    animationController
        .reverse()
        .then((v) => widget.viewModel.getHouseHoldList());
  }

  void _initAnimation() {
    animationController = AnimationController(
      duration: Duration(milliseconds: 500),
      vsync: this,
    );
  }

  @override
  void dispose() {
    super.dispose();
    timer.cancel();
    animationController.dispose();
  }

  void _querySubmitted(String query) {
    List<HouseHold> result = List<HouseHold>();

    if (query.isEmpty) {
      result = widget.viewModel.houseHoldList;
    } else {
      result = widget.viewModel.houseHoldList.where((e) {
        return e.searchText.contains(removeDiacritics(query).toLowerCase());
      }).toList();
    }

    widget.viewModel.houseHoldChanged(result);
  }

  Widget _body() {
    return Stack(
      children: <Widget>[
        InkWell(
          splashColor: Colors.transparent,
          focusColor: Colors.transparent,
          highlightColor: Colors.transparent,
          hoverColor: Colors.transparent,
          onTap: () => Utility.hideKeyboardOf(context),
          child: Column(
            children: <Widget>[
              Expanded(
                child: NestedScrollView(
                  controller: _scrollController,
                  headerSliverBuilder:
                      (BuildContext context, bool innerBoxIsScrolled) {
                    return <Widget>[
                      SliverList(
                        delegate: SliverChildBuilderDelegate(
                          (context, index) {
                            return Container(
                              color: Color(0xFFFEFEFE),
                              padding: EdgeInsets.fromLTRB(16, 16, 16, 0),
                              child: Text('Bộ lọc'),
                            );
                          },
                          childCount: 1,
                        ),
                      ),
                      SliverPersistentHeader(
                        pinned: true,
                        floating: true,
                        delegate: ContestTabHeader(
                            height: 76,
                            child: Container(
                              color: Color(0xFFFEFEFE),
                              height: 76,
                              child: SearchBox(
                                cursorColor: Color(0xFF01477f),
                                textColor: Color(0xFF01477f),
                                controller: searchEditingCtl,
                                onChanged: (q) {},
                                onSubmitted: _querySubmitted,
                              ),
                            )),
                      ),
                    ];
                  },
                  body: StreamBuilder<List<HouseHold>>(
                    stream: widget.viewModel.houseHoldStream,
                    builder: (ctx, snapshot) {
                      if (!snapshot.hasData) {
                        return Center(child: CircularProgressIndicator());
                      }

                      return ListView.builder(
                        itemCount: snapshot.data.length,
                        padding: EdgeInsets.only(top: 4, bottom: 80),
                        scrollDirection: Axis.vertical,
                        itemBuilder: (context, index) {
                          var count = snapshot.data.length;
                          var animation = Tween(begin: 0.2, end: 1.0).animate(
                            CurvedAnimation(
                              parent: animationController,
                              curve: Interval((1 / count) * index, 1.0,
                                  curve: Curves.fastOutSlowIn),
                            ),
                          );
                          animationController.forward();
                          var hh = snapshot.data[index];
                          return HouseHoldItemView(
                            callback: () {},
                            phoneCall: () => Utility.launchURL(
                              context,
                              url: hh.phoneCall,
                              errorMessage: r'Số điện thoại không hợp lệ',
                            ),
                            item: hh,
                            animation: animation,
                            animationController: animationController,
                          );
                        },
                      );
                    },
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return _body();
  }
}

class ContestTabHeader extends SliverPersistentHeaderDelegate {
  final Widget child;
  final double height;

  ContestTabHeader({this.child = const SizedBox(), this.height = 52.0});

  @override
  Widget build(
      BuildContext context, double shrinkOffset, bool overlapsContent) {
    return child;
  }

  @override
  double get maxExtent => height;

  @override
  double get minExtent => height;

  @override
  bool shouldRebuild(SliverPersistentHeaderDelegate oldDelegate) {
    return false;
  }
}
