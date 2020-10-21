import 'package:flutter/material.dart';

class SearchBox extends StatefulWidget {
  final Color cursorColor;
  final Color textColor;
  final hintText;
  final TextEditingController controller;
  final ValueChanged<String> onChanged;
  final ValueChanged<String> onSubmitted;
  final Function searchAction;

  const SearchBox({
    this.searchAction,
    this.cursorColor,
    this.controller,
    this.textColor,
    this.onChanged,
    this.onSubmitted,
    this.hintText = r"Tìm kiếm",
  });

  @override
  State<StatefulWidget> createState() => SearchBoxState();
}

class SearchBoxState extends State<SearchBox> {
  bool showClearButton = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.fromLTRB(16, 16, 16, 8),
      padding: EdgeInsets.only(top: 2),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: <BoxShadow>[
          BoxShadow(
            color: Colors.grey.withOpacity(0.3),
            blurRadius: 5,
          ),
        ],
        borderRadius: BorderRadius.all(Radius.circular(5.0)),
        border: Border.all(
          width: 0.5,
          color: Colors.grey.withOpacity(0.3),
        ),
      ),
      child: Center(
        child: TextField(
          onSubmitted: (query) {
            FocusScope.of(context).requestFocus(FocusNode());
            widget.onSubmitted(query);
          },
          autofocus: false,
          textInputAction: TextInputAction.search,
          controller: widget.controller,
          onChanged: (query) {
            widget.onChanged(query);
            setState(() => showClearButton = query.isNotEmpty);
          },
          style: TextStyle(
            fontSize: 16,
          ),
          cursorColor: widget.cursorColor,
          decoration: new InputDecoration(
            prefixIcon: InkWell(
              onTap: widget.searchAction,
              child: Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Icon(
                  Icons.search,
                  color: widget.textColor,
                ),
              ),
            ),
            border: InputBorder.none,
            hintText: widget.hintText,
            suffixIcon: showClearButton
                ? InkWell(
              child: Icon(
                Icons.close,
                size: 23,
                color: Color(0xFF888888),
              ),
              onTap: () => setState(() {
                widget.controller.clear();
                showClearButton = false;
                widget.onChanged('');
              }),
            )
                : null,
          ),
        ),
      ),
    );
  }
}
