import 'package:chmt/pages/drawer/navigate_home.dart';
import 'package:chmt/pages/splash/splash_page.dart';
import 'package:flutter/material.dart';

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

class Routes {
  static const String splash = 'splash_screen';
  static const String homePage = 'home_page';
}

///
Route<dynamic> generateRoute(RouteSettings settings) {
  final Map args = settings.arguments;

  switch (settings.name) {
    case Routes.splash:
      return NoAnimationPageRoute(
        settings: RouteSettings(name: Routes.splash),
        builder: (context) => SplashScreen(),
      );

    case Routes.homePage:
      return FadeTransitionPageRoute(
        settings: RouteSettings(name: Routes.homePage),
        builder: (context) => NavigationHomeScreen(),
      );

    default:
      return NoAnimationPageRoute(
        builder: (context) => Scaffold(
          body: Center(
            child: Text('Không tìm thấy ${settings.name}'),
          ),
        ),
      );
  }
}

///
/// NoAnimationPageRoute
///
class NoAnimationPageRoute<T> extends MaterialPageRoute<T> {
  NoAnimationPageRoute({
    @required WidgetBuilder builder,
    RouteSettings settings,
    bool maintainState = true,
    bool fullscreenDialog = false,
  }) : super(
      builder: builder,
      maintainState: maintainState,
      settings: settings,
      fullscreenDialog: fullscreenDialog);

  @override
  Widget buildTransitions(BuildContext context, Animation<double> animation,
      Animation<double> secondaryAnimation, Widget child) {
    return child;
  }

  @override
  Duration get transitionDuration => Duration(milliseconds: 300);
}

///
/// FadeTransitionPageRoute
///
class FadeTransitionPageRoute<T> extends MaterialPageRoute<T> {
  FadeTransitionPageRoute({
    @required WidgetBuilder builder,
    RouteSettings settings,
    bool maintainState = true,
    bool fullscreenDialog = false,
  }) : super(
      builder: builder,
      maintainState: maintainState,
      settings: settings,
      fullscreenDialog: fullscreenDialog);

  @override
  Widget buildTransitions(BuildContext context, Animation<double> animation,
      Animation<double> secondaryAnimation, Widget child) {
    return FadeTransition(
      opacity: animation,
      child: child,
    );
  }

  @override
  Duration get transitionDuration => Duration(milliseconds: 500);
}