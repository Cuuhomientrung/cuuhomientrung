import 'dart:async';

import 'package:chmt/helper/search_box.dart';
import 'package:chmt/helper/tab_header.dart';
import 'package:chmt/model/model.dart';
import 'package:chmt/pages/rescuer/rescuer_item.dart';
import 'package:chmt/pages/rescuer/rescuer_vm.dart';
import 'package:chmt/utils/utility.dart';
import 'package:diacritic/diacritic.dart';
import 'package:flutter/material.dart';
import 'package:getflutter/getflutter.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:rxdart/rxdart.dart';

enum Address { province, district, commune }

extension Location on Address {
  String get location {
    switch (this) {
      case Address.province:
        return r'tỉnh';
      case Address.district:
        return r'huyện';
      case Address.commune:
        return r'xã';
      default:
        return '';
    }
  }
}

class RescuerPage extends StatefulWidget {

  @override
  State<StatefulWidget> createState() => _RescuerPage();
}

class _RescuerPage extends State<RescuerPage>
    with TickerProviderStateMixin {
  AnimationController animationController;
  ScrollController _scrollController = ScrollController();
  var searchEditingCtl = TextEditingController(text: '');

  final viewModel = RescuerViewModel();

  @override
  void initState() {
    _initAnimation();

    super.initState();
    viewModel.getRescuerList();

    viewModel.refreshStream.listen((e) => _reload());
    viewModel.rescuerStream.listen((e) {
      setState(() {
        rescuerCount = e.length.toString();
      });
    });
  }

  void _reload() {
    viewModel.reset();
    _refresh();
  }

  void _refresh() {
    _scrollController
        .animateTo(0.0,
        curve: Curves.easeOut, duration: const Duration(milliseconds: 300))
        .then((value) {
      animationController
          .reverse()
          .then((v) => viewModel.getRescuerList());
    });
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
    animationController.dispose();
  }

  void _querySubmitted(String query) {
    List<Rescuer> result = List<Rescuer>();

    if (query.isEmpty) {
      result = viewModel.rescuerList;
    } else {
      result = viewModel.rescuerList.where((e) {
        return e.searchText.contains(removeDiacritics(query).toLowerCase());
      }).toList();
    }

    viewModel.rescuerChanged(result);
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
                                return SizedBox();
                            // return Container(
                            //   color: Color(0xFFFEFEFE),
                            //   padding: EdgeInsets.fromLTRB(16, 16, 16, 0),
                            //   child: _filterBar(),
                            // );
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
                  body: StreamBuilder<List<Rescuer>>(
                    stream: viewModel.rescuerStream,
                    builder: (ctx, snapshot) {
                      if (!snapshot.hasData) {
                        return Utility.centerLoadingIndicator();
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
                          var rescuer = snapshot.data[index];
                          var address = viewModel.getLandmark(rescuer);

                          return RescuerItemView(
                            callback: () {},
                            phoneCallback: () => Utility.launchURL(
                              context,
                              url: rescuer.phoneCall,
                              errorMessage: r'Số điện thoại không hợp lệ',
                            ),
                            statusCallback: (){},
                            item: rescuer,
                            address: address,
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
          child: Text(
            r"LỌC",
            style: TextStyle(
              color: Colors.black54,
              fontWeight: FontWeight.w500,
            ),
          ),
          color: Colors.amber,
          size: GFSize.SMALL,
        ),
        GFButton(
          padding: EdgeInsets.symmetric(horizontal: 4),
          onPressed: () => _selectAddress(Address.province),
          child: StreamBuilder<Province>(
            stream: viewModel.selectedProvinceStream,
            builder: (ctx, snapshot) {
              var text = r"Tỉnh";
              if (snapshot.hasData) text = snapshot.data.name;
              return Text('$text ');
            },
          ),
          icon: Icon(
            Icons.location_on,
            size: 16,
            color: Colors.white,
          ),
          color: Colors.blue,
          size: GFSize.SMALL,
        ),
        GFButton(
          padding: EdgeInsets.symmetric(horizontal: 4),
          onPressed: () => _selectAddress(Address.district),
          child: StreamBuilder<District>(
            stream: viewModel.selectedDistrictStream,
            builder: (ctx, snapshot) {
              var text = r"Huyện";
              if (snapshot.hasData) text = snapshot.data.name;
              return Text('$text ');
            },
          ),
          icon: Icon(
            Icons.location_on,
            size: 16,
            color: Colors.white,
          ),
          color: Colors.blue,
          size: GFSize.SMALL,
        ),
        GFButton(
          padding: EdgeInsets.symmetric(horizontal: 4),
          onPressed: () => _selectAddress(Address.commune),
          child: StreamBuilder<Commune>(
            stream: viewModel.selectedCommuneStream,
            builder: (ctx, snapshot) {
              var text = r"Xã";
              if (snapshot.hasData) text = snapshot.data.name;
              return Text('$text ');
            },
          ),
          icon: Icon(
            Icons.location_on,
            size: 16,
            color: Colors.white,
          ),
          color: Colors.blue,
          size: GFSize.SMALL,
        ),
        GFButton(
          padding: EdgeInsets.symmetric(horizontal: 4),
          onPressed: () => _selectStatus(),
          child: StreamBuilder<int>(
            stream: viewModel.statusStream,
            builder: (ctx, snapshot) {
              var text = r"Trạng thái cứu hộ";
              if (snapshot.hasData) text = snapshot.data.rescuerStatus;
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
        list = viewModel.provinceList;
        break;
      case Address.district:
        list = viewModel.districtList;
        break;
      case Address.commune:
        list = viewModel.communeList;
        break;
      default:
        break;
    }

    if (list.isEmpty) return;

    final address = await showDialog<AddressItem>(
        context: context,
        builder: (ctx) {
          var textColor = Color(0xFF01477f);

          final query = BehaviorSubject<String>();
          var textField = TextField(
            cursorColor: Color(0xFF01477f),
            textAlign: TextAlign.center,
            decoration:
            InputDecoration(hintText: r'Chọn ' + '${type.location}'),
            onChanged: query.sink.add,
          );

          return StreamBuilder<String>(
            stream: query.stream,
            builder: (ctx, snapshot) {
              var address = list;
              if (snapshot.hasData && snapshot.data.isNotEmpty) {
                var q = removeDiacritics(snapshot.data.toLowerCase());
                address = address
                    .where((e) =>
                    removeDiacritics(e.name).toLowerCase().contains(q))
                    .toList();
              }

              return SimpleDialog(
                title: textField,
                children: address.map((d) {
                  return Column(
                    children: <Widget>[
                      Divider(height: 0.7),
                      Container(
                        child: Material(
                          color: Colors.transparent,
                          child: InkWell(
                            onTap: () {
                              Navigator.pop(context, d);
                              query.close();
                            },
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
            },
          );
        });

    if (address != null) {
      switch (type) {
        case Address.province:
          viewModel.selectedProvinceChanged(address);
          break;
        case Address.district:
          viewModel.selectedDistrictChanged(address);
          break;
        case Address.commune:
          viewModel.selectedCommuneChanged(address);
          break;
        default:
          break;
      }
      _refresh();
    }
  }

  Future<int> statusChange() async {
    List<int> list = [0, 1, 2, 3, 4];

    return await showDialog<int>(
        context: context,
        builder: (ctx) {
          var textColor = Color(0xFF01477f);

          return SimpleDialog(
            title: Text(
              r'Chọn trạng thái',
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
                              '${d.rescuerStatus}',
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
  }

  void _selectStatus() async {
    final status = await statusChange();

    if (status != null) {
      viewModel.statusChanged(status);
      _refresh();
    }
  }

  var rescuerCount = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          rescuerCount.isNotEmpty ? '$rescuerCount ' + r'đội cứu hộ' : r'Đội cứu hộ',
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
              _refresh();
            },
          )
        ],
      ),
      body: _body(),
    );
  }
}
