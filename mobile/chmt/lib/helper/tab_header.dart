import 'package:flutter/material.dart';

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