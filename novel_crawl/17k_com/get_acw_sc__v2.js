// var arg1 = "D5AAB21A010D6550F7064F935021A5548A64971E";


function get_arg2(arg1){
    var _0x5e8b26 = "3000176000856006061501533003690027800375";
    String["prototype"]["hexXor"] = function (_0x4e08d8) {
        var _0x5a5d3b = "";
        for (var _0xe89588 = 0x0; _0xe89588 < this["length"] && _0xe89588 < _0x4e08d8["length"]; _0xe89588 += 0x2) {
            var _0x401af1 = parseInt(this["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x105f59 = parseInt(_0x4e08d8["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x189e2c = (_0x401af1 ^ _0x105f59)["toString"](0x10);
            if (_0x189e2c["length"] == 0x1) {
                _0x189e2c = "0" + _0x189e2c;
            }
            _0x5a5d3b += _0x189e2c;
        }
        return _0x5a5d3b;
    };
    String["prototype"]["unsbox"] = function () {
        var _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24];
        var _0x4da0dc = [];
        var _0x12605e = "";
        for (var _0x20a7bf = 0x0; _0x20a7bf < this["length"]; _0x20a7bf++) {
            var _0x385ee3 = this[_0x20a7bf];
            for (var _0x217721 = 0x0; _0x217721 < _0x4b082b["length"]; _0x217721++) {
                if (_0x4b082b[_0x217721] == _0x20a7bf + 0x1) {
                    _0x4da0dc[_0x217721] = _0x385ee3;
                }
            }
        }
        _0x12605e = _0x4da0dc["join"]("");
        return _0x12605e;
    };

    var _0x23a392 = arg1["unsbox"]();
    arg2 = _0x23a392["hexXor"](_0x5e8b26);
    return arg2
}

// console.log(arg2)