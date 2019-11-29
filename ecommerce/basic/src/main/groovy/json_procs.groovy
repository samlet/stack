import groovy.json.JsonSlurper

static void jsonProc() {
    def jsonSlurper = new JsonSlurper()
    def object = jsonSlurper.parseText('{ "name": "John", "ID" : "1"}')

    println(object.name);
    println(object.ID);
}

jsonProc()
