import "package:test/test.dart";

void main() {
  test("String.split() splits the string on the delimiter", () {
    var string = "foo,bar,baz";
    expect(string.split(","), equals(["foo", "bar", "baz"]));
  });

  test("String.trim() removes surrounding whitespace", () {
    var string = "  foo ";
    print(string);
    expect(string.trim(), equals("foo"));
  });

  test(".split() splits the string on the delimiter", () {
    expect("foo,bar,baz", allOf([
      contains("foo"),
      isNot(startsWith("bar")),
      endsWith("baz")
    ]));
  });
}