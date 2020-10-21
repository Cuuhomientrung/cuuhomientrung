import 'dart:async';

import 'package:chmt/helper/search_box.dart';
import 'package:chmt/model/model.dart';
import 'package:chmt/utils/utility.dart';
import 'package:diacritic/diacritic.dart';
import 'package:flutter/material.dart';
import 'package:getflutter/getflutter.dart';
import 'package:google_fonts/google_fonts.dart';

import 'house_hold_item.dart';
import 'household_vm.dart';

enum Address { province, district, commune }

extension Location on Address {
  String get location {
    switch (this) {
      case Address.province: return r'tỉnh';
      case Address.district: return r'huyện';
      case Address.commune: return r'xã';
      default: return '';
    }
  }
}

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

    widget.viewModel.refreshStream.listen((e) => _reload());
  }

  void _reload() {
    widget.viewModel.reset();
    _refresh();
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
                              child: _filterBar(),
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
  
  Widget _filterBar() {
    return GFButtonBar(
      alignment: WrapAlignment.start,
      children: [
        GFButton(
          padding: EdgeInsets.symmetric(horizontal: 4),
          onPressed: () => _refresh(),
          child: Text(r"LỌC"),
          color: GFColors.PRIMARY,
          size: GFSize.SMALL,
        ),
        GFButton(
          padding: EdgeInsets.symmetric(horizontal: 4),
          onPressed: () => _selectAddress(Address.province),
          child: StreamBuilder<Province>(
            stream: widget.viewModel.selectedProvinceStream,
            builder: (ctx, snapshot) {
              var text = r"Tỉnh";
              if (snapshot.hasData) text = snapshot.data.name;
              return Text('$text ');
            },
          ),
          icon: Icon(
            Icons.arrow_drop_down,
            color: Colors.white,
          ),
          color: Colors.blue,
          size: GFSize.SMALL,
        ),
        GFButton(
          padding: EdgeInsets.symmetric(horizontal: 4),
          onPressed: () => _selectAddress(Address.district),
          child: StreamBuilder<District>(
            stream: widget.viewModel.selectedDistrictStream,
            builder: (ctx, snapshot) {
              var text = r"Huyện";
              if (snapshot.hasData) text = snapshot.data.name;
              return Text('$text ');
            },
          ),
          icon: Icon(
            Icons.arrow_drop_down,
            color: Colors.white,
          ),
          color: Colors.blue,
          size: GFSize.SMALL,
        ),
        GFButton(
          padding: EdgeInsets.symmetric(horizontal: 4),
          onPressed: () => _selectAddress(Address.commune),
          child: StreamBuilder<Commune>(
            stream: widget.viewModel.selectedCommuneStream,
            builder: (ctx, snapshot) {
              var text = r"Xã";
              if (snapshot.hasData) text = snapshot.data.name;
              return Text('$text ');
            },
          ),
          icon: Icon(
            Icons.arrow_drop_down,
            color: Colors.white,
          ),
          color: Colors.blue,
          size: GFSize.SMALL,
        ),
      ],
    );
  }

  void _selectAddress(Address type) async {
    var list = List<AddressItem>();
    switch (type) {
      case Address.province:
        list = widget.viewModel.provinceList;
      break;
      case Address.district:
        list = widget.viewModel.districtList;
      break;
      case Address.commune:
        list = widget.viewModel.communeList;
      break;
      default: break;
    }

    if (list.isEmpty) return;

    final address = await showDialog<AddressItem>(
        context: context,
        builder: (ctx) {
          var textColor = Color(0xFF01477f);

          return SimpleDialog(
            title: Text(
              r'Chọn ' + '${type.location}',
              textAlign: TextAlign.center,
              style: GoogleFonts.openSans(
                fontSize: 16,
              ),
            ),
            children: list.map((d) {
              return Column(
                children: <Widget>[
                  Divider(height: 0.7),
                  Container(
                    child: Material(
                      color: Colors.transparent,
                      child: InkWell(
                        onTap: () => Navigator.pop(context, d),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(
                            vertical: 16.0,
                            horizontal: 24.0,
                          ),
                          child: Center(
                            child: Text(
                              '${d.name}',
                              textAlign: TextAlign.center,
                              style: GoogleFonts.openSans(
                                color: textColor,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  Divider(height: 0.7),
                ],
              );
            }).toList(),
          );
        });

    if (address != null) {
      switch (type) {
        case Address.province:
          widget.viewModel.selectedProvinceChanged(address);
          break;
        case Address.district:
          widget.viewModel.selectedDistrictChanged(address);
          break;
        case Address.commune:
          widget.viewModel.selectedCommuneChanged(address);
          break;
        default: break;
      }
      _refresh();
    }
  }

  @override
  Widget build(BuildContext context) {
    return _body();
  }
}

///
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
