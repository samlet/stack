import 'dart:async';

import 'package:grpc/grpc.dart';

import 'package:crmsfa/src/generated/common_types.pb.dart';
import 'package:crmsfa/src/generated/crmsfa.pb.dart';
import 'package:crmsfa/src/generated/crmsfa.pbgrpc.dart';

Future<void> main(List<String> args) async {
  final channel = new ClientChannel('localhost',
      port: 50051,
      options: const ChannelOptions(
          credentials: const ChannelCredentials.insecure()));
  final stub = new CrmsfaProcsClient(channel);

  final name = args.isNotEmpty ? args[0] : 'world';

  try {
    final response = await stub.ping(new PingRequest()..name = name);
    print('Client received: ${response.message}');
  } catch (e) {
    print('Caught error: $e');
  }
  await channel.shutdown();
}
