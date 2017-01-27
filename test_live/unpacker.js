var unpack = require('browser-unpack');
var pack = require('browser-pack');
var concat = require('concat-stream');
var vm = require('vm');

var fs = require('fs');
var src = fs.readFileSync(__dirname + '/before.js', 'utf8');

var rows = unpack(src);

console.log(rows);