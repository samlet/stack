import 'dart:async';

import 'package:crmsfa/src/generated/crmsfa.pbgrpc.dart';
import 'package:crmsfa/src/generated/users_types.pb.dart';
import 'package:grpc/grpc.dart';

import 'package:crmsfa/src/generated/common_types.pb.dart';
import 'package:crmsfa/src/generated/users.pb.dart';
import 'package:crmsfa/src/generated/users.pbgrpc.dart';

Future<void> main(List<String> args) async {
  final channel = new ClientChannel('localhost',
      port: 50051,
      options: const ChannelOptions(
          credentials: const ChannelCredentials.insecure()));
  final users_stub = new UsersClient(channel);
  final crmsfa_stub = new CrmsfaProcsClient(channel);

  final name = args.isNotEmpty ? args[0] : 'world';

  try {
    // call crmsfa service ping
    final pingReply = await crmsfa_stub.ping(new PingRequest()..name = name);
    print('Client received: ${pingReply.message}');

    // call users services
    final response = await users_stub.createUser(new CreateUserRequest()..username = name);
    print('Client received: ${response.user.username}');

    final user1=new User()
      ..username="alexa"
      ..userId=1;
    final user2=new User()
      ..username="christie"
      ..userId=2;
    final users = <User>[user1, user2];
    final req=new GetUsersRequest();
    req.user.addAll(users);
    await for (var user in users_stub.getUsers(req)) {
      print(user);
    }
  } catch (e) {
    print('Caught error: $e');
  }
  await channel.shutdown();
}

