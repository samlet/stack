# procs-go-modules.md
⊕ [模块·golang / go Wiki](https://github.com/golang/go/wiki/Modules)
    Go 1.11包括对此处提出的版本化模块的初步支持。模块是Go 1.11中的一个实验性选择加入功能，其计划是结合反馈并最终确定Go 1.13的功能。即使某些细节可能会发生变化，未来版本也会支持使用Go 1.11或1.12定义的模块。
    最初的原型（vgo）于2018年2月宣布。在2018年7月，对版本化模块的支持登陆主存储库。Go 1.11于2018年8月发布。
⊕ [用 golang 1.11 module 做项目版本管理 - 简书](https://www.jianshu.com/p/c5733da150c6)

+ workspace/tidb/workspace/tikv/procs-tikv.md
+ workspace/tidb/workspace/hello/go.mod
+ workspace/hyperledger/sagas_chain/chain_store/go.mod

## goland
+ 使用goland自动检测即可支持modules:
    Go Modules (vgo) Detected: Configure Integration

## start
```sh
# 在GOPATH之外创建一个目录：

$ mkdir -p /tmp/scratchpad/hello
$ cd /tmp/scratchpad/hello

# 初始化一个新模块：
$ go mod init github.com/you/hello
go: creating new go.mod: module github.com/you/hello

# 写下你的代码：
$ cat <<EOF > hello.go
package main

import (
    "fmt"
    "rsc.io/quote"
)

func main() {
    fmt.Println(quote.Hello())
}
EOF

# 构建并运行：
$ go build 
$ ./hello

Hello, world.

# 该go.mod文件已更新为包含您的依赖项的显式版本，其中v1.5.2这是一个semver标记：
$ cat go.mod
module github.com/you/hello

require rsc.io/quote v1.5.2
```
+ 典型的日常工作流程可以是：

.go根据需要将import语句添加到代码中。
标准命令喜欢go build或go test将根据需要自动添加新的依赖项以满足导入（更新go.mod和下载新的依赖项）。
当需要时，依赖关系的更具体的版本中，可以用诸如命令选择go get foo@v1.2.3，go get foo@master，go get foo@e3702bed2，或直接通过编辑go.mod。

+ 简要介绍您可能使用的其他常用功能：

go list -m all- 查看将在构建中用于所有直接和间接依赖关系的最终版本（详细信息）
go list -u -m all- 查看所有直接和间接依赖关系的可用次要和补丁升级（详细信息）
go get -u或go get -u=patch- 更新所有直接和间接依赖关系到最新的次要或补丁升级（详情）
go build ./...或go test ./...- 从模块根目录运行时构建或测试模块中的所有包（详细信息）
go mod tidy- 修剪任何不再需要的依赖项，go.mod并添加其他OS，体系结构和构建标记组合所需的依赖项（详细信息）
replace指令或gohack- 使用fork，本地副本或依赖项的确切版本（详细信息）
go mod vendor- 创建vendor目录的可选步骤（详细信息）


