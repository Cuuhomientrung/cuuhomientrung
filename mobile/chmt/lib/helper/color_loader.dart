import 'package:flutter/material.dart';
import 'dart:async';

class ColorLoader extends StatefulWidget {
  const ColorLoader();

  @override
  State createState() => _ColorLoaderState();
}

class _ColorLoaderState extends State<ColorLoader>
    with SingleTickerProviderStateMixin {
  List<Color> colors = [
    Colors.purpleAccent,
    Colors.green,
    Colors.red,
    Colors.lightBlue,
  ];

  Duration duration = Duration(milliseconds: 1000);
  Timer timer;

  List<ColorTween> tweenAnimations = [];
  int tweenIndex = 0;

  AnimationController controller;
  List<Animation<Color>> colorAnimations = [];

  @override
  void initState() {
    super.initState();

    controller = new AnimationController(
      vsync: this,
      duration: duration,
    );

    for (int i = 0; i < colors.length - 1; i++) {
      tweenAnimations.add(
        ColorTween(
          begin: colors[i],
          end: colors[i + 1],
        ),
      );
    }

    tweenAnimations.add(
      ColorTween(
        begin: colors[colors.length - 1],
        end: colors[0],
      ),
    );

    for (int i = 0; i < colors.length; i++) {
      Animation<Color> animation = tweenAnimations[i].animate(
        CurvedAnimation(
          parent: controller,
          curve: Interval(
            (1 / colors.length) * (i + 1) - 0.05,
            (1 / colors.length) * (i + 1),
            curve: Curves.linear,
          ),
        ),
      );

      colorAnimations.add(animation);
    }

    tweenIndex = 0;

    timer = Timer.periodic(duration, (Timer t) {
      setState(() {
        tweenIndex = (tweenIndex + 1) % colors.length;
      });
    });

    controller.forward();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.zero,
      margin: EdgeInsets.zero,
      child: Stack(
        alignment: AlignmentDirectional.center,
        children: <Widget>[
          Center(
            child: SizedBox(
              width: 64,
              height: 64,
              child: CircularProgressIndicator(
                strokeWidth: 2.5,
                valueColor: colorAnimations[tweenIndex],
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    timer.cancel();
    controller.dispose();
    super.dispose();
  }
}