import "package:test/test.dart";
import 'dart:async';

import 'package:grpc/grpc.dart';

import 'package:crmsfa/src/generated/common_types.pb.dart';
import 'package:crmsfa/src/generated/crmsfa.pb.dart';
import 'package:crmsfa/src/generated/crmsfa.pbgrpc.dart';

void main() {
  final channel = new ClientChannel('localhost',
      port: 50051,
      options: const ChannelOptions(
          credentials: const ChannelCredentials.insecure()));
  final stub = new CrmsfaProcsClient(channel);

  test("CrmsfaProcsClient.ping()", () async {
    final name = 'world';
    try {
      final response = await stub.ping(new PingRequest()..name = name);
      print('Client received: ${response.message}');
    } catch (e) {
      print('Caught error: $e');
    }
  });
}
