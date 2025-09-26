const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const path = require("path");

function loadProto(protoFile, pkgName) {
  const def = protoLoader.loadSync(path.join("/app/protos", protoFile), {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
  });
  const loaded = grpc.loadPackageDefinition(def);
  return loaded[pkgName];
}

module.exports = { loadProto };
